<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Send } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import { createClub } from '../api/clubs'
import { useFormValidation } from '../composables/useFormValidation'

const router = useRouter()
const { allFieldsFilled, isValidEmail } = useFormValidation()

const clubName = ref('')
const clubCategory = ref('')
const clubTagline = ref('')
const clubAbout = ref('')
const clubEmail = ref('')

const categoryOptions = [
  'Tech',
  'Arts',
  'Culture',
  'Sports',
  'Music',
  'Business',
  'Science',
  'Other'
]

const guideSteps = [
  {
    num: '1',
    text: 'Fill in your club details and submit this form.'
  },
  {
    num: '2',
    text: 'Your request goes to the Campus Council Admin for review.'
  },
  {
    num: '3',
    text: 'Admin approves or rejects within 2 to 3 working days and provides a written reason.'
  },
  {
    num: '4',
    text: 'Once approved, your club appears in the directory and students can request to join.'
  },
  {
    num: '!',
    text: 'Make sure your college email address is verified before submitting.',
    warn: true
  }
]

function goBack() {
  router.back()
}

async function handleSubmit() {
  const fields = {
    name: clubName.value,
    category: clubCategory.value,
    tagline: clubTagline.value,
    about: clubAbout.value,
    email: clubEmail.value
  }

  if (!allFieldsFilled(fields)) {
    window.alert('Please fill in all fields before submitting.')
    return
  }

  if (!isValidEmail(clubEmail.value)) {
    window.alert('Please enter a valid email address.')
    return
  }

  await createClub({
    name: clubName.value.trim(),
    category: clubCategory.value,
    tagline: clubTagline.value.trim(),
    about: clubAbout.value.trim(),
    email: clubEmail.value.trim()
  })

  window.alert('Your club request has been submitted! The admin will review it within 2 to 3 working days.')
  router.push('/leader/club')
}
</script>

<template>
  <LeaderSidebar />

  <div class="main-content">

    <header class="topbar">
      <button class="btn-secondary" @click="goBack">
        <ArrowLeft /> Back
      </button>
      <div class="title-block">
        <h1 class="page-title">Create a New Club</h1>
        <p class="page-sub">Submit your request for admin approval</p>
      </div>
      <div class="topbar-spacer"></div>
    </header>

    <main class="content-body custom-scrollbar">

      <div class="form-guide-grid">

        <div class="form-card">
          <p class="form-card-title">Club Details</p>

          <div class="form-group">
            <label for="club-name">Club Name</label>
            <input type="text" id="club-name" v-model="clubName" class="input-field" placeholder="e.g. Campus Gaming Club">
          </div>

          <div class="form-group">
            <label for="club-category">Category</label>
            <select id="club-category" v-model="clubCategory" class="select-field">
              <option value="">Select a category</option>
              <option v-for="option in categoryOptions" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>

          <div class="form-group">
            <label for="club-tagline">Tagline</label>
            <input type="text" id="club-tagline" v-model="clubTagline" class="input-field" placeholder="One sentence about your club (shown on the directory card)">
          </div>

          <div class="form-group">
            <label for="club-about">About the Club</label>
            <textarea id="club-about" v-model="clubAbout" class="textarea-field" rows="5" placeholder="Describe your club's mission, activities, and what members can expect..."></textarea>
          </div>

          <div class="form-group">
            <label for="club-email">Leader Contact Email</label>
            <input type="email" id="club-email" v-model="clubEmail" class="input-field" placeholder="aayansh@knit.ac.in">
          </div>

          <button class="btn-primary" @click="handleSubmit">
            <Send /> Submit for Approval
          </button>
        </div>

        <div class="guide-card">
          <p class="guide-card-title">What happens next</p>
          <div v-for="step in guideSteps" :key="step.text" class="guide-step">
            <span class="guide-step-num" :class="{ 'guide-step-warn': step.warn }">{{ step.num }}</span>
            <span>{{ step.text }}</span>
          </div>
        </div>

      </div>

    </main>

  </div>
</template>
