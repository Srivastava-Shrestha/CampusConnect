<script setup>
import { Check, X } from 'lucide-vue-next'
import StatusPill from './StatusPill.vue'

defineProps({
  approval: { type: Object, required: true },
  metaField: { type: String, default: 'meta' }
})

const emit = defineEmits(['approve', 'reject'])

const statusLabels = {
  pending: 'Pending',
  approved: 'Approved',
  rejected: 'Rejected'
}

function approveClub() {
  emit('approve')
}

function rejectClub() {
  emit('reject')
}
</script>

<template>
  <div
    class="approval-card"
    :class="{ approved: approval.status === 'approved', rejected: approval.status === 'rejected' }"
  >
    <div class="approval-club-icon" :class="approval.icon">{{ approval.emoji }}</div>
    <div class="approval-info">
      <p class="approval-club-name">{{ approval.name }}</p>
      <p class="approval-meta">{{ approval[metaField] }}</p>
    </div>
    <div class="approval-actions">
      <template v-if="approval.status === 'pending'">
        <StatusPill status="pending" label="Pending" />
        <button class="btn-success" @click="approveClub">
          <Check /> Approve
        </button>
        <button class="btn-danger" @click="rejectClub">
          <X /> Reject
        </button>
      </template>
      <StatusPill v-else :status="approval.status" :label="statusLabels[approval.status]" />
    </div>
  </div>
</template>
