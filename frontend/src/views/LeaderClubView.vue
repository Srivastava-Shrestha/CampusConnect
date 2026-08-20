<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useClubsStore } from '../stores/clubs'
import { Pencil, MapPin, Users, Calendar, CalendarPlus, Megaphone, UsersRound } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import ClubIcon from '../components/ui/ClubIcon.vue'
import ClubProposalList from '../components/ui/ClubProposalList.vue'
import { getClubById, updateClub, deleteClub, getMyClubs } from '../api/clubs'
import { getEvents, normalizeEvent } from '../api/events'
import { toast } from '../composables/useToast'
import LeaderClubSwitcher from '../components/ui/LeaderClubSwitcher.vue'
import CustomSelect from '../components/ui/CustomSelect.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const clubsStore = useClubsStore()

const club = ref(null)
const upcomingEvents = ref([])

const categoryOptions = [
  'Tech',
  'Arts',
  'Culture',
  'Sports',
  'Music',
  'Business',
  'Science',
  'Other'
]

const editing = ref(false)
const saving = ref(false)
const clubStats = ref([])

const editForm = ref({
  description: '',
  category: '',
  image_url: ''
})

const selectedClubId = computed({
  get: () => clubsStore.selectedLeaderClub?.id ?? null,
  set: (clubId) => changeClub(clubId)
})



const quickActions = computed(() => [
  {
    label: 'Create Event',
    desc: 'Schedule a new workshop, competition, or meet',
    icon: CalendarPlus,
    iconClass: 'green',
    to: `/${auth.user.collegeSlug}/leader/events/new`
  },
  {
    label: 'Post Announcement',
    desc: 'Broadcast an update to all club members',
    icon: Megaphone,
    iconClass: 'orange',
    to: `/${auth.user.collegeSlug}/leader/announcements/new`
  },
  {
    label: 'Manage Members',
    desc: 'Review join requests and manage your roster',
    icon: UsersRound,
    iconClass: 'blue',
    to: `/${auth.user.collegeSlug}/leader/members`
  }
])

function buildStats(loadedClub) {
  // member_count comes straight from the backend, which counts every
  // APPROVED membership - and the leader has one of those too, created
  // automatically when the club was proposed. "Members" here means the
  // people the leader is leading, not a headcount that includes themselves.
  const regularMemberCount = Math.max(loadedClub.member_count - 1, 0)

  return [
    { num: regularMemberCount, label: 'Members' },
    { num: loadedClub.head?.full_name ?? '-', label: 'Club Head' },
    { num: loadedClub.status, label: 'Status' },
    {
      num: new Date(loadedClub.created_at).getFullYear(),
      label: 'Created'
    }
  ]
}

function manageEvent(event) {
  // Attendance only opens once the event has started; until then the events page
  // carries the publish and cancel actions.
  if (new Date(event.starts_at) <= new Date()) {
    router.push(`/${route.params.slug}/leader/events/${event.id}/attend`)
  } else {
    router.push(`/${route.params.slug}/leader/events`)
  }
}

async function changeBannerImage() {
  const currentUrl = club.value.image_url || ''
  const newUrl = window.prompt('Enter an image URL for the club banner:', currentUrl)

  if (newUrl === null) return
  const trimmed = newUrl.trim()
  if (trimmed === currentUrl) return

  try {
    await updateClub(club.value.id, { image_url: trimmed || null })
    club.value.image_url = trimmed || null
    toast.success('Banner image updated.')
  } catch (error) {
    toast.error(error?.message || 'Could not update the banner image.')
  }
}

function startEditing() {

  editForm.value = {
    description: club.value.description,
    category: club.value.category,
    image_url: club.value.image_url || ''
  }

  editing.value = true
}

async function saveClubEdits() {

  if (!editForm.value.description.trim()) {
    toast.error('Description cannot be empty.')
    return
  }

  if (!editForm.value.category) {
    toast.error('Please choose a category.')
    return
  }

  saving.value = true

  try {

    await updateClub(
      club.value.id,
    {
      description: editForm.value.description.trim(),
      category: editForm.value.category,
      image_url: editForm.value.image_url.trim() || null
    }
  )

    club.value.description = editForm.value.description.trim()
    club.value.category = editForm.value.category
    club.value.image_url = editForm.value.image_url.trim() || null

    clubStats.value = buildStats(club.value)

    editing.value = false

    toast.success('Club updated successfully.')

  } catch (error) {

    toast.error(error.message)

  } finally {

    saving.value = false

  }

}
function cancelEditing() {
  editing.value = false
}

