<script setup>
import { CheckCircle2 } from 'lucide-vue-next'
import StatusPill from './StatusPill.vue'

defineProps({
  issue: { type: Object, required: true }
})
</script>

<template>
  <div class="issue-card" :class="{ resolved: issue.status === 'resolved' }">
    <div class="issue-top">
      <p class="issue-title">{{ issue.title }}</p>
      <StatusPill :status="issue.status" :label="issue.statusLabel" />
    </div>
    <p class="issue-meta">{{ issue.meta }}</p>
    <p class="issue-desc">{{ issue.desc }}</p>
    <div v-if="issue.response" class="issue-response">
      <p class="issue-response-label">
        <CheckCircle2 />
        Leader responded · {{ issue.response.by }}
      </p>
      <p class="issue-response-text">{{ issue.response.text }}</p>
    </div>
    <div class="issue-footer">
      <span v-for="tag in issue.tags" :key="tag" class="announce-tag">{{ tag }}</span>
    </div>
    <slot name="actions"></slot>
  </div>
</template>
