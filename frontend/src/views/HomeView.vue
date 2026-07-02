<script setup>
import { GraduationCap } from 'lucide-vue-next'
</script>

<template>
  <div class="landing-shell">
    <div class="logo-row logo-row-flat">
      <div class="logo-mark">
        <GraduationCap />
      </div>
      <span class="brand">Campus Connect</span>
    </div>
    <p>The landing page will be implemented in the public group phase.</p>
    <p>
      <router-link to="/login">Sign in</router-link> ·
      <router-link to="/signup">Create account</router-link>
    </p>
  </div>
</template>