const deleting = ref(false)

async function deleteCurrentClub() {

  const confirmed = window.confirm(
    'Are you sure you want to delete this club?\n\nThis action cannot be undone.'
  )

  if (!confirmed) return

  deleting.value = true

  try {

    await deleteClub(club.value.id)

    toast.success('Club deleted successfully.')

    router.push(`/${auth.user.collegeSlug}/clubs`)

  } catch (error) {

    toast.error(error.message)
    deleting.value = false

  }

}

async function changeClub(clubId) {
  clubsStore.selectLeaderClub(clubId)
  await loadClubData(clubId)
}

async function loadClubData(clubId) {
  try {
    club.value = await getClubById(clubId)

    clubStats.value = buildStats(club.value)

    const rows = await getEvents({
      club_id: clubId,
      upcoming_only: true
    })

    upcomingEvents.value = rows
      .map(row => normalizeEvent(row))
      .filter(event => event.status !== 'cancelled')

  } catch (error) {
    console.error(error)
    toast.error('Failed to load club details.')
  }
}

// Having no club yet is a normal starting state, not an error. This page used
// to toast "No active club assigned" and redirect to /clubs, which left the
// leader with no explanation and no route to creating one. We now stay put and
// render the empty state below instead.
const hasLoaded = ref(false)

const hasNoClub = computed(() => hasLoaded.value && clubsStore.leaderClubs.length === 0)

function goToCreateClub() {
  router.push(`/${auth.user.collegeSlug}/clubs/propose`)
}

// Every club this student created, in any state, so a leader can see the
// approval status of proposals that are not live yet alongside the club they
// already run.
const proposals = ref([])
const loadingProposals = ref(true)

async function loadProposals() {
  loadingProposals.value = true

  try {
    proposals.value = await getMyClubs({ role: 'LEADER' })
  } catch (error) {
    proposals.value = []
  } finally {
    loadingProposals.value = false
  }
}

onMounted(loadProposals)

onMounted(async () => {
  try {
    await clubsStore.loadLeaderClubs()

    if (clubsStore.leaderClubs.length) {
      await loadClubData(clubsStore.selectedLeaderClub.id)
    }

  } catch (error) {
    console.error(error)
    toast.error('Failed to load club information.')
  } finally {
    hasLoaded.value = true
  }
})
</script>

