<script setup>
import { ref, onMounted, computed } from 'vue'
import { Award, CalendarClock } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import CertCard from '../components/ui/CertCard.vue'
import { useAuthStore } from '../stores/auth'
import { getMyCertificates } from '../api/certificates'
import { getMyRegistrations } from '../api/events'
import { getMyProfile } from '../api/students'
import { toast } from '../composables/useToast'
import { cachedFetch } from '../utils/apiCache'

// Logging out lives once, in the sidebar - this page used to have its own
// second button, which meant two logout controls were visible at once
// whenever this page was open. See issue #46.
const auth = useAuthStore()

const certificates = ref([])
const clubCount = ref(0)

// Interests picked at onboarding, shown as tags on the profile header. Was
// always an empty array before - nothing ever populated it.
const profileTags = ref([])

const profileStats = computed(() => [
  { num: clubCount.value, label: 'Clubs' },
  { num: eventHistory.value.length, label: 'Events' },
  { num: certificates.value.length, label: 'Certs' }
])

const eventHistory = ref([])

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const resultLabels = {
  WINNER: 'Winner',
  RUNNER_UP: 'Runner-up',
  PARTICIPANT: 'Participant'
}

const resultClasses = {
  WINNER: 'winner',
  RUNNER_UP: 'runner-up',
  PARTICIPANT: 'participant'
}

// A registration only carries a real outcome once the leader has checked the student
// in and set a result; until then it is still just a sign-up.
function toHistoryEntry(registration) {
  const startsAt = new Date(registration.starts_at)

  return {
    id: registration.registration_id,
    day: String(startsAt.getDate()),
    month: MONTHS[startsAt.getMonth()],
    title: registration.event_title,
    club: registration.club_name,
    result: registration.result === 'REGISTRANT' ? null : registration.result
  }
}

onMounted(async function loadProfile() {
  try {
    const profile = await cachedFetch('my-profile', getMyProfile)

    profileTags.value = profile.interests || []
    clubCount.value = profile.joined_clubs ? profile.joined_clubs.length : 0
  } catch (error) {
    console.error(error)
  }

  try {
    certificates.value = await cachedFetch('my-certificates', getMyCertificates)
  } catch (error) {
    console.error(error)
    certificates.value = []
  }

  try {
    const registrations = await cachedFetch('my-registrations', getMyRegistrations)

    eventHistory.value = registrations.map(toHistoryEntry)
  } catch (error) {
    console.error(error)
    eventHistory.value = []
  }
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content">

    <Topbar title="My Profile" sub="Certificates, results, and activity" :show-bell="false" />

    <main class="content-body custom-scrollbar">

      <div class="profile-hero">
        <div class="profile-avatar-lg">{{ auth.user.initials }}</div>
        <div class="profile-hero-info">
          <p class="profile-name">{{ auth.user.name }}</p>
          <div v-if="profileTags.length" class="profile-tags">
            <span v-for="tag in profileTags" :key="tag" class="profile-tag">{{ tag }}</span>
          </div>
        </div>
        <div class="profile-hero-stats">
          <div v-for="stat in profileStats" :key="stat.label" class="profile-stat">
            <p class="profile-stat-num">{{ stat.num }}</p>
            <p class="profile-stat-label">{{ stat.label }}</p>
          </div>
        </div>
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Certificates Earned</h2>
          <router-link to="/verify/lookup" class="clubs-section-link">
            Verify a certificate
          </router-link>
        </div>

        <div v-if="certificates.length === 0" class="empty-state empty-state-wide">
          <Award />
          <p>No certificates yet. Winning or participating in an event earns you one automatically.</p>
        </div>

        <div v-else class="cert-grid">
          <CertCard
            v-for="cert in certificates"
            :key="cert.serial"
            :cert="cert"
          />
        </div>
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Event History</h2>
          <span class="clubs-count-text">{{ eventHistory.length }} events</span>
        </div>

        <div v-if="eventHistory.length === 0" class="empty-state empty-state-wide">
          <CalendarClock />
          <p>No events yet. Registered events will show up here once you sign up for one.</p>
        </div>

        <div v-else class="announce-feed">
          <div v-for="entry in eventHistory" :key="entry.id" class="event-history-row">
            <div class="event-history-date">
              <span class="event-history-day">{{ entry.day }}</span>
              <span class="event-history-month">{{ entry.month }}</span>
            </div>
            <div class="event-history-info">
              <p class="event-history-title">{{ entry.title }}</p>
              <p class="event-history-club">{{ entry.club }}</p>
            </div>
            <span v-if="!entry.result" class="event-status registered">Registered</span>
            <div v-else class="result-badge" :class="resultClasses[entry.result]">
              <Award /> {{ resultLabels[entry.result] }}
            </div>
          </div>
        </div>
      </div>

    </main>

  </div>
</template>
