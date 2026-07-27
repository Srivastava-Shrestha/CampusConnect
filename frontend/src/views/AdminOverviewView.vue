<script setup>
import { ref, computed, onMounted } from 'vue'
import { Clock, CheckCircle2, XCircle, Save } from 'lucide-vue-next'
import AdminSidebar from '../components/layout/AdminSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import StatCard from '../components/ui/StatCard.vue'
import StatusPill from '../components/ui/StatusPill.vue'
import ApprovalCard from '../components/ui/ApprovalCard.vue'
import { getClubApprovals, approveClubRequest, rejectClubRequest } from '../api/clubs'
import { toast } from '../composables/useToast'
import { onboardCollege } from '../api/auth'
import { useAuthStore } from '../stores/auth'

const pendingList = ref([])

const collegeName = ref('')
const emailDomain = ref('')
const description = ref('')

const approvedTotal = 18
const rejectedTotal = 2

const auth = useAuthStore()

const pendingCount = computed(function countStillPending() {
  return pendingList.value.filter(function isPending(approval) {
    return approval.status === 'pending'
  }).length
})

async function handleApprove(approval) {
  await approveClubRequest(approval.id)
  approval.status = 'approved'
}

async function handleReject(approval) {
  const reason = window.prompt('Enter a short reason for rejection (shown to the club leader):')
  if (reason === null) {
    return
  }

  await rejectClubRequest(approval.id, reason)
  approval.status = 'rejected'
}

async function saveSettings() {
  if (!collegeName.value.trim() || !emailDomain.value.trim() || !description.value.trim()) {
    toast.error('College name, email domain and description are required.')
    return
  }

  try {
    await onboardCollege(
      {
        name: collegeName.value.trim(),
        email_suffix: emailDomain.value.replace('@', '').trim(),
        description: description.value.trim()
      },
      auth.token
    )

    toast.success('College registered successfully.')

  } catch (error) {
    toast.error(error.message)
  }
}

onMounted(async function loadOverview() {
  const allApprovals = await getClubApprovals()

  pendingList.value = allApprovals.filter(function onlyPending(approval) {
    return approval.status === 'pending'
  })
})
</script>

<template>
  <AdminSidebar />

  <div class="main-content">

    <Topbar title="Admin Dashboard" sub="KNIT Sultanpur · Campus Connect" />

    <main class="content-body custom-scrollbar">

      <div class="stats-grid">
        <StatCard :num="pendingCount" label="Pending Approvals" :icon="Clock" color-class="blue-stat" />
        <StatCard :num="approvedTotal" label="Clubs Approved" :icon="CheckCircle2" color-class="green-stat" />
        <StatCard :num="rejectedTotal" label="Clubs Rejected" :icon="XCircle" color-class="pink-stat" />
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Pending Club Approvals</h2>
          <StatusPill status="pending" :label="pendingCount + ' pending'" />
        </div>

        <div class="approval-list">
          <ApprovalCard
            v-for="approval in pendingList"
            :key="approval.id"
            :approval="approval"
            @approve="handleApprove(approval)"
            @reject="handleReject(approval)"
          />
        </div>
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">College Settings</h2>
        </div>
        <div class="admin-settings-card">
          <div class="admin-settings-grid">
            <div class="form-group">
              <label for="college-name">College Name</label>
              <input type="text" id="college-name" v-model="collegeName" class="input-field" placeholder="Indian Institute Of Technology Madras">
            </div>
            <div class="form-group">
              <label for="email-domain">Verified Student Email Domain</label>
              <input type="text" id="email-domain" v-model="emailDomain" class="input-field" placeholder=".iitm.ac.in">
            </div>
            <div class="form-group">
              <label for="description">Description</label>
              <textarea id="description" v-model="description" class="input-field" rows="3" placeholder="Enter a short description about the college">
              </textarea>
            </div>
          </div>
          <button class="btn-primary" @click="saveSettings">
            <Save /> Save Settings
          </button>
        </div>
      </div>

    </main>

  </div>
</template>
