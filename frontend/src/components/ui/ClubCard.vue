<script setup>
import { Users, Sparkles } from 'lucide-vue-next'

defineProps({
  club: { type: Object, required: true },
  badge: { type: String, default: '' }
})

const emit = defineEmits(['open'])

function openClub() {
  emit('open')
}
</script>

<template>
  <div class="club-card" @click="openClub">
  <div class="club-card-banner">
    <div class="club-card-circle-1"></div>
    <div class="club-card-circle-2"></div>
    <div class="club-card-circle-3"></div>

    <div v-if="badge" class="club-card-recommended-badge">
      <Sparkles /> {{ badge }}
    </div>
  </div>

  <div class="club-card-content">
    <div>
      <div class="club-card-header">
        <span class="club-card-title">{{ club.name }}</span>

        <span class="club-card-members">
          <Users /> {{ club.member_count }}
        </span>
      </div>

      <p class="club-card-desc">
        {{ club.description }}
      </p>
    </div>

    <div class="club-card-tags">
      <span class="club-card-tag">{{ club.category }}</span>
      <span v-if="club.type" class="club-card-tag">
          {{ club.type }}
      </span>
    </div>
  </div>
</div>
</template>
