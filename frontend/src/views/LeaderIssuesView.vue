<script setup>
import { ref, computed, onMounted } from 'vue'
import { CircleDot, Loader, CheckCircle2, MessageSquare, Check, Send, Inbox } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import StatCard from '../components/ui/StatCard.vue'
import FilterChips from '../components/ui/FilterChips.vue'
import { getLeaderIssues, replyToIssue, resolveIssue } from '../api/issues'
import { useAuthStore } from '../stores/auth'
import { toast } from '../composables/useToast'

const auth = useAuthStore()

const issues = ref([])
const activeFilter = ref('all')
const openReplyId = ref(null)
const replyText = ref('')

const filterChips = [
  { id: 'all', label: 'All' },
  { id: 'open', label: 'Open' },
  { id: 'in-progress', label: 'In Progress' },
  { id: 'resolved', label: 'Resolved' }
]

const visibleIssues = computed(function filterIssues() {
  return issues.value.filter(function matchesFilter(issue) {
    if (activeFilter.value === 'all') {
      return true
    }

    return issue.status === activeFilter.value
  })
})

const openCount = computed(function countOpen() {
  return issues.value.filter((issue) => issue.status === 'open').length
})

const inProgressCount = computed(function countInProgress() {
  return issues.value.filter((issue) => issue.status === 'in-progress').length
})

const resolvedCount = computed(function countResolved() {
  return issues.value.filter((issue) => issue.status === 'resolved').length
})

function openReply(issueId) {
  openReplyId.value = issueId
  replyText.value = ''
}

function closeReply() {
  openReplyId.value = null
  replyText.value = ''
}

async function submitReply(issue) {
  const text = replyText.value.trim()

  if (!text) {
    toast.error('Please type a reply before sending.')
    return
  }

  await replyToIssue(issue.id, text)

  issue.response = {
    by: auth.user.name,
    text: text
  }
  issue.status = 'in-progress'
  issue.statusLabel = 'In Progress'

  closeReply()
}

async function markResolved(issue) {
  await resolveIssue(issue.id)

  issue.status = 'resolved'
  issue.statusLabel = 'Resolved'

  if (openReplyId.value === issue.id) {
    closeReply()
  }
}
onMounted(async function loadLeaderIssues() {
  issues.value = await getLeaderIssues()
})
</script>

<template>
  <LeaderSidebar />

  <div class="main-content">

    <Topbar title="Issues" sub="Member concerns raised to Robotics & Automation Club" :show-bell="false" />

    <main class="content-body custom-scrollbar">

      <div class="stats-grid">
        <StatCard :num="openCount" label="Open" :icon="CircleDot" color-class="pink-stat" />
        <StatCard :num="inProgressCount" label="In Progress" :icon="Loader" color-class="blue-stat" />
        <StatCard :num="resolvedCount" label="Resolved" :icon="CheckCircle2" color-class="green-stat" />
      </div>

      <FilterChips :chips="filterChips" v-model="activeFilter" />

      <div>
        <div
          v-for="issue in visibleIssues"
          :key="issue.id"
          class="issue-card"
          :class="{ resolved: issue.status === 'resolved' }"
        >
          <div class="issue-top">
            <p class="issue-title">{{ issue.title }}</p>
            <span class="status-pill" :class="issue.status">{{ issue.statusLabel }}</span>
          </div>

          <p class="issue-meta">
            <strong>{{ issue.raisedBy }}</strong> · {{ issue.meta }}
          </p>

          <p class="issue-desc">{{ issue.desc }}</p>

          <div v-if="issue.response" class="issue-response">
            <p class="issue-response-label">
              <CheckCircle2 />
              Your response · {{ issue.response.by }}
            </p>
            <p class="issue-response-text">{{ issue.response.text }}</p>
          </div>

          <div class="issue-footer">
            <span v-for="tag in issue.tags" :key="tag" class="announce-tag">{{ tag }}</span>
          </div>

          <div v-if="issue.status !== 'resolved'" class="issue-action-row">
            <button class="btn-secondary" @click="openReply(issue.id)">
              <MessageSquare />
              {{ issue.response ? 'Follow Up' : 'Reply' }}
            </button>
            <button class="btn-success" @click="markResolved(issue)">
              <Check /> Mark Resolved
            </button>
          </div>

          <div v-if="openReplyId === issue.id" class="issue-reply-area">
            <textarea
              class="textarea-field"
              v-model="replyText"
              rows="3"
              placeholder="Type your response to the member..."
            ></textarea>
            <div class="issue-action-row">
              <button class="btn-primary" @click="submitReply(issue)">
                <Send /> Send Reply
              </button>
              <button class="btn-secondary" @click="closeReply">Cancel</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="visibleIssues.length === 0" class="empty-state">
        <Inbox />
        <p>No issues match this filter.</p>
      </div>

    </main>

  </div>
</template>
