<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { CalendarX } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import EventCard from '../components/ui/EventCard.vue'
import FilterChips from '../components/ui/FilterChips.vue'
import { useEventsStore } from '../stores/events'
import { useChipFilter } from '../composables/useChipFilter'

const router = useRouter()
const eventsStore = useEventsStore()

const filterChips = [
  { id: 'all', label: 'All Events' },
  { id: 'upcoming', label: 'Upcoming' },
  { id: 'registered', label: 'My Registrations' },
  { id: 'past', label: 'Past' }
]

const eventsList = computed(() => eventsStore.events)

const { activeFilter, filteredItems } = useChipFilter(eventsList, function matchesStatus(event, filter) {
  return event.status === filter
})

function openEvent(eventId) {
  router.push('/events/' + eventId)
}

onMounted(function loadEventsList() {
  eventsStore.loadEvents()
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content">

    <Topbar title="Events" sub="Upcoming events across all your clubs" />

    <main class="content-body custom-scrollbar">

      <FilterChips :chips="filterChips" v-model="activeFilter" />

      <div class="events-grid">
        <EventCard
          v-for="event in filteredItems"
          :key="event.id"
          :event="event"
          @open="openEvent(event.id)"
        />
      </div>

      <div v-if="filteredItems.length === 0" class="empty-state">
        <CalendarX />
        <p>No events match this filter.</p>
      </div>

    </main>

  </div>
</template>
