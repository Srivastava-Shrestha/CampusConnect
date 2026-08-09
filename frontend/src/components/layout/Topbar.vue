<script setup>
import { Bell } from 'lucide-vue-next'
import { toast } from '../../composables/useToast'

defineProps({
  title: { type: String, required: true },
  sub: { type: String, default: '' },
  showBell: { type: Boolean, default: true }
})

function showNotifications() {
  toast.info('No new notifications.')
}
</script>

<template>
  <header class="topbar">
    <div class="title-block">
      <h1 class="page-title">{{ title }}</h1>
      <p v-if="sub" class="page-sub">{{ sub }}</p>
    </div>

    <div class="topbar-spacer"></div>

    <slot>
      <div v-if="showBell" class="bell-btn" @click="showNotifications">
        <Bell />
      </div>
    </slot>
  </header>
</template>
