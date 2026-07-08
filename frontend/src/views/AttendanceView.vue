<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, CheckCheck, Save } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import LeaderTopNav from '../components/layout/LeaderTopNav.vue'
import { getEventParticipants, getEventById, saveAttendance } from '../api/events'
import { toast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()

const event = ref(null)
const participants = ref([])
const presentIds = ref([])

const presentCount = computed(() => presentIds.value.length)

function togglePresent(participantId) {
  if (presentIds.value.includes(participantId)) {
    presentIds.value = presentIds.value.filter((id) => id !== participantId)
  } else {
    presentIds.value.push(participantId)
  }
}

function markAllPresent() {
  presentIds.value = participants.value.map((participant) => participant.id)
}

async function submitAttendance() {
  if (presentCount.value === 0) {
    toast.error('Please mark at least one participant as present.')
    return
  }

  await saveAttendance(route.params.id, presentIds.value)
  toast.success('Attendance saved for ' + presentCount.value + ' participants. Now set results on the Results page.')
  router.push('/leader/events/' + route.params.id + '/results')
}

function goBackToEvents() {
  router.push('/leader/events')
}

onMounted(async function loadAttendancePage() {
  event.value = await getEventById(route.params.id)
  participants.value = await getEventParticipants(route.params.id)
})
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
        <h1 class="page-title">Mark Attendance</h1>
        <p class="page-sub" v-if="event">{{ event.title }} · {{ event.day }} {{ event.month }} 2026</p>
      </div>
      <div class="topbar-spacer"></div>
      <button class="btn-secondary" @click="markAllPresent">
        <CheckCheck /> Mark All Present
      </button>
    </header>

    <main class="content-body custom-scrollbar">

      <div class="club-profile-meta">
        <p class="section-heading">Registered Participants</p>
        <p class="text-note" v-if="event">{{ event.registered }} registered · Check each student who was physically present at the event.</p>
      </div>

      <div class="participant-list mt-16">
        <div v-for="participant in participants" :key="participant.id" class="participant-row">
          <input
            type="checkbox"
            class="attend-checkbox"
            :id="'att-' + participant.id"
            :checked="presentIds.includes(participant.id)"
            @change="togglePresent(participant.id)"
          >
          <label :for="'att-' + participant.id" class="participant-avatar">{{ participant.initials }}</label>
          <div class="participant-info">
            <p class="participant-name">{{ participant.name }}</p>
            <p class="participant-sub">{{ participant.sub }} · {{ participant.regId }}</p>
          </div>
        </div>
      </div>

      <div class="event-action-bar">
        <p class="text-note">{{ presentCount }} of {{ participants.length }} marked present</p>
        <button class="btn-primary" @click="submitAttendance">
          <Save /> Save Attendance
        </button>
      </div>

    </main>

  </div>
</template>
