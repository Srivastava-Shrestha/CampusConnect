<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Send } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import LeaderTopNav from '../components/layout/LeaderTopNav.vue'
import { postAnnouncement } from '../api/announcements'
import { useFormValidation } from '../composables/useFormValidation'

const router = useRouter()
const { allFieldsFilled } = useFormValidation()

const clubName = 'Robotics & Automation Club'

const announcementTitle = ref('')
const announcementCategory = ref('')
const announcementBody = ref('')
const isPinned = ref(false)

const categoryOptions = [
  { value: 'general', label: 'General' },
  { value: 'event', label: 'Event Update' },
  { value: 'resource', label: 'Resource / Lab' },
  { value: 'achievement', label: 'Achievement' },
  { value: 'urgent', label: 'Urgent' }
]

const guideSteps = [
  {
    num: '1',
    text: 'Keep the title under 10 words. Members scan titles first before reading the body.'
  },
  {
    num: '2',
    text: 'State the who, what, when, and where in the first two sentences.'
  },
  {
    num: '3',
    text: 'Use the correct category so students can filter by topic in their feed.'
  },
  {
    num: '4',
    text: 'Pin only when the information is time-sensitive. Over-pinning reduces impact.'
  },
  {
    num: '5',
    text: 'All 84 members of your club will see this in their Announcements feed immediately.'
  },
  {
    num: '!',
    text: 'Announcements cannot be edited after posting. Delete and re-post if corrections are needed.',
    warn: true
  }
]

function togglePinned() {
  isPinned.value = !isPinned.value
}

function goBackToFeed() {
  router.push('/leader/announcements')
}

async function handlePostAnnouncement() {
  const fields = {
    title: announcementTitle.value,
    category: announcementCategory.value,
    body: announcementBody.value
  }

  if (!allFieldsFilled(fields)) {
    window.alert('Please fill in all fields before posting.')
    return
  }

  await postAnnouncement({
    title: announcementTitle.value.trim(),
    category: announcementCategory.value,
    body: announcementBody.value.trim(),
    pinned: isPinned.value
  })

  let message = 'Announcement posted to 84 members.'
  if (isPinned.value) {
    message += ' It is pinned at the top of the feed.'
  }

  window.alert(message)
  router.push('/leader/announcements')
}
</script>

<template>
  <StudentSidebar />

  <div class="main-content">
    <LeaderTopNav />

    <header class="topbar">
      <button class="btn-secondary" @click="goBackToFeed">
        <ArrowLeft /> Feed
      </button>
      <div class="title-block">
        <h1 class="page-title">Post Announcement</h1>
        <p class="page-sub">{{ clubName }}</p>
      </div>
      <div class="topbar-spacer"></div>
    </header>

    <main class="content-body custom-scrollbar">

      <div class="form-guide-grid">

        <div class="form-card">
          <p class="form-card-title">Announcement Details</p>

          <div class="form-group">
            <label>Club</label>
            <input type="text" class="input-field" :value="clubName" readonly>
          </div>

          <div class="form-group">
            <label for="ann-title">Title</label>
            <input type="text" id="ann-title" v-model="announcementTitle" class="input-field" placeholder="Short, clear subject line">
          </div>

          <div class="form-group">
            <label for="ann-category">Category</label>
            <select id="ann-category" v-model="announcementCategory" class="select-field">
              <option value="">Select category</option>
              <option v-for="option in categoryOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="ann-body">Message</label>
            <textarea id="ann-body" v-model="announcementBody" class="textarea-field" rows="5" placeholder="Write your announcement here. Be clear and specific so members know exactly what to do or expect."></textarea>
          </div>

          <div class="toggle-row">
            <div class="toggle-label-block">
              <p class="toggle-label">Pin this announcement</p>
              <p class="toggle-desc">Pinned announcements appear at the top of the feed with a highlighted border.</p>
            </div>
            <div class="toggle-switch" :class="{ on: isPinned }" @click="togglePinned"></div>
          </div>

          <button class="btn-primary" @click="handlePostAnnouncement">
            <Send /> Post Announcement
          </button>
        </div>

        <div class="guide-card">
          <p class="guide-card-title">Writing good announcements</p>
          <div v-for="step in guideSteps" :key="step.text" class="guide-step">
            <span class="guide-step-num" :class="{ 'guide-step-warn': step.warn }">{{ step.num }}</span>
            <span>{{ step.text }}</span>
          </div>
        </div>

      </div>

    </main>

  </div>
</template>
