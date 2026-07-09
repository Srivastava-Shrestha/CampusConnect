<script setup>
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { Sparkles, CalendarSearch, Flame } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import ClubCard from '../components/ui/ClubCard.vue'
import EventCard from '../components/ui/EventCard.vue'
import { findMatchingClubs } from '../api/ai'
import { toast } from '../composables/useToast'

const router = useRouter()

const interestsText = ref('')
const isSearching = ref(false)
const showResults = ref(false)
const resultsDesc = ref('Based on your interests')
const submittedQuery = ref('')
const resultKind = ref('clubs')
const resultMessage = ref('')
const matches = ref([])
const resultsSection = ref(null)
const composerInput = ref(null)

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

const COMPOSER_MAX_HEIGHT = 120

function autoGrowComposer() {
  const textarea = composerInput.value
  if (!textarea) return

  textarea.style.height = 'auto'
  textarea.style.height = textarea.scrollHeight + 'px'
  textarea.classList.toggle('is-maxed', textarea.scrollHeight > COMPOSER_MAX_HEIGHT)
}

async function findClubs() {
  const input = interestsText.value.trim()

  if (!input) {
    toast.error('Please describe your interests before searching.')
    return
  }

  submittedQuery.value = input
  isSearching.value = true
  const result = await findMatchingClubs(input)
  isSearching.value = false

  resultKind.value = result.kind
  resultMessage.value = result.message || ''
  matches.value = result.items
  resultsDesc.value = buildResultsDescription(input)
  showResults.value = true
  interestsText.value = ''
  await nextTick()
  autoGrowComposer()

  if (resultsSection.value) {
    resultsSection.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function openClub(clubId) {
  router.push('/clubs/' + clubId)
}

function openEvent(eventId) {
  router.push('/events/' + eventId)
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

              <!-- Direct club matches -->
              <template v-if="resultKind === 'clubs'">
                <p class="finder-assistant-intro">
                  Here are the clubs that best match your interests
                  <span class="finder-assistant-meta">{{ resultsDesc }}</span>
                </p>

                <div class="clubs-grid finder-result-grid">
                  <div v-for="(match, index) in matches" :key="match.id" class="finder-result-item">
                    <ClubCard
                      :club="match"
                      :badge="index === 0 ? 'Top Match' : ''"
                      @open="openClub(match.id)"
                    />
                    <p class="finder-match-note">{{ match.reason }}</p>
                  </div>
                </div>
              </template>

              <!-- No club matched, but a public event did -->
              <template v-else-if="resultKind === 'event_fallback'">
                <div class="finder-fallback-banner">
                  <CalendarSearch />
                  <p>{{ resultMessage }}</p>
                </div>

                <div class="events-grid finder-fallback-events finder-result-grid">
                  <div v-for="ev in matches" :key="ev.id" class="finder-result-item">
                    <EventCard :event="ev" @open="openEvent(ev.id)" />
                    <p class="finder-match-note">{{ ev.reason }}</p>
                  </div>
                </div>
              </template>

              <!-- Nothing matched at all, fall back to the most active clubs -->
              <template v-else>
                <div class="finder-fallback-banner finder-fallback-banner-popular">
                  <Flame />
                  <p>{{ resultMessage }}</p>
                </div>

                <div class="clubs-grid finder-result-grid">
                  <div v-for="match in matches" :key="match.id" class="finder-result-item">
                    <ClubCard :club="match" badge="Popular" @open="openClub(match.id)" />
                    <p class="finder-match-note">{{ match.reason }}</p>
                  </div>
                </div>
              </template>

            </div>
          </div>

        </div>

      </div>

      <!-- Composer pinned to the bottom, chat style -->
      <div class="finder-composer">
        <div class="finder-composer-inner">
          <textarea
            ref="composerInput"
            v-model="interestsText"
            class="finder-composer-input"
            rows="1"
            placeholder="Describe your interests, e.g. electronics, photography, startups..."
            @input="autoGrowComposer"
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
