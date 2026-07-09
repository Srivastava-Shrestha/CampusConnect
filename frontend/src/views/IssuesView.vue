<script setup>
import { ref, computed, onMounted } from 'vue'
import { MessageSquareWarning, Send } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import CustomSelect from '../components/ui/CustomSelect.vue'
import IssueCard from '../components/ui/IssueCard.vue'
import StatusPill from '../components/ui/StatusPill.vue'
import { getIssues, raiseIssue } from '../api/issues'
import { useFormValidation } from '../composables/useFormValidation'
import { toast } from '../composables/useToast'

const { allFieldsFilled } = useFormValidation()

const issues = ref([])

const issueTitle = ref('')
const issueCategory = ref('')
const issueClub = ref('')
const issueDesc = ref('')

const categoryOptions = [
  { value: 'event', label: 'Event' },
  { value: 'club', label: 'Club' },
  { value: 'certificate', label: 'Certificate' },
  { value: 'technical', label: 'Technical' },
  { value: 'general', label: 'General' }
]

const clubOptions = [
  { value: 'robotics', label: 'Robotics & Automation Club' },
  { value: 'music', label: 'Music Collective' },
  { value: 'photo', label: 'Photography Circle' },
  { value: 'coding', label: 'Coding Society' }
]

const openCount = computed(function countOpenIssues() {
  return issues.value.filter((issue) => issue.status !== 'resolved').length
})

function clearForm() {
  issueTitle.value = ''
  issueCategory.value = ''
  issueClub.value = ''
  issueDesc.value = ''
}

async function submitIssue() {
  const fields = {
    title: issueTitle.value,
    category: issueCategory.value,
    club: issueClub.value,
    desc: issueDesc.value
  }

  if (!allFieldsFilled(fields)) {
    toast.error('Please fill in all fields before submitting.')
    return
  }

  await raiseIssue(fields)
  toast.success('Issue submitted. The club leader has been notified and will respond within 48 hours.')
  clearForm()
}

onMounted(async function loadIssues() {
  issues.value = await getIssues()
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content">

    <Topbar title="Issues" sub="Raise a concern or track your open issues" :show-bell="false" />

    <main class="content-body custom-scrollbar">

      <div class="issues-layout">

        <div class="issue-form-card">
          <p class="issue-form-title">
            <MessageSquareWarning />
            Raise a New Issue
          </p>

          <div class="form-group">
            <label for="issue-title">Issue Title</label>
            <input type="text" id="issue-title" v-model="issueTitle" class="input-field" placeholder="Short summary of the problem">
          </div>

          <div class="form-group">
            <label for="issue-category">Category</label>
            <CustomSelect v-model="issueCategory" :options="categoryOptions" placeholder="Select category" />
          </div>

          <div class="form-group">
            <label for="issue-club">Related Club</label>
            <CustomSelect v-model="issueClub" :options="clubOptions" placeholder="Select club" />
          </div>

          <div class="form-group">
            <label for="issue-desc">Description</label>
            <textarea id="issue-desc" v-model="issueDesc" class="textarea-field" rows="4" placeholder="Describe the issue in detail so the club leader can help you."></textarea>
          </div>

          <button class="btn-primary" @click="submitIssue">
            <Send /> Submit Issue
          </button>

          <p class="text-note">Issues are sent directly to the club leader. Most are resolved within 48 hours.</p>
        </div>

        <div>
          <div class="issue-feed-header">
            <h2 class="clubs-section-title">Your Issues</h2>
            <StatusPill status="open" :label="openCount + ' open'" />
          </div>

          <div class="issue-feed">
            <IssueCard
              v-for="issue in issues"
              :key="issue.id"
              :issue="issue"
            />
          </div>
        </div>

      </div>

    </main>

  </div>
</template>
