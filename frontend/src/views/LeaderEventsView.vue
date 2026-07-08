<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Clock, MapPin, Users, CalendarX, ClipboardCheck, Trophy, Medal } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import FilterChips from '../components/ui/FilterChips.vue'
import { getLeaderEvents } from '../api/events'

const router = useRouter()

const events = ref([])
const activeFilter = ref('all')

const filterChips = [
  { id: 'all', label: 'All Events' },
  { id: 'upcoming', label: 'Upcoming' },
  { id: 'past', label: 'Past' },
  { id: 'needs-action', label: 'Needs Action' }
]

const visibleEvents = computed(function filterEvents() {
  return events.value.filter(function matchesFilter(event) {
    if (activeFilter.value === 'all') return true
    if (activeFilter.value === 'past') return event.status === 'past' || event.status === 'needs-action'
    return event.status === activeFilter.value
  })
})

function statusPillClass(event) {
  if (event.status === 'needs-action') return 'registered'
  return event.status === 'past' ? 'past' : 'upcoming'
}

function manageEvent(event) {
  if (event.action === 'attendance') {
    router.push('/leader/events/' + event.id + '/attend')
  } else {
    router.push('/leader/events/' + event.id + '/results')
  }
}

function manageLabel(event) {
  if (event.action === 'attendance') return 'Take Attendance'
  if (event.action === 'set-results') return 'Set Results'
  return 'View Results'
}

function goToCreateEvent() {
  router.push('/leader/events/new')
}

onMounted(async function loadLeaderEvents() {
  events.value = await getLeaderEvents()
})
</script>

<template>
  <LeaderSidebar />

  <div class="main-content">

    <Topbar title="Events" sub="Robotics & Automation Club">
      <button class="btn-primary" @click="goToCreateEvent">
        <Plus /> Create Event
      </button>
    </Topbar>

    <main class="content-body custom-scrollbar">

      <FilterChips :chips="filterChips" v-model="activeFilter" />

      <div class="events-grid">
        <div v-for="event in visibleEvents" :key="event.id" class="event-card">
          <div class="event-card-accent" :class="event.accent"></div>
          <div class="event-card-date-box">
            <span class="event-date-day">{{ event.day }}</span>
            <span class="event-date-month">{{ event.month }}</span>
          </div>
          <div class="event-card-body">
            <div>
              <p class="event-card-title">{{ event.title }}</p>
              <p class="event-card-club">{{ event.type }}</p>
              <div class="event-card-meta">
                <span><Clock /> {{ event.time }}</span>
                <span><MapPin /> {{ event.venue }}</span>
              </div>
            </div>
            <div class="event-card-footer">
              <span class="event-status" :class="statusPillClass(event)">{{ event.statusLabel }}</span>
              <span class="club-card-members"><Users /> {{ event.countText }}</span>
            </div>
            <div class="event-card-manage-row">
              <button class="btn-secondary-sm" @click="manageEvent(event)">
                <ClipboardCheck v-if="event.action === 'attendance'" />
                <Trophy v-else-if="event.action === 'set-results'" />
                <Medal v-else />
                {{ manageLabel(event) }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="visibleEvents.length === 0" class="empty-state">
        <CalendarX />
        <p>No events match this filter.</p>
      </div>

    </main>

  </div>
</template>
