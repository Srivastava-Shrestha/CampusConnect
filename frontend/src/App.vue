<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// The prototype CSS keys page layout off a body class, so sync it per route
watch(
  () => route.meta.bodyClass,
  function applyBodyClass(bodyClass) {
    document.body.className = bodyClass || 'portal-body'
  },
  { immediate: true }
)
</script>

<template>
  <router-view />
</template>
