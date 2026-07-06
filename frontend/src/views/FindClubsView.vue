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
const submittedQuery = ref('')
const matches = ref([])
const resultsSection = ref(null)

const suggestions = [
  'I love building robots and electronics',
  'Photography and film on weekends',
  'Debating, writing, and public speaking',
  'Startups, coding, and product design'
]

function buildResultsDescription(input) {
  const firstWords = input.split(' ').slice(0, 4).join(' ')
  return 'Based on: "' + firstWords + '..."'
}

function useSuggestion(text) {
  interestsText.value = text
  findClubs()
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

  submittedQuery.value = input
  isSearching.value = true
  const matchList = await findMatchingClubs(input)
  isSearching.value = false

  matches.value = attachClubDetails(matchList)
  resultsDesc.value = buildResultsDescription(input)
  showResults.value = true
  interestsText.value = ''

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

    <main class="content-body finder-chat">

      <div class="finder-chat-scroll custom-scrollbar">

        <!-- Empty state: centered intro + quick prompts -->
        <div v-if="!showResults" class="finder-empty">
          <div class="finder-hero-icon">
            <Sparkles />
          </div>
          <p class="finder-hero-title">What are you into?</p>
          <p class="finder-hero-desc">
            Describe your interests in plain language. The AI will match you with clubs
            at your college, including niche ones with no social media presence.
          </p>

          <div class="finder-suggestions">
            <button
              v-for="prompt in suggestions"
              :key="prompt"
              class="finder-suggestion-chip"
              @click="useSuggestion(prompt)"
            >
              <Sparkles /> {{ prompt }}
            </button>
          </div>
        </div>

        <!-- Conversation: user prompt + AI matches -->
        <div v-else class="finder-thread" ref="resultsSection">

          <div class="finder-user-msg">{{ submittedQuery }}</div>

          <div class="finder-assistant">
            <div class="finder-assistant-avatar">
              <Sparkles />
            </div>
            <div class="finder-assistant-body">
              <p class="finder-assistant-intro">
                Here are the clubs that best match your interests
                <span class="finder-assistant-meta">{{ resultsDesc }}</span>
              </p>

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
          </div>

        </div>

      </div>

      <!-- Composer pinned to the bottom, chat style -->
      <div class="finder-composer">
        <div class="finder-composer-inner">
          <textarea
            v-model="interestsText"
            class="finder-composer-input"
            rows="1"
            placeholder="Describe your interests, e.g. electronics, photography, startups..."
            @keydown.enter.exact.prevent="findClubs"
          ></textarea>
          <button
            class="finder-send-btn"
            :disabled="isSearching"
            :aria-label="isSearching ? 'Finding clubs' : 'Find clubs'"
            @click="findClubs"
          >
            <Sparkles />
            <span>{{ isSearching ? 'Finding...' : 'Find' }}</span>
          </button>
        </div>
        <p class="finder-composer-hint">
          AI matches you with clubs at your college — press Enter to search.
        </p>
      </div>

    </main>

  </div>
</template>