<template>
  <LeaderSidebar />

  <div v-if="!hasLoaded" class="main-content page-loading-state">
    <div class="empty-state">
      <p>Loading your club...</p>
    </div>
  </div>

  <div class="main-content" v-else-if="hasNoClub">

    <header class="topbar">
      <div class="title-block">
        <h1 class="page-title">My Club</h1>
        <p class="page-sub">You do not lead a club yet</p>
      </div>
    </header>

    <main class="content-body custom-scrollbar">
      <div class="empty-state">
        <UsersRound />
        <p>
          You are not leading a club yet. Start one and it will show up here,
          along with its members, events and announcements.
        </p>
        <button class="btn-primary" @click="goToCreateClub">
          <CalendarPlus /> Start a new club
        </button>
      </div>
    </main>

  </div>

  <div class="main-content" v-else-if="club">

    <header class="topbar">
      <div class="title-block">
        <h1 class="page-title">My Club</h1>
      </div>
      <div class="topbar-spacer"></div>
      <div style="display:flex;gap:12px;align-items:center;">

        <div v-if="clubsStore.leaderClubs.length > 1" class="leader-club-switcher">
          <CustomSelect
             v-model="selectedClubId"
             :options="
              clubsStore.leaderClubs.map(c => ({
                value: c.id,
                label: c.name
                }))
              "
              placeholder="Select Club"/>
        </div>

        <button class="btn-secondary" @click="startEditing"> <Pencil />Edit Club Info</button>

        <button
          class="btn-secondary"
          style="background:#ef4444;color:white;"
          :disabled="deleting"
          @click="deleteCurrentClub"
        >
          <span v-if="deleting" class="btn-spinner"></span>
          <template v-else>Delete Club</template>
        </button>

      </div>
    </header>

    <main class="content-body custom-scrollbar">

      <div>
        <div
          class="club-profile-banner"
          :class="{ 'banner-blue': !club.image_url }"
          :style="club.image_url ? { backgroundImage: `url(${club.image_url})` } : {}"
        >
          <template v-if="!club.image_url">
            <div class="club-card-circle-1"></div>
            <div class="club-card-circle-2"></div>
            <div class="club-card-circle-3"></div>
          </template>
          <div class="club-profile-icon">
            <ClubIcon name="users" />
          </div>
          <button class="banner-edit-btn" title="Change banner image" @click="changeBannerImage">
            <Pencil />
          </button>
        </div>
        <div class="club-profile-meta">
          <p class="club-profile-name">{{ club.name }}</p>
          <div class="club-profile-sub">
            <span class="cat-chip">{{ club.category }}</span>
            <span><MapPin /> {{ club.type }}</span>
            <span><Users /> {{ club.member_count }} members</span>
            <span><Calendar /> {{ new Date(club.created_at).getFullYear() }}</span>
          </div>
        </div>
      </div>

      <div class="club-stats-row">
        <div v-for="stat in clubStats" :key="stat.label" class="club-stat-card">
          <p class="club-stat-num">{{ stat.num }}</p>
          <p class="club-stat-label">{{ stat.label }}</p>
        </div>
      </div>

      <div>
        <p class="section-heading">Quick Actions</p>
        <div class="quick-actions-grid">
          <router-link
            v-for="action in quickActions"
            :key="action.to"
            :to="action.to"
            class="quick-action-card"
          >
            <div class="quick-action-icon" :class="action.iconClass">
              <component :is="action.icon" />
            </div>
            <p class="quick-action-label">{{ action.label }}</p>
            <p class="quick-action-desc">{{ action.desc }}</p>
          </router-link>
        </div>
      </div>

      <div class="card">

  <p class="section-heading">About the Club</p>

  <div v-if="!editing">
  <p>{{ club.description }}</p>
</div>

<div v-if="editing">

  <div class="form-group">
    <label>Category</label>

    <select v-model="editForm.category" class="input-field">
      <option
        v-for="category in categoryOptions"
        :key="category"
        :value="category"
      >
        {{ category }}
      </option>
    </select>
  </div>

  <div class="form-group">
    <label>Description</label>

    <textarea
      v-model="editForm.description"
      rows="6"
      class="input-field"
    ></textarea>
  </div>

  <div class="form-group">
    <label>Image URL</label>

    <input
      v-model="editForm.image_url"
      class="input-field"
    />
  </div>

  <div style="display:flex;gap:10px;margin-top:20px;">

    <button
      class="btn-primary"
      :disabled="saving"
      @click="saveClubEdits"
    >
      <span v-if="saving" class="btn-spinner"></span>
      <template v-else>Save Changes</template>
    </button>

    <button
      class="btn-secondary"
      :disabled="saving"
      @click="cancelEditing"
    >
      Cancel
    </button>

  </div>

</div>

</div>

      <div>
        <p class="section-heading">Upcoming Events</p>
        <div class="club-event-list">
          <div v-for="event in upcomingEvents" :key="event.id" class="club-event-row">
            <div class="club-event-date-box">
              <span class="club-event-date-day">{{ event.day }}</span>
              <span class="club-event-date-month">{{ event.month }}</span>
            </div>
            <div class="club-event-info">
              <p class="club-event-title">{{ event.title }}</p>
              <p class="club-event-sub">{{ event.venue }} · {{ event.time }} · {{ event.registered }} registered</p>
            </div>
            <button class="btn-secondary-sm" @click="manageEvent(event)">Manage</button>
          </div>
        </div>
      </div>

      <ClubProposalList :proposals="proposals" :loading="loadingProposals" />

    </main>

  </div>
</template>

