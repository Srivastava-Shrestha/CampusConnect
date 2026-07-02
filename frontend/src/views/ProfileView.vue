<script setup>
import { ref, onMounted } from 'vue'
import { ExternalLink, Award } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import CertCard from '../components/ui/CertCard.vue'
import { useAuthStore } from '../stores/auth'
import { getMyCertificates } from '../api/certificates'

const auth = useAuthStore()

const certificates = ref([])

const profileTags = ['Computer Science', '1st Year', 'KNIT Sultanpur', 'Joined Jun 2026']

const profileStats = [
  { num: 3, label: 'Clubs' },
  { num: 5, label: 'Events' },
  { num: 2, label: 'Certs' }
]

const eventHistory = [
  { id: 1, day: '8', month: 'Jul', title: 'Photography Walk: Old City', club: 'Photography Circle', result: 'participant' },
  { id: 2, day: '10', month: 'Jul', title: 'Open Mic Night', club: 'Music Collective', result: 'registered' },
  { id: 3, day: '15', month: 'Mar', title: 'Open Mic Night, Spring Edition', club: 'Music Collective', result: 'participant' },
  { id: 4, day: '2', month: 'Feb', title: 'Robot Line Follower Workshop', club: 'Robotics & Automation Club', result: 'participant' },
  { id: 5, day: '20', month: 'Jan', title: 'Freshers Welcome Hack', club: 'Coding Society', result: 'participant' }
]

onMounted(async function loadCertificates() {
  certificates.value = await getMyCertificates()
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
          <div class="profile-tags">
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
            <ExternalLink /> Verify a certificate
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
          <span class="clubs-count-text">{{ eventHistory.length }} events attended</span>
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
            <span v-if="entry.result === 'registered'" class="event-status registered">Registered</span>
            <div v-else class="result-badge participant">
              <Award /> Participant
            </div>
          </div>
        </div>
      </div>

    </main>

  </div>
</template>
