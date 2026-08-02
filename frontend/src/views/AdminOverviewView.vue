<script setup>
import { ref, computed, onMounted } from 'vue'
import { Clock, CheckCircle2, XCircle } from 'lucide-vue-next'
import AdminSidebar from '../components/layout/AdminSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import StatCard from '../components/ui/StatCard.vue'
import StatusPill from '../components/ui/StatusPill.vue'
import ApprovalCard from '../components/ui/ApprovalCard.vue'
import { getClubApprovals, approveClubRequest, rejectClubRequest } from '../api/clubs'
import { toast } from '../composables/useToast'
import { useAuthStore } from '../stores/auth'

const pendingList = ref([])

const approvedTotal = ref(0)
const rejectedTotal = ref(0)

const auth = useAuthStore()

const pendingCount = computed(() => pendingList.value.length)

async function handleApprove(approval) {
  await approveClubRequest(approval.id)
  approval.status = 'approved'
}

const collegeSubtitle = computed(() => {
  return `${auth.user.collegeName || auth.user.collegeSlug} · Campus Connect`
})

async function handleReject(approval) {
  const reason = window.prompt('Enter a short reason for rejection (shown to the club leader):')
  if (reason === null) {
    return
  }

  await rejectClubRequest(approval.id, reason)
  approval.status = 'rejected'
}

onMounted(async () => {
  try {
    const [pending, active, rejected] = await Promise.all([
      getClubApprovals("PENDING"),
      getClubApprovals("ACTIVE"),
      getClubApprovals("REJECTED")
    ])

    pendingList.value = pending
    approvedTotal.value = active.length
    rejectedTotal.value = rejected.length

  } catch (error) {
    toast.error(error.message)
  }
})
</script>

<template>
  <AdminSidebar />

  <div class="main-content">

    <Topbar title="Admin Dashboard" :sub="collegeSubtitle"/>

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

    </main>

  </div>
</template>
