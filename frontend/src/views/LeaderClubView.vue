<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Pencil, MapPin, Users, Calendar, CalendarPlus, Megaphone, UsersRound } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import ClubIcon from '../components/ui/ClubIcon.vue'
import { getClubById } from '../api/clubs'
import { getLeaderEvents } from '../api/events'
import { toast } from '../composables/useToast'

const router = useRouter()

const club = ref(null)
const upcomingEvents = ref([])

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
    { num: loadedClub.members, label: 'Members' },
    { num: loadedClub.eventsRun, label: 'Events Run' },
    { num: 3, label: 'Join Requests' },
    { num: loadedClub.founded, label: 'Founded' }
  ]
}

function manageEvent(event) {
  if (event.action === 'attendance') {
    router.push('/leader/events/' + event.id + '/attend')
  } else {
    router.push('/leader/events')
  }
}

function showEditHint() {
  toast.info('Club info editing will be available after the backend is connected.')
}

onMounted(async function loadDashboard() {
  club.value = await getClubById(1)
  clubStats.value = buildStats(club.value)

  const allLeaderEvents = await getLeaderEvents()
  upcomingEvents.value = allLeaderEvents.filter(function onlyUpcoming(event) {
    return event.status === 'upcoming'
  })
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
      <button class="btn-secondary" @click="showEditHint">
        <Pencil /> Edit Club Info
      </button>
    </header>

    <main class="content-body custom-scrollbar">

      <div>
        <div class="club-profile-banner" :class="club.banner">
          <div class="club-card-circle-1"></div>
          <div class="club-card-circle-2"></div>
          <div class="club-card-circle-3"></div>
          <div class="club-profile-icon">
            <ClubIcon :name="club.icon" />
          </div>
        </div>
        <div class="club-profile-meta">
          <p class="club-profile-name">{{ club.name }}</p>
          <div class="club-profile-sub">
            <span class="cat-chip">{{ club.category }}</span>
            <span><MapPin /> {{ club.college }}</span>
            <span><Users /> {{ club.members }} members</span>
            <span><Calendar /> Founded {{ club.founded }}</span>
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
        <p>{{ club.about }}</p>
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
              <p class="club-event-sub">{{ event.type }} · {{ event.venue }} · {{ event.time }} · {{ event.countText }} registered</p>
            </div>
            <button class="btn-secondary-sm" @click="manageEvent(event)">Manage</button>
          </div>
        </div>
      </div>

    </main>

  </div>
</template>
