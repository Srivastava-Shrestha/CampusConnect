<script setup>
import { useLoadingBar } from '../../composables/useLoadingBar'

const { visible, progress } = useLoadingBar()
</script>

<template>
  <div v-show="visible" class="route-progress" aria-hidden="true">
    <div class="route-progress-bar" :style="{ width: progress + '%' }"></div>
  </div>
</template>
