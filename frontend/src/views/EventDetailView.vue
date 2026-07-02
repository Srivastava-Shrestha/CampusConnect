<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Calendar, Clock, MapPin, Users, Tag, CheckCircle2, Award } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import { useEventsStore } from '../stores/events'
import { registerForEvent } from '../api/events'

const route = useRoute()
const router = useRouter()
const eventsStore = useEventsStore()

const isRegistered = ref(false)
const registrationId = ref('')

const event = computed(() => eventsStore.currentEvent)

const seatsRemaining = computed(function calcSeats() {
  if (!event.value) return 0
  return event.value.capacity - event.value.registered
})

async function handleRegister() {
  const result = await registerForEvent(route.params.id)
  registrationId.value = result.registrationId || 'CC-2026-0482'
  isRegistered.value = true
}

function goBackToEvents() {
  router.push('/events')
}

onMounted(function loadDetail() {
  eventsStore.loadEvent(route.params.id)
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content" v-if="event">

    <header class="topbar">
      <button class="btn-secondary" @click="goBackToEvents">
        <ArrowLeft /> Events
      </button>

      <div class="title-block">
        <h1 class="page-title">Event Detail</h1>
        <p class="page-sub">{{ event.club }}</p>
      </div>

      <div class="topbar-spacer"></div>
    </header>

    <main class="content-body custom-scrollbar">

      <div>
        <div class="event-hero-banner" :class="event.accent">
          <div class="club-card-circle-1"></div>
          <div class="club-card-circle-2"></div>
          <div class="club-card-circle-3"></div>
          <div class="event-hero-overlay"></div>
          <div class="event-hero-text">
            <p class="event-hero-title">{{ event.title }}</p>
            <p class="event-hero-sub">{{ event.club }} · {{ event.month }} {{ event.day }}, 2026</p>
          </div>
        </div>

        <div class="club-profile-meta">
          <div class="event-detail-grid">

            <div>
              <p class="section-heading">About this Event</p>
              <p class="body-text">{{ event.about || 'Details for this event will be shared by the club soon.' }}</p>

              <div class="event-meta-list mt-20">
                <div class="event-meta-item">
                  <Calendar />
                  <span><span class="event-meta-label">Date</span> &nbsp; {{ event.dateLong || (event.day + ' ' + event.month + ' 2026') }}</span>
                </div>
                <div class="event-meta-item">
                  <Clock />
                  <span><span class="event-meta-label">Time</span> &nbsp; {{ event.timeLong || event.time }}</span>
                </div>
                <div class="event-meta-item">
                  <MapPin />
                  <span><span class="event-meta-label">Venue</span> &nbsp; {{ event.venueLong || event.venue }}</span>
                </div>
                <div class="event-meta-item">
                  <Users />
                  <span><span class="event-meta-label">Capacity</span> &nbsp; {{ event.capacity }} participants ({{ event.registered }} registered)</span>
                </div>
                <div class="event-meta-item">
                  <Tag />
                  <span><span class="event-meta-label">Type</span> &nbsp; {{ event.type || 'Event' }}</span>
                </div>
              </div>
            </div>

            <div class="reg-panel">

              <div v-if="!isRegistered">
                <p class="reg-panel-title">Register for this Event</p>
                <div class="reg-capacity-row">
                  <span>Seats remaining</span>
                  <span class="reg-capacity-num">{{ seatsRemaining }}</span>
                </div>
                <p class="text-note">{{ event.closesNote || 'Registration closes the day before the event.' }}</p>
                <button class="btn-auth-submit" @click="handleRegister">
                  <CheckCircle2 /> Register Now
                </button>
              </div>

              <div v-else>
                <p class="reg-panel-title">You are Registered!</p>
                <div class="reg-id-box">
                  <p class="reg-id-label">Registration ID</p>
                  <p class="reg-id-value">{{ registrationId }}</p>
                </div>
                <p class="text-note">Show this ID at the event gate. You will receive a confirmation on your registered email.</p>

                <div v-if="event.status === 'past'">
                  <p class="reg-panel-title">Your Result</p>
                  <div class="result-badge participant">
                    <Award /> Participant
                  </div>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>

    </main>

  </div>
</template>
