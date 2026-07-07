<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Send } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import LeaderTopNav from '../components/layout/LeaderTopNav.vue'
import { createEvent } from '../api/events'
import { useFormValidation } from '../composables/useFormValidation'

const router = useRouter()
const { allFieldsFilled } = useFormValidation()

const eventTitle = ref('')
const eventType = ref('')
const eventDesc = ref('')
const eventDate = ref('')
const eventCapacity = ref('')
const eventStart = ref('')
const eventEnd = ref('')
const eventVenue = ref('')

const typeOptions = ['Workshop', 'Hackathon', 'Competition', 'Social / Open Mic', 'Talk / Seminar', 'Other']

const guideSteps = [
  {
    num: '1',
    text: 'Fill in all fields. A clear description gets better registrations.'
  },
  {
    num: '2',
    text: 'Set a realistic capacity. Registered students receive a confirmation ID.'
  },
  {
    num: '3',
    text: 'Once published, all members of your club can see and register for the event.'
  },
  {
    num: '4',
    text: 'On the day, use the Attendance page to mark who actually showed up.'
  },
  {
    num: '5',
    text: 'After the event, set results. Certificates are auto-generated for all attendees.'
  },
  {
    num: '!',
    text: 'You can edit or cancel the event anytime before it starts.',
    warn: true
  }
]

function goBackToEvents() {
  router.push('/leader/events')
}

async function publishEvent() {
  const requiredFields = {
    title: eventTitle.value,
    type: eventType.value,
    desc: eventDesc.value,
    date: eventDate.value,
    capacity: eventCapacity.value,
    venue: eventVenue.value
  }

  if (!allFieldsFilled(requiredFields)) {
    window.alert('Please fill in all required fields before publishing.')
    return
  }

  await createEvent({
    title: eventTitle.value.trim(),
    type: eventType.value,
    desc: eventDesc.value.trim(),
    date: eventDate.value,
    capacity: eventCapacity.value,
    start: eventStart.value,
    end: eventEnd.value,
    venue: eventVenue.value.trim()
  })

  window.alert('Event published! Members can now register.')
  router.push('/leader/events')
}
</script>

<template>
  <StudentSidebar />

  <div class="main-content">
    <LeaderTopNav />

    <header class="topbar">
      <button class="btn-secondary" @click="goBackToEvents">
        <ArrowLeft /> Events
      </button>
      <div class="title-block">
        <h1 class="page-title">Create a New Event</h1>
        <p class="page-sub">Robotics & Automation Club</p>
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
            <label for="event-type">Event Type</label>
            <select id="event-type" v-model="eventType" class="select-field">
              <option value="">Select type</option>
              <option v-for="option in typeOptions" :key="option" :value="option">{{ option }}</option>
            </select>
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
              <label for="event-capacity">Max Participants</label>
              <input type="number" id="event-capacity" v-model="eventCapacity" class="input-field" placeholder="80" min="1">
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

          <button class="btn-primary" @click="publishEvent">
            <Send /> Publish Event
          </button>
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
