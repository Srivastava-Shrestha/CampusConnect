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
</script>

<template>
  <LoadingBar />
  <ToastContainer />
  <div :class="shellClass">
    <router-view />
  </div>
</template>
