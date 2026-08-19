<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, UserPlus, Clock, MapPin, Users } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import ClubIcon from '../components/ui/ClubIcon.vue'
import { useClubsStore } from '../stores/clubs'
import { useEventsStore } from '../stores/events'
import { requestToJoinClub } from '../api/clubs'
import { toast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const clubsStore = useClubsStore()
const eventsStore = useEventsStore()

const joinState = ref('none')

const club = computed(() => clubsStore.currentClub)

const clubEvents = computed(function eventsForThisClub() {
  if (!club.value) return []
  return eventsStore.events.filter(function belongsToClub(event) {
    return event.club_id === club.value.id && event.status !== 'past'
  })
})

watch(
  () => route.params.id,
  async (id) => {
    joinState.value = 'none'

    try {
      await clubsStore.loadClub(id)
    } catch (error) {
      toast.error(error?.message || 'Failed to load club.')
    }
  }
)

async function handleJoinRequest() {
  if (joinState.value === 'pending') return

  try {
    await requestToJoinClub(route.params.id)
    joinState.value = 'pending'
    toast.success('Join request sent successfully.')
  } catch (error) {
    toast.error(error?.message || 'Failed to send join request.')
  }
}

function goBackToClubs() {
  router.push(`/${route.params.slug}/clubs`)
}

function showRegisterHint() {
  toast.info('Register for this event from the Events page.')
}

function categoryIcon(category) {
  const map = {
    tech: "laptop",
    arts: "palette",
    culture: "drama",
    sports: "sports",
    music: "music",
    business: "briefcase",
    science: "microscope",
  }

  return map[(category || "").toLowerCase()] || "robot"
}

onMounted(async function loadProfile() {
  try {
    await Promise.all([
      clubsStore.loadClub(route.params.id),
      eventsStore.loadEvents()
    ])
  } catch (error) {
    toast.error(error?.message || 'Failed to load club details.')
  }
})
</script>

<template>
  <StudentSidebar />

  <div v-if="club" class="main-content">

    <header class="topbar">
      <button class="btn-secondary" @click="goBackToClubs">
        <ArrowLeft /> Back to Clubs
      </button>

      <div class="title-block">
        <h1 class="page-title">{{ club.name }}</h1>
        <p class="page-sub">{{ club.category }} · {{ club.type }}</p>
      </div>

      <div class="topbar-spacer"></div>

      <button class="btn-join" :disabled="joinState === 'pending'" :class="{ pending: joinState === 'pending' }" @click="handleJoinRequest"
>
        <Clock v-if="joinState === 'pending'" />
        <UserPlus v-else />
        {{ joinState === 'pending' ? 'Request Sent' : 'Request to Join' }}
      </button>
    </header>

    <main class="content-body custom-scrollbar">

      <div>
        <div class="club-profile-banner">
          <div class="club-card-circle-1"></div>
          <div class="club-card-circle-2"></div>
          <div class="club-card-circle-3"></div>
          <div class="club-profile-icon">
            <ClubIcon :name="categoryIcon(club.category)" />
          </div>
        </div>
        <div class="club-profile-meta">
          <p class="club-profile-name">{{ club.name }}</p>
          <div class="club-profile-sub">
            <span class="cat-chip">{{ club.category }}</span>
            <span><MapPin /> {{ club.type }}</span>
            <span><Users /> {{ club.member_count }} members</span>
          </div>
          <p v-if="joinState === 'pending'" class="join-status-text">
            Your join request is pending approval from the club leader.
          </p>
        </div>
      </div>

      <div class="club-stats-row">
        <div class="club-stat-card">
          <p class="club-stat-num">{{ club.member_count }}</p>
          <p class="club-stat-label">Members</p>
        </div>
        <div class="club-stat-card">
          <p class="club-stat-num">{{ clubEvents.length }}</p>
          <p class="club-stat-label">Events Run</p>
        </div>
        <div class="club-stat-card">
          <p class="club-stat-num">
            {{ club.created_at ? new Date(club.created_at).getFullYear() : '-' }}
          </p>
          <p class="club-stat-label">Founded</p>
        </div>
      </div>

      <div class="card">
        <p class="section-heading">About</p>
        <p>{{ club.description }}</p>
      </div>

      <div>
        <p class="section-heading">Upcoming Events</p>
        <div class="club-event-list">

          <div v-for="event in clubEvents" :key="event.id" class="club-event-row">
            <div class="club-event-date-box">
              <span class="club-event-date-day">{{ event.day }}</span>
              <span class="club-event-date-month">{{ event.month }}</span>
            </div>
            <div class="club-event-info">
              <p class="club-event-title">{{ event.title }}</p>
              <p class="club-event-sub">{{ event.venue }} · {{ event.time }}</p>
            </div>
            <button class="btn-secondary-sm" @click="showRegisterHint">
              Register
            </button>
          </div>

        </div>
      </div>

    </main>

  </div>
  <div v-else class="empty-state">
    <Users />
      <p>Unable to load club details.</p>
</div>
</template>
