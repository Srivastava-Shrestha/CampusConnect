<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { ArrowLeft, Send, Save } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import { createEvent, publishEvent } from '../api/events'
import { useClubsStore } from '../stores/clubs'
import { toast } from '../composables/useToast'
import { useFormValidation } from '../composables/useFormValidation'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const clubsStore = useClubsStore()
const { allFieldsFilled } = useFormValidation()

const club = ref(null)
const saving = ref(false)

const eventTitle = ref('')
const eventDesc = ref('')
const eventDate = ref('')
const eventCapacity = ref('')
const eventStart = ref('')
const eventEnd = ref('')
const eventVenue = ref('')

const guideSteps = [
  {
    num: '1',
    text: 'Fill in all fields. A clear description gets better registrations.'
  },
  {
    num: '2',
    text: 'Capacity is optional. Leave it empty to accept unlimited registrations.'
  },
  {
    num: '3',
    text: 'Save as draft to keep working on it. Only you and your co-leaders can see a draft.'
  },
  {
    num: '4',
    text: 'Publishing opens registration to every approved member of your club.'
  },
  {
    num: '5',
    text: 'On the day, use the Attendance page to mark who showed up, then set results.'
  },
  {
    num: '!',
    text: 'An event starting in the past cannot be published, and a cancelled event cannot be edited.',
    warn: true
  }
]

function goBackToEvents() {
  router.push(`/${route.params.slug}/leader/events`)
}

// <input type="date"> and <input type="time"> give local wall-clock values; the API
// wants one ISO instant per boundary.
function toIsoInstant(date, time) {
  return new Date(`${date}T${time}`).toISOString()
}

function buildPayload() {
  if (!club.value) {
    toast.error('No club selected.')
    return null
  }
  const requiredFields = {
    title: eventTitle.value,
    desc: eventDesc.value,
    date: eventDate.value,
    start: eventStart.value,
    end: eventEnd.value,
    venue: eventVenue.value
  }

  if (!allFieldsFilled(requiredFields)) {
    toast.error('Please fill in all required fields.')
    return null
  }

  const startsAt = toIsoInstant(eventDate.value, eventStart.value)
  if (new Date(startsAt) <= new Date()) {
  toast.error('The event must start in the future.')
  return null
  }
  const endsAt = toIsoInstant(eventDate.value, eventEnd.value)

  if (endsAt <= startsAt) {
    toast.error('The end time must be after the start time.')
    return null
  }
  const capacity =
  eventCapacity.value === ''
    ? null
    : Number(eventCapacity.value)

  if (capacity !== null && (!Number.isInteger(capacity) || capacity < 1)) {
    toast.error('Capacity must be at least 1.')
    return null
}
  return {
    club_id: club.value.id,
    title: eventTitle.value.trim(),
    description: eventDesc.value.trim(),
    venue: eventVenue.value.trim(),
    starts_at: startsAt,
    ends_at: endsAt,
    capacity
  }
}

async function saveDraft() {
  const payload = buildPayload()
  if (!payload) return

  saving.value = true

  try {
    const created = await createEvent(payload)
    toast.success(`"${created.title}" saved as a draft.`)
    router.push(`/${route.params.slug}/leader/events`)
  } catch (error) {
    toast.error(error?.message || 'Unable to create event.')
  } finally {
    saving.value = false
  }
}

async function publishNewEvent() {
  const payload = buildPayload()
  if (!payload) return

  saving.value = true

  try {
    const created = await createEvent(payload)

    try {
      await publishEvent(created.id)
      toast.success('Event published! Members can now register.')
    } catch (error) {
      // The event exists as a draft either way, so say that instead of looking like a total failure.
      toast.error(`Event was saved as a draft, but publishing failed: ${error?.message || 'Unknown error.'}`
)
    }

    router.push(`/${route.params.slug}/leader/events`)
  } catch (error) {
    toast.error(error?.message || 'Unable to create event.')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    await clubsStore.loadLeaderClubs()

    if (!clubsStore.selectedLeaderClub) {
      toast.error('No active club selected.')
      router.push(`/${auth.user.collegeSlug}/clubs`)
      return
    }

    club.value = clubsStore.selectedLeaderClub

  } catch (error) {
    toast.error(error?.message || 'Unable to load your club.')
    router.push(`/${auth.user.collegeSlug}/clubs`)
  }
})
</script>

<template>
  <LeaderSidebar />

  <div class="main-content">

    <header class="topbar">
      <button class="btn-secondary" @click="goBackToEvents">
        <ArrowLeft /> Events
      </button>
      <div class="title-block">
        <h1 class="page-title">Create a New Event</h1>
        <p class="page-sub">{{ club ? club.name : 'Loading your club...' }}</p>
      </div>
      <div class="topbar-spacer"></div>
    </header>

    <main class="content-body custom-scrollbar">

      <div class="form-guide-grid">

        <div class="form-card">
          <p class="form-card-title">Event Details</p>

          <div class="form-group">
            <label for="event-title">Event Title</label>
            <input type="text" id="event-title" v-model="eventTitle" class="input-field" placeholder="e.g. Automation Hackathon 2026">
          </div>

          <div class="form-group">
            <label for="event-desc">Description</label>
            <textarea id="event-desc" v-model="eventDesc" class="textarea-field" rows="4" placeholder="What will happen at this event? What should attendees bring or prepare?"></textarea>
          </div>

          <div class="grid-2-tight">
            <div class="form-group">
              <label for="event-date">Date</label>
              <input type="date" id="event-date" v-model="eventDate" class="input-field">
            </div>
            <div class="form-group">
              <label for="event-capacity">Max Participants (optional)</label>
              <input type="number" id="event-capacity" v-model="eventCapacity" class="input-field" placeholder="Leave empty for unlimited" min="1">
            </div>
          </div>

          <div class="grid-2-tight">
            <div class="form-group">
              <label for="event-start">Start Time</label>
              <input type="time" id="event-start" v-model="eventStart" class="input-field">
            </div>
            <div class="form-group">
              <label for="event-end">End Time</label>
              <input type="time" id="event-end" v-model="eventEnd" class="input-field">
            </div>
          </div>

          <div class="form-group">
            <label for="event-venue">Venue</label>
            <input type="text" id="event-venue" v-model="eventVenue" class="input-field" placeholder="e.g. Seminar Hall, Block A">
          </div>

          <div class="event-action-bar">
            <button class="btn-secondary" :disabled="saving || !club" @click="saveDraft">
              <Save /> Save as Draft
            </button>
            <button class="btn-primary" :disabled="saving || !club" @click="publishNewEvent">
              <Send /> Publish Event
            </button>
          </div>
        </div>

        <div class="guide-card">
          <p class="guide-card-title">Publishing checklist</p>
          <div v-for="step in guideSteps" :key="step.text" class="guide-step">
            <span class="guide-step-num" :class="{ 'guide-step-warn': step.warn }">{{ step.num }}</span>
            <span>{{ step.text }}</span>
          </div>
        </div>

      </div>

    </main>

  </div>
</template>