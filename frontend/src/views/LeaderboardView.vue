<script setup>
import { ref, computed, onMounted } from 'vue'
import { Crown, Trophy } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import FilterChips from '../components/ui/FilterChips.vue'
import { getLeaderboard } from '../api/clubs'

const podium = ref([])
const rows = ref([])
const activeFilter = ref('all')

const filterChips = [
  { id: 'all', label: 'All Categories' },
  { id: 'tech', label: 'Tech' },
  { id: 'culture', label: 'Culture' },
  { id: 'arts', label: 'Arts' },
  { id: 'business', label: 'Business' },
  { id: 'sports', label: 'Sports' }
]

const visiblePodium = computed(function filterPodium() {
  return podium.value.filter(matchesActiveFilter)
})

const visibleRows = computed(function filterRows() {
  return rows.value.filter(matchesActiveFilter)
})

function matchesActiveFilter(entry) {
  return activeFilter.value === 'all' || entry.category === activeFilter.value
}

onMounted(async function loadLeaderboard() {
  const data = await getLeaderboard()
  podium.value = data.podium
  rows.value = data.rows
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content">

    <Topbar title="Leaderboard" sub="Clubs ranked by activity score · June 2026" :show-bell="false" />

    <main class="content-body custom-scrollbar">

      <div class="leaderboard-section">

        <FilterChips :chips="filterChips" v-model="activeFilter" />

        <div>
          <h2 class="clubs-section-title">Top Clubs This Month</h2>
          <div class="podium-container">
            <div
              v-for="entry in visiblePodium"
              :key="entry.rank"
              class="podium-card"
              :class="entry.tier"
            >
              <div v-if="entry.tier === 'gold'" class="podium-crown">
                <Crown />
              </div>
              <p class="podium-rank">{{ entry.rank }}</p>
              <div class="podium-avatar">{{ entry.emoji }}</div>
              <p class="podium-name">{{ entry.name }}</p>
              <p class="podium-score">{{ entry.score }}</p>
              <p class="text-note">pts</p>
            </div>
          </div>
        </div>

        <div>
          <div class="clubs-section-header">
            <h2 class="clubs-section-title">Full Rankings</h2>
            <span class="text-note">{{ visibleRows.length }} clubs ranked</span>
          </div>

          <div class="lb-list">
            <div v-for="row in visibleRows" :key="row.rank" class="lb-row">
              <span class="lb-rank">{{ row.rank }}</span>
              <div class="lb-club-dot" :class="row.dot">{{ row.emoji }}</div>
              <div class="lb-info">
                <p class="lb-club-name">{{ row.name }}</p>
                <p class="lb-club-cat">{{ row.cat }}</p>
              </div>
              <div class="lb-score-col">
                <p class="lb-score">{{ row.score }}</p>
                <p class="lb-score-label">pts</p>
              </div>
            </div>
          </div>

          <div v-if="visibleRows.length === 0" class="empty-state">
            <Trophy />
            <p>No clubs in this category yet.</p>
          </div>
        </div>

        <div class="club-profile-meta">
          <p class="section-heading">How is the score calculated?</p>
          <p class="body-text">Activity score is calculated from the total number of events held (40 pts each), member count growth (5 pts per new member), average attendance rate (up to 200 pts bonus), and issues resolved (10 pts each). Scores reset on the first of each month.</p>
        </div>

      </div>

    </main>

  </div>
</template>
