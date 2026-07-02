<script setup>
import { useRoute } from 'vue-router'

defineProps({
  items: { type: Array, required: true },
  roleClass: { type: String, required: true }
})

const route = useRoute()

function isActive(item) {
  if (item.exact) {
    return route.path === item.to
  }
  return route.path === item.to || route.path.startsWith(item.to + '/')
}
</script>

<template>
  <nav class="mobile-nav">
    <router-link
      v-for="item in items"
      :key="item.to"
      :to="item.to"
      class="mobile-nav-item"
      :class="[roleClass, { active: isActive(item) }]"
    >
      <component :is="item.icon" />
      <span>{{ item.label }}</span>
    </router-link>
  </nav>
</template>
