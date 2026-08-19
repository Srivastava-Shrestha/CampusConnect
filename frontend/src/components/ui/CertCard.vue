<script setup>
import { Award, ExternalLink } from 'lucide-vue-next'

defineProps({
  cert: { type: Object, required: true }
})

function buildViewQuery(cert) {
  return {
    name: cert.name,
    event: cert.event,
    club: cert.club,
    result: cert.result,
    date: cert.date,
    serial: cert.serial
  }
}
</script>

<template>
  <div class="cert-card">
    <p class="cert-event-name">{{ cert.event }}</p>
    <p class="cert-club-tag">{{ cert.club }} · {{ cert.dateShort }}</p>
    <div class="result-badge" :class="cert.result">
      <Award /> {{ cert.resultLabel }}
    </div>
    <div class="cert-footer">
      <span class="cert-serial">{{ cert.serial }}</span>
      <router-link
        :to="{ path: '/cert/view', query: buildViewQuery(cert) }"
        target="_blank"
        class="cert-verify-link"
      >
        View <ExternalLink />
      </router-link>
    </div>
  </div>
</template>
