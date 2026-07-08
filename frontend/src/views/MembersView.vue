<script setup>
import { ref, computed, onMounted } from 'vue'
import { Users, Clock, ShieldCheck, Check, X } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import LeaderTopNav from '../components/layout/LeaderTopNav.vue'
import Topbar from '../components/layout/Topbar.vue'
import StatCard from '../components/ui/StatCard.vue'
import StatusPill from '../components/ui/StatusPill.vue'
import MemberRow from '../components/ui/MemberRow.vue'
import { getMembers, getJoinRequests, approveJoinRequest, rejectJoinRequest, removeMember } from '../api/members'
import { toast } from '../composables/useToast'

const clubId = 1
const totalMembers = ref(84)

const members = ref([])
const requests = ref([])

const pendingCount = computed(function countPending() {
  return requests.value.filter((request) => !request.decision).length
})

const officerCount = computed(function countOfficers() {
  return members.value.filter((member) => member.role === 'officer').length
})

async function approveRequest(request) {
  await approveJoinRequest(clubId, request.id)
  request.decision = 'approved'
}

async function rejectRequest(request) {
  await rejectJoinRequest(clubId, request.id)
  request.decision = 'rejected'
}

async function handleRemoveMember(member) {
  const confirmed = window.confirm('Remove ' + member.name + ' from the club? They will need to re-apply to rejoin.')
  if (!confirmed) return

  await removeMember(clubId, member.id)
  toast.success(member.name + ' has been removed from the club.')
}

onMounted(async function loadMembersPage() {
  members.value = await getMembers(clubId)
  requests.value = await getJoinRequests(clubId)
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content">
    <LeaderTopNav />

    <Topbar title="Members" sub="Robotics & Automation Club" :show-bell="false" />

    <main class="content-body custom-scrollbar">

      <div class="stats-grid">
        <StatCard :num="totalMembers" label="Total Members" :icon="Users" color-class="green-stat" />
        <StatCard :num="pendingCount" label="Pending Requests" :icon="Clock" color-class="blue-stat" />
        <StatCard :num="officerCount" label="Officers" :icon="ShieldCheck" color-class="pink-stat" />
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Pending Join Requests</h2>
          <StatusPill status="pending" :label="pendingCount + ' pending'" />
        </div>

        <div class="approval-list">
          <div v-for="request in requests" :key="request.id" class="member-request-card" :class="{ 'approved-member': request.decision === 'approved', 'rejected-member': request.decision === 'rejected' }">
            <div class="member-req-avatar">{{ request.initials }}</div>
            <div class="member-req-info">
              <p class="member-req-name">{{ request.name }}</p>
              <p class="member-req-sub">{{ request.sub }}</p>
            </div>
            <div class="member-req-actions">
              <template v-if="!request.decision">
                <StatusPill status="pending" label="Pending" />
                <button class="btn-success" @click="approveRequest(request)">
                  <Check /> Approve
                </button>
                <button class="btn-danger" @click="rejectRequest(request)">
                  <X /> Reject
                </button>
              </template>
              <StatusPill v-else-if="request.decision === 'approved'" status="approved" label="Approved" />
              <StatusPill v-else status="rejected" label="Rejected" />
            </div>
          </div>
        </div>
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Active Members</h2>
          <span class="clubs-count-text">Showing {{ members.length }} of {{ totalMembers }}</span>
        </div>

        <div class="member-list">
          <MemberRow
            v-for="member in members"
            :key="member.id"
            :member="member"
            @remove="handleRemoveMember(member)"
          />
        </div>
      </div>

    </main>

  </div>
</template>
