<script setup>
import { ref, computed, onMounted } from 'vue'
import { Clock, CheckCircle2, XCircle } from 'lucide-vue-next'
import AdminSidebar from '../components/layout/AdminSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import StatCard from '../components/ui/StatCard.vue'
import ApprovalCard from '../components/ui/ApprovalCard.vue'
import FilterChips from '../components/ui/FilterChips.vue'
import { getClubApprovals, approveClubRequest, rejectClubRequest } from '../api/clubs'

const approvals = ref([])
const activeFilter = ref('all')

const approvedBase = 18
const rejectedBase = 2

const filterChips = [
  { id: 'all', label: 'All' },
  { id: 'pending', label: 'Pending' },
  { id: 'approved', label: 'Approved' },
  { id: 'rejected', label: 'Rejected' }
]

const visibleApprovals = computed(function filterApprovals() {
  return approvals.value.filter(function matchesFilter(approval) {
    if (activeFilter.value === 'all') {
      return true
    }

    return approval.status === activeFilter.value
  })
})

const pendingCount = computed(function countPending() {
  return approvals.value.filter(function isPending(approval) {
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

onMounted(async function loadApprovals() {
  approvals.value = await getClubApprovals()
})
</script>

<template>
  <AdminSidebar />

  <div class="main-content">

    <Topbar title="Club Approvals" sub="KNIT Sultanpur · All club registration requests" />

    <main class="content-body custom-scrollbar">

      <div class="stats-grid">
        <StatCard :num="pendingCount" label="Pending Review" :icon="Clock" color-class="blue-stat" />
        <StatCard :num="approvedBase" label="Approved" :icon="CheckCircle2" color-class="green-stat" />
        <StatCard :num="rejectedBase" label="Rejected" :icon="XCircle" color-class="pink-stat" />
      </div>

      <FilterChips :chips="filterChips" v-model="activeFilter" />

      <div class="approval-list">
        <ApprovalCard
          v-for="approval in visibleApprovals"
          :key="approval.id"
          :approval="approval"
          meta-field="metaFull"
          @approve="handleApprove(approval)"
          @reject="handleReject(approval)"
        />
      </div>

      <div v-if="visibleApprovals.length === 0" class="empty-state">
        <CheckCircle2 />
        <p>No approvals match this filter.</p>
      </div>

    </main>

  </div>
</template>
