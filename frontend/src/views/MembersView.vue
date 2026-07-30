<script setup>
import { ref, computed, onMounted } from 'vue'
import { Users, Clock, ShieldCheck, Check, X } from 'lucide-vue-next'

import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import StatCard from '../components/ui/StatCard.vue'
import StatusPill from '../components/ui/StatusPill.vue'
import MemberRow from '../components/ui/MemberRow.vue'

import {
  getMyClubs,
  getClubMembers,
  getPendingRequests,
  handleMembershipRequest
} from '../api/clubs'

import { toast } from '../composables/useToast'

const clubId = ref(null)
const clubName = ref('Your Club')

const members = ref([])
const requests = ref([])

const totalMembers = computed(() => members.value.length)

const pendingCount = computed(() =>
  requests.value.filter(request => !request.decision).length
)

const officerCount = computed(() =>
  members.value.filter(member => member.role === 'officer').length
)

async function approveRequest(request) {
  try {
    await handleMembershipRequest(
      clubId.value,
      request.id,
      'APPROVED'
    )

    request.decision = 'approved'
    toast.success('Request approved.')
  } catch (error) {
    console.error(error)
    toast.error('Failed to approve request.')
  }
}

async function rejectRequest(request) {
  try {
    await handleMembershipRequest(
      clubId.value,
      request.id,
      'REJECTED'
    )

    request.decision = 'rejected'
    toast.success('Request rejected.')
  } catch (error) {
    console.error(error)
    toast.error('Failed to reject request.')
  }
}

function handleRemoveMember() {
  toast.info('Removing members is not supported yet.')
}

onMounted(async () => {
  try {

    const myClubs = await getMyClubs({
      role: 'LEADER'
    })

    console.log('Leader clubs:', myClubs)

    if (!Array.isArray(myClubs) || myClubs.length === 0) {
      toast.error('No club assigned.')
      return
    }

    clubId.value = myClubs[0].id
    clubName.value = myClubs[0].name

    const rawMembers = await getClubMembers(clubId.value)
    const rawRequests = await getPendingRequests(clubId.value)

    members.value = rawMembers.map(item => ({
      id: item.id,
      name: item.full_name,
      initials: item.full_name
        .split(' ')
        .map(word => word[0])
        .join('')
        .slice(0, 2)
        .toUpperCase(),
      sub: `Student ID: ${item.student_id}`,
      role: item.role === 'LEADER' ? 'officer' : 'member',
      roleLabel:
        item.role.charAt(0) +
        item.role.slice(1).toLowerCase()
    }))

    requests.value = rawRequests.map(item => ({
      id: item.id,
      name: item.full_name,
      initials: item.full_name
        .split(' ')
        .map(word => word[0])
        .join('')
        .slice(0, 2)
        .toUpperCase(),
      sub: `Student ID: ${item.student_id}`,
      role: item.role,
      status: item.status,
      decision:
        item.status === 'APPROVED'
          ? 'approved'
          : item.status === 'REJECTED'
            ? 'rejected'
            : null
    }))

  } catch (error) {
    console.error(error)
    toast.error('Failed to load members.')
  }
})
</script>

<template>
  <LeaderSidebar />

  <div class="main-content">

    <Topbar
      title="Members"
      :sub="clubName"
      :show-bell="false"
    />

    <main class="content-body custom-scrollbar">

      <div class="stats-grid">
        <StatCard
          :num="totalMembers"
          label="Total Members"
          :icon="Users"
          color-class="green-stat"
        />

        <StatCard
          :num="pendingCount"
          label="Pending Requests"
          :icon="Clock"
          color-class="blue-stat"
        />

        <StatCard
          :num="officerCount"
          label="Officers"
          :icon="ShieldCheck"
          color-class="pink-stat"
        />
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">
            Pending Join Requests
          </h2>

          <StatusPill
            status="pending"
            :label="pendingCount + ' pending'"
          />
        </div>

        <div class="approval-list">

          <div
            v-for="request in requests"
            :key="request.id"
            class="member-request-card"
            :class="{
              'approved-member': request.decision === 'approved',
              'rejected-member': request.decision === 'rejected'
            }"
          >

            <div class="member-req-avatar">
              {{ request.initials }}
            </div>

            <div class="member-req-info">
              <p class="member-req-name">
                {{ request.name }}
              </p>

              <p class="member-req-sub">
                {{ request.sub }}
              </p>
            </div>

            <div class="member-req-actions">

              <template v-if="!request.decision">

                <StatusPill
                  status="pending"
                  label="Pending"
                />

                <button
                  class="btn-success"
                  @click="approveRequest(request)"
                >
                  <Check />
                  Approve
                </button>

                <button
                  class="btn-danger"
                  @click="rejectRequest(request)"
                >
                  <X />
                  Reject
                </button>

              </template>

              <StatusPill
                v-else-if="request.decision === 'approved'"
                status="approved"
                label="Approved"
              />

              <StatusPill
                v-else
                status="rejected"
                label="Rejected"
              />

            </div>

          </div>

        </div>
      </div>

      <div>

        <div class="clubs-section-header">

          <h2 class="clubs-section-title">
            Active Members
          </h2>

          <span class="clubs-count-text">
            Showing {{ members.length }} of {{ totalMembers }}
          </span>

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
