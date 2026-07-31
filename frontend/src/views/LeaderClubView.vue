<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Pencil, MapPin, Users, Calendar, CalendarPlus, Megaphone, UsersRound } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import ClubIcon from '../components/ui/ClubIcon.vue'
import { getClubById, getMyClubs, updateClub, deleteClub } from '../api/clubs'
import { getEvents, normalizeEvent } from '../api/events'
import { toast } from '../composables/useToast'
import CustomSelect from '../components/ui/CustomSelect.vue'

const router = useRouter()

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

const editForm = ref({
  description: '',
  category: '',
  image_url: ''
})

const clubStats = ref([])

const quickActions = [
  {
    label: 'Create Event',
    desc: 'Schedule a new workshop, competition, or meet',
    icon: CalendarPlus,
    iconClass: 'green',
    to: '/leader/events/new'
  },
  {
    label: 'Post Announcement',
    desc: 'Broadcast an update to all club members',
    icon: Megaphone,
    iconClass: 'orange',
    to: '/leader/announcements/new'
  },
  {
    label: 'Manage Members',
    desc: 'Review join requests and manage your roster',
    icon: UsersRound,
    iconClass: 'blue',
    to: '/leader/members'
  }
]

function buildStats(loadedClub) {
  return [
    { num: loadedClub.member_count, label: 'Members' },
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
    router.push('/leader/events/' + event.id + '/attend')
  } else {
    router.push('/leader/events')
  }
}

function startEditing() {
  alert("Edit button clicked!")

  editForm.value = {
    description: club.value.description,
    category: club.value.category,
    image_url: club.value.image_url || ''
  }

  editing.value = true

  console.log("editing =", editing.value)
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

async function deleteCurrentClub() {

  const confirmed = window.confirm(
    'Are you sure you want to delete this club?\n\nThis action cannot be undone.'
  )

  if (!confirmed) return

  try {

    await deleteClub(club.value.id)

    toast.success('Club deleted successfully.')

    router.push('/clubs')

  } catch (error) {

    toast.error(error.message)

  }

}
onMounted(async function loadDashboard() {

  try {
    const myClubs = await getMyClubs({ role: 'LEADER' })

    if (!myClubs.length) {
      toast.error('No club assigned.')
      return
    }

    club.value = await getClubById(myClubs[0].id)
    console.log("Club Details:", club.value)
    clubStats.value = buildStats(club.value)

  } catch (error) {
    console.error(error)
    toast.error('Failed to load club information.')
    return
  }
  try {

    const rows = await getEvents({
      club_id: club.value.id,
      upcoming_only: true
    })

    upcomingEvents.value = rows
      .map(row => normalizeEvent(row))
      .filter(event => event.status !== 'cancelled')

  } catch (error) {
    console.error('Failed to load club events:', error)
    upcomingEvents.value = []
  }

})
</script>

<template>
  <LeaderSidebar />

  <div class="main-content" v-if="club">

    <header class="topbar">
      <div class="title-block">
        <h1 class="page-title">My Club</h1>
        <p class="page-sub">{{ club.name }}</p>
      </div>
      <div class="topbar-spacer"></div>
      <div style="display:flex;gap:12px;">

        <button class="btn-secondary" @click="startEditing"> <Pencil />Edit Club Info</button>

        <button
          class="btn-secondary"
          style="background:#ef4444;color:white;"
          @click="deleteCurrentClub"
        >
          Delete Club
        </button>

      </div>
    </header>

    <main class="content-body custom-scrollbar">

      <div>
        <div class="club-profile-banner banner-blue">
          <div class="club-card-circle-1"></div>
          <div class="club-card-circle-2"></div>
          <div class="club-card-circle-3"></div>
          <div class="club-profile-icon">
            <ClubIcon name="users" />
          </div>
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
      @click="saveClubEdits"
    >
      Save Changes
    </button>

    <button
      class="btn-secondary"
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

    </main>

  </div>
</template>

