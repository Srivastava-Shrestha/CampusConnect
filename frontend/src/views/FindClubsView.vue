<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Sparkles } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import ClubCard from '../components/ui/ClubCard.vue'
import { findMatchingClubs } from '../api/ai'
import { mockClubs } from '../api/clubs'

const router = useRouter()

const interestsText = ref('')
const isSearching = ref(false)
const showResults = ref(false)
const resultsDesc = ref('Based on your interests')
const matches = ref([])
const resultsSection = ref(null)

function buildResultsDescription(input) {
  const firstWords = input.split(' ').slice(0, 4).join(' ')
  return 'Based on: "' + firstWords + '..."'
}

function attachClubDetails(matchList) {
  return matchList.map(function combineWithClub(match) {
    const club = mockClubs.find((item) => item.name === match.name)
    return { ...club, reason: match.reason }
  })
}

async function findClubs() {
  const input = interestsText.value.trim()

  if (!input) {
    window.alert('Please describe your interests before searching.')
    return
  }

  isSearching.value = true
  const matchList = await findMatchingClubs(input)
  isSearching.value = false

  matches.value = attachClubDetails(matchList)
  resultsDesc.value = buildResultsDescription(input)
  showResults.value = true

  if (resultsSection.value) {
    resultsSection.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function openClub(clubId) {
  router.push('/clubs/' + clubId)
}
</script>

<template>
  <StudentSidebar />

  <div class="main-content">

    <Topbar title="AI Club Finder" sub="Describe your interests and find clubs that match" :show-bell="false" />

    <main class="content-body custom-scrollbar">

      <div class="finder-hero">
        <div class="finder-hero-icon">
          <Sparkles />
        </div>

        <p class="finder-hero-title">What are you into?</p>
        <p class="finder-hero-desc">
          Describe your interests in plain language. The AI will match you with clubs at your college,
          including niche ones that have no social media presence.
        </p>

        <textarea
          v-model="interestsText"
          class="finder-textarea"
          placeholder="e.g. I love building things with electronics, enjoy photography on weekends, and want to meet people who care about startups..."
        ></textarea>

        <button class="btn-primary" :disabled="isSearching" @click="findClubs">
          <template v-if="isSearching">Finding clubs...</template>
          <template v-else><Sparkles /> Find Clubs</template>
        </button>
      </div>

      <div class="finder-results" :class="{ visible: showResults }" ref="resultsSection">

        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Clubs matched for you</h2>
          <span class="clubs-count-text">{{ resultsDesc }}</span>
        </div>

        <div class="clubs-grid">
          <div v-for="(match, index) in matches" :key="match.id">
            <ClubCard
              :club="match"
              :badge="index === 0 ? 'Top Match' : ''"
              @open="openClub(match.id)"
            />
            <p class="finder-match-note">{{ match.reason }}</p>
          </div>
        </div>

      </div>

    </main>

  </div>
</template>
