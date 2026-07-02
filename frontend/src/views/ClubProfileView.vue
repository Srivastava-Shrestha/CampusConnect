<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, UserPlus, Clock, MapPin, Users } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import { useClubsStore } from '../stores/clubs'
import { useEventsStore } from '../stores/events'
import { requestToJoinClub } from '../api/clubs'

const route = useRoute()
const router = useRouter()
const clubsStore = useClubsStore()
const eventsStore = useEventsStore()

const joinState = ref('none')

const club = computed(() => clubsStore.currentClub)

const clubEvents = computed(function eventsForThisClub() {
  if (!club.value) return []
  return eventsStore.events.filter(function belongsToClub(event) {
    return event.club === club.value.name && event.status !== 'past'
  })
})

async function handleJoinRequest() {
  if (joinState.value === 'pending') return

  joinState.value = 'pending'
  await requestToJoinClub(route.params.id)
}

function goBackToClubs() {
  router.push('/clubs')
}

function showRegisterHint() {
  window.alert('Register for this event from the Events page.')
}

onMounted(function loadProfile() {
  clubsStore.loadClub(route.params.id)
  eventsStore.loadEvents()
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content" v-if="club">

    <header class="topbar">
      <button class="btn-secondary" @click="goBackToClubs">
        <ArrowLeft /> Back to Clubs
      </button>

      <div class="title-block">
        <h1 class="page-title">{{ club.name }}</h1>
        <p class="page-sub">{{ club.category }} · {{ club.college }}</p>
      </div>

      <div class="topbar-spacer"></div>

      <button class="btn-join" :class="{ pending: joinState === 'pending' }" @click="handleJoinRequest">
        <Clock v-if="joinState === 'pending'" />
        <UserPlus v-else />
        {{ joinState === 'pending' ? 'Request Sent' : 'Request to Join' }}
      </button>
    </header>

    <main class="content-body custom-scrollbar">

      <div>
        <div class="club-profile-banner" :class="club.banner">
          <div class="club-card-circle-1"></div>
          <div class="club-card-circle-2"></div>
          <div class="club-card-circle-3"></div>
          <div class="club-profile-icon">{{ club.emoji }}</div>
        </div>
        <div class="club-profile-meta">
          <p class="club-profile-name">{{ club.name }}</p>
          <div class="club-profile-sub">
            <span class="cat-chip">{{ club.category }}</span>
            <span><MapPin /> {{ club.college }}</span>
            <span><Users /> {{ club.members }} members</span>
          </div>
          <p v-if="joinState === 'pending'" class="join-status-text">
            Your join request is pending approval from the club leader.
          </p>
        </div>
      </div>

      <div class="club-stats-row">
        <div class="club-stat-card">
          <p class="club-stat-num">{{ club.members }}</p>
          <p class="club-stat-label">Members</p>
        </div>
        <div class="club-stat-card">
          <p class="club-stat-num">{{ club.eventsRun }}</p>
          <p class="club-stat-label">Events Run</p>
        </div>
        <div class="club-stat-card">
          <p class="club-stat-num">{{ club.founded }}</p>
          <p class="club-stat-label">Founded</p>
        </div>
      </div>

      <div class="card">
        <p class="section-heading">About</p>
        <p>{{ club.about }}</p>
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
</template>
