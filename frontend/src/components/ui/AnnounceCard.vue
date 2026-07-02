<script setup>
import { Pin } from 'lucide-vue-next'
import ClubIcon from './ClubIcon.vue'

defineProps({
  announcement: { type: Object, required: true }
})
</script>

<template>
  <div class="announce-card" :class="{ pinned: announcement.pinned }">
    <div v-if="announcement.unread" class="announce-unread-dot"></div>
    <div class="announce-club-row">
      <div class="announce-dot" :class="announcement.dot">
        <ClubIcon :name="announcement.icon" />
      </div>
      <div class="announce-club-info">
        <p class="announce-club-name">{{ announcement.club }}</p>
        <p class="announce-time">{{ announcement.time }}</p>
      </div>
      <span v-if="announcement.pinned" class="announce-pin-badge">
        <Pin /> Pinned
      </span>
    </div>
    <p class="announce-title">{{ announcement.title }}</p>
    <p class="announce-body">{{ announcement.body }}</p>
    <div class="announce-footer">
      <span v-for="tag in announcement.tags" :key="tag" class="announce-tag">{{ tag }}</span>
    </div>
    <slot name="actions"></slot>
  </div>
</template>
