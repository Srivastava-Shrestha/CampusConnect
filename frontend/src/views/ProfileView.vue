<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Award, LogOut } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import CertCard from '../components/ui/CertCard.vue'
import { useAuthStore } from '../stores/auth'
import { getMyCertificates } from '../api/certificates'
import { getMyRegistrations } from '../api/events'
import { toast } from '../composables/useToast'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  const slug = auth.user.collegeSlug

  auth.logout()

  router.push(`/${slug}/login`)
}

const certificates = ref([])

const profileTags = ref([])

const profileStats = computed(() => [
  { num: '-', label: 'Clubs' },
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
    certificates.value = await getMyCertificates()
  } catch (error) {
    console.error(error)
    certificates.value = []
  }

  try {
    const registrations = await getMyRegistrations()

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
        <button class="btn-secondary-sm profile-logout-btn" @click="handleLogout">
          <LogOut /> Log out
        </button>
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Certificates Earned</h2>
          <router-link to="/verify/lookup" class="clubs-section-link">
            Verify a certificate
          </router-link>
        </div>

        <div class="cert-grid">
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

        <div class="announce-feed">
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

<style scoped>
.profile-logout-btn {
  gap: 6px;
  color: var(--color-pink-text, #ab3a50);
  align-self: center;
}

.profile-logout-btn svg {
  width: 18px;
  height: 18px;
}
</style>