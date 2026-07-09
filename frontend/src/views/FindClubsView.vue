<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Sparkles, CalendarSearch, Flame, Play, Pause, Volume2, Trash2 } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import ClubCard from '../components/ui/ClubCard.vue'
import EventCard from '../components/ui/EventCard.vue'
import { findMatchingClubs } from '../api/ai'
import { toast } from '../composables/useToast'
import { renderMarkdown, stripMarkdown } from '../utils/markdown'
import { useNarrator } from '../composables/useNarrator'

const STORAGE_KEY = 'cc_finder_conversation'

const router = useRouter()
const narrator = useNarrator()

const interestsText = ref('')
const isSearching = ref(false)
const composerInput = ref(null)
const scrollArea = ref(null)

// The whole session's chat: each turn is one user prompt plus the assistant's
// answer (message + cards). New prompts append here instead of replacing, and
// the array is mirrored to sessionStorage so the history survives navigating
// away and back within the same tab.
const conversation = ref(loadConversation())

// Which turn the narrator is currently reading, so each turn's Listen button
// reflects its own state.
const activeNarrationId = ref(null)

function loadConversation() {
  try {
    const saved = sessionStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved) : []
  } catch (error) {
    return []
  }
}

watch(conversation, function persist(turns) {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(turns))
  } catch (error) {
    // sessionStorage can be unavailable (private mode / quota) - the chat
    // still works in-memory, it just will not persist.
  }
}, { deep: true })

// When narration ends on its own, drop the active-turn highlight.
watch(() => narrator.isSpeaking.value, function onSpeakingChange(speaking) {
  if (!speaking) activeNarrationId.value = null
})

const hasHistory = computed(function checkHistory() {
  return conversation.value.length > 0
})

const suggestions = [
  'I love building robots and electronics',
  'Photography and film on weekends',
  'Debating, writing, and public speaking',
  'Startups, coding, and product design'
]

// Quick follow-up replies shown under the latest answer. One tap sends the
// message so the student can keep the conversation going without typing.
const followUpsByKind = {
  clubs: [
    'Show me a few more clubs like these',
    'Any events I could go to?',
    'Something more creative'
  ],
  event_fallback: [
    'Show me clubs instead',
    'Any tech or coding options?',
    'Something more hands-on'
  ],
  popularity: [
    'I am into arts and culture',
    'Show me tech and coding clubs',
    'Any events happening soon?'
  ]
}

const latestFollowUps = computed(function currentFollowUps() {
  if (!hasHistory.value) return []
  const lastKind = conversation.value[conversation.value.length - 1].kind
  return followUpsByKind[lastKind] || followUpsByKind.clubs
})

function renderTurnMessage(turn) {
  const fallback = 'Here are the clubs that best match your interests.'
  return renderMarkdown(turn.message || fallback)
}

function narrateLabel(turn) {
  if (activeNarrationId.value !== turn.id || !narrator.isSpeaking.value) return 'Listen'
  return narrator.isPaused.value ? 'Resume' : 'Pause'
}

function isNarrating(turn) {
  return activeNarrationId.value === turn.id && narrator.isSpeaking.value
}

function narrateTurn(turn) {
  if (activeNarrationId.value === turn.id) {
    // Same turn - toggle pause / resume (or restart if it had finished).
    narrator.toggle(stripMarkdown(turn.message))
    return
  }
  // A different turn - start reading this one from the top.
  narrator.speak(stripMarkdown(turn.message))
  activeNarrationId.value = turn.id
}

function useSuggestion(text) {
  interestsText.value = text
  findClubs()
}

function sendFollowUp(text) {
  interestsText.value = text
  findClubs()
}

function clearConversation() {
  narrator.stop()
  conversation.value = []
  activeNarrationId.value = null
}

const COMPOSER_MAX_HEIGHT = 120

