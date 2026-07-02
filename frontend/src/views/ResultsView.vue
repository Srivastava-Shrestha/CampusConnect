<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Award } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import { getEventParticipants, getEventById, saveResults } from '../api/events'

const route = useRoute()
const router = useRouter()

const event = ref(null)
const attendees = ref([])
const results = ref({})

const resultOptions = [
  { value: 'participant', label: 'Participant' },
  { value: 'runner-up', label: 'Runner-up' },
  { value: 'winner', label: 'Winner' }
]

function countResult(value) {
  return Object.values(results.value).filter((result) => result === value).length
}

function validateResults() {
  if (countResult('winner') > 1) {
    window.alert('Only one participant can be marked as Winner.')
    return false
  }
  if (countResult('runner-up') > 2) {
    window.alert('At most two participants can be marked as Runner-up.')
    return false
  }
  return true
}

async function publishResults() {
  if (!validateResults()) return

  await saveResults(route.params.id, results.value)
  window.alert('Results published! Certificates have been generated and are visible on each student profile.')
  router.push('/leader/events')
}

function goBackToAttendance() {
  router.push('/leader/events/' + route.params.id + '/attend')
}

onMounted(async function loadResultsPage() {
  event.value = await getEventById(route.params.id)
  attendees.value = await getEventParticipants(route.params.id)

  attendees.value.forEach(function defaultToParticipant(attendee) {
    results.value[attendee.id] = 'participant'
  })
})
</script>

<template>
  <LeaderSidebar />

  <div class="main-content">

    <header class="topbar">
      <button class="btn-secondary" @click="goBackToAttendance">
        <ArrowLeft /> Attendance
      </button>
      <div class="title-block">
        <h1 class="page-title">Set Results</h1>
        <p class="page-sub" v-if="event">{{ event.title }} · {{ attendees.length }} attended</p>
      </div>
      <div class="topbar-spacer"></div>
    </header>

    <main class="content-body custom-scrollbar">

      <div class="club-profile-meta">
        <p class="section-heading">Attendees</p>
        <p class="text-note">Assign a result to each participant. Certificates will be generated automatically after you publish.</p>
      </div>

      <div class="participant-list mt-16">
        <div v-for="attendee in attendees" :key="attendee.id" class="participant-row">
          <div class="participant-avatar">{{ attendee.initials }}</div>
          <div class="participant-info">
            <p class="participant-name">{{ attendee.name }}</p>
            <p class="participant-sub">{{ attendee.sub }}</p>
          </div>
          <select class="result-select-field" v-model="results[attendee.id]">
            <option v-for="option in resultOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
          </select>
        </div>
      </div>

      <div class="event-action-bar">
        <p class="text-note">Certificates are issued instantly after publishing results.</p>
        <button class="btn-primary" @click="publishResults">
          <Award /> Publish Results
        </button>
      </div>

    </main>

  </div>
</template>
