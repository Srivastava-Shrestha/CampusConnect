<script setup>
import { ref, computed, onMounted } from 'vue'
import { Clock, CheckCircle2, XCircle, Save } from 'lucide-vue-next'
import AdminSidebar from '../components/layout/AdminSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import StatCard from '../components/ui/StatCard.vue'
import StatusPill from '../components/ui/StatusPill.vue'
import ApprovalCard from '../components/ui/ApprovalCard.vue'
import { getClubApprovals, approveClubRequest, rejectClubRequest } from '../api/clubs'

const pendingList = ref([])

const collegeName = ref('KNIT Sultanpur')
const emailDomain = ref('@knit.ac.in')
const city = ref('Sultanpur')
const state = ref('Uttar Pradesh')

const approvedTotal = 18
const rejectedTotal = 2

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

function saveSettings() {
  window.alert('College settings saved successfully.')
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
              <input type="text" id="college-name" v-model="collegeName" class="input-field">
            </div>
            <div class="form-group">
              <label for="email-domain">Verified Student Email Domain</label>
              <input type="text" id="email-domain" v-model="emailDomain" class="input-field">
            </div>
            <div class="form-group">
              <label for="city">City</label>
              <input type="text" id="city" v-model="city" class="input-field">
            </div>
            <div class="form-group">
              <label for="state">State</label>
              <input type="text" id="state" v-model="state" class="input-field">
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