function autoGrowComposer() {
  const textarea = composerInput.value
  if (!textarea) return

  textarea.style.height = 'auto'
  textarea.style.height = textarea.scrollHeight + 'px'
  textarea.classList.toggle('is-maxed', textarea.scrollHeight > COMPOSER_MAX_HEIGHT)
}

function scrollToBottom() {
  const area = scrollArea.value
  if (area) area.scrollTop = area.scrollHeight
}

let nextTurnId = Date.now()

async function findClubs() {
  const input = interestsText.value.trim()

  if (!input) {
    toast.error('Please describe your interests before searching.')
    return
  }

  narrator.stop()
  isSearching.value = true
  interestsText.value = ''
  await nextTick()
  autoGrowComposer()

  const result = await findMatchingClubs(input)
  isSearching.value = false

  nextTurnId += 1
  conversation.value.push({
    id: nextTurnId,
    query: input,
    kind: result.kind,
    message: result.message || '',
    items: result.items
  })

  await nextTick()
  scrollToBottom()
}

onMounted(function scrollOnReturn() {
  if (hasHistory.value) nextTick(scrollToBottom)
})

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

      <div class="finder-chat-scroll custom-scrollbar" ref="scrollArea">

        <!-- Empty state: centered intro + quick prompts -->
        <div v-if="!hasHistory" class="finder-empty">
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

        <!-- Conversation: every turn stacked, oldest first -->
        <div v-else class="finder-thread">

          <div class="finder-thread-bar">
            <button class="finder-clear-btn" @click="clearConversation">
              <Trash2 /> Clear chat
            </button>
          </div>

          <div v-for="turn in conversation" :key="turn.id" class="finder-turn">

            <div class="finder-user-msg">{{ turn.query }}</div>

            <div class="finder-assistant">
              <div class="finder-assistant-avatar">
                <Sparkles />
              </div>
              <div class="finder-assistant-body">

                <!-- Conversational reply (Markdown), same for every result kind -->
                <div class="finder-msg-bubble">
                  <span v-if="turn.kind === 'event_fallback'" class="finder-msg-tag">
                    <CalendarSearch /> Event suggestion
                  </span>
                  <span v-else-if="turn.kind === 'popularity'" class="finder-msg-tag">
                    <Flame /> Popular on campus
                  </span>

                  <div class="finder-msg-md" v-html="renderTurnMessage(turn)"></div>

                  <button
                    v-if="narrator.isSupported.value"
                    class="finder-narrate-btn"
                    :class="{ 'is-active': isNarrating(turn) }"
                    :aria-label="narrateLabel(turn)"
                    @click="narrateTurn(turn)"
                  >
                    <Pause v-if="isNarrating(turn) && !narrator.isPaused.value" />
                    <Play v-else-if="isNarrating(turn) && narrator.isPaused.value" />
                    <Volume2 v-else />
                    <span>{{ narrateLabel(turn) }}</span>
                  </button>
                </div>

                <!-- Public events -->
                <div
                  v-if="turn.kind === 'event_fallback'"
                  class="events-grid finder-fallback-events finder-result-grid"
                >
                  <div v-for="ev in turn.items" :key="ev.id" class="finder-result-item">
                    <EventCard :event="ev" @open="openEvent(ev.id)" />
                  </div>
                </div>

                <!-- Clubs (direct matches or popularity fallback) -->
                <div v-else class="clubs-grid finder-result-grid">
                  <div v-for="(match, index) in turn.items" :key="match.id" class="finder-result-item">
                    <ClubCard
                      :club="match"
                      :badge="turn.kind === 'popularity' ? 'Popular' : (index === 0 ? 'Top Match' : '')"
                      @open="openClub(match.id)"
                    />
                  </div>
                </div>

              </div>
            </div>
          </div>

          <!-- Quick follow-up replies for the latest answer only -->
          <div v-if="latestFollowUps.length" class="finder-followups">
            <button
              v-for="chip in latestFollowUps"
              :key="chip"
              class="finder-followup-chip"
              :disabled="isSearching"
              @click="sendFollowUp(chip)"
            >
              {{ chip }}
            </button>
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
