<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Award } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import CustomSelect from '../components/ui/CustomSelect.vue'
import {
  getEventParticipants, getEventById, setResult,
  normalizeEvent, normalizeParticipant
} from '../api/events'
import { toast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()

const event = ref(null)
const participants = ref([])
const results = ref({})
const saving = ref(false)

const resultOptions = [
  { value: 'PARTICIPANT', label: 'Participant' },
  { value: 'RUNNER_UP', label: 'Runner-up' },
  { value: 'WINNER', label: 'Winner' }
]

// A result can only be recorded for someone who was checked in at the event.
const attendees = computed(function checkedInOnly() {
  return participants.value.filter((participant) => participant.checked_in)
})

function countResult(value) {
  return Object.values(results.value).filter((result) => result === value).length
}

function validateResults() {
  if (countResult('WINNER') > 1) {
    toast.error('Only one participant can be marked as Winner.')
    return false
  }
  if (countResult('RUNNER_UP') > 2) {
    toast.error('At most two participants can be marked as Runner-up.')
    return false
  }
  return true
}

function changedRows() {
  return attendees.value.filter(function hasChanged(attendee) {
    return results.value[attendee.registration_id] !== attendee.result
  })
}

async function publishResults() {
  if (!validateResults()) return

  const changed = changedRows()

  if (!changed.length) {
    toast.info('No result changes to publish.')
    return
  }

  saving.value = true

  const outcomes = await Promise.allSettled(
    changed.map(function saveRow(attendee) {
      return setResult(
        route.params.id,
        attendee.registration_id,
        results.value[attendee.registration_id]
      )
    })
  )

  saving.value = false

  const failed = outcomes.filter((outcome) => outcome.status === 'rejected')

  if (failed.length) {
    toast.error(`${failed.length} of ${changed.length} results failed: ${failed[0].reason.message}`)
    await loadParticipants()
    return
  }

  toast.success('Results published! Each student can now see their result on the event page.')
  router.push('/leader/events')
}

async function loadParticipants() {
  const rows = await getEventParticipants(route.params.id)

  participants.value = rows.map((row) => normalizeParticipant(row))

  const draft = {}
  attendees.value.forEach(function seedCurrentResult(attendee) {
    // REGISTRANT is the sign-up default rather than an outcome, so it starts at Participant.
    draft[attendee.registration_id] =
      attendee.result === 'REGISTRANT' ? 'PARTICIPANT' : attendee.result
  })
  results.value = draft
}

function goBackToAttendance() {
  router.push('/leader/events/' + route.params.id + '/attend')
}

onMounted(async function loadResultsPage() {
  try {
    event.value = normalizeEvent(await getEventById(route.params.id))
    await loadParticipants()
  } catch (error) {
    toast.error(error.message)
  }
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
        <p class="text-note">
          Assign a result to each attendee. Only students marked present on the Attendance page
          appear here.
        </p>
      </div>

      <div class="participant-list mt-16">
        <div v-for="attendee in attendees" :key="attendee.registration_id" class="participant-row">
          <div class="participant-avatar">{{ attendee.initials }}</div>
          <div class="participant-info">
            <p class="participant-name">{{ attendee.name }}</p>
            <p class="participant-sub">{{ attendee.sub }}</p>
          </div>
          <CustomSelect
            v-model="results[attendee.registration_id]"
            :options="resultOptions"
            placeholder="Set result"
            class="result-select-wrap"
          />
        </div>
      </div>

      <div v-if="attendees.length === 0" class="empty-state">
        <p>Nobody has been checked in yet. Mark attendance first.</p>
      </div>

      <div class="event-action-bar">
        <p class="text-note">Students see their result on the event page once published.</p>
        <button class="btn-primary" :disabled="saving || attendees.length === 0" @click="publishResults">
          <Award /> Publish Results
        </button>
      </div>

    </main>

  </div>
</template>

