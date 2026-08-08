<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import LoadingBar from './components/ui/LoadingBar.vue'
import ToastContainer from './components/ui/ToastContainer.vue'

const route = useRoute()

// style.css keys each page shell off a class that must wrap the page content
const shellClass = computed(function pickShellClass() {
  return route.meta.bodyClass || 'portal-body'
})

// Admin and club-leader tools use a calmer, more neutral palette than the
// public and student-facing pages, which keep the warm Campus Connect colours.
// The class below scopes that palette; section 55 of style.css redefines the
// design tokens inside it. bodyClass cannot do this job because 'portal-body'
// is shared by student, leader and admin pages alike.
const themeClass = computed(function pickThemeClass() {
  if (route.meta.role === 'admin') {
    return 'theme-workspace'
  }

  if (route.meta.role === 'leader') {
    return 'theme-workspace'
  }

  return ''
})
</script>

<template>
  <LoadingBar />
  <ToastContainer />
  <div :class="[shellClass, themeClass]">
    <router-view />
  </div>
</template>
