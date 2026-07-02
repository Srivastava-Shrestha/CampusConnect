<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { GraduationCap, Compass, CalendarDays, Megaphone, Trophy, Sparkles } from 'lucide-vue-next'

const route = useRoute()
const auth = useAuthStore()

const menuItems = [
  { label: 'Clubs', to: '/clubs', icon: Compass },
  { label: 'Events', to: '/events', icon: CalendarDays },
  { label: 'Announcements', to: '/announcements', icon: Megaphone },
  { label: 'Leaderboard', to: '/leaderboard', icon: Trophy },
  { label: 'AI Finder', to: '/find-clubs', icon: Sparkles }
]

function isActive(itemPath) {
  return route.path === itemPath || route.path.startsWith(itemPath + '/')
}
</script>

<template>
  <aside class="sidebar">
    <router-link to="/" class="logo-row">
      <div class="logo-mark">
        <GraduationCap />
      </div>
      <span class="brand">Campus Connect</span>
    </router-link>

    <p class="nav-label">Menu</p>

    <nav class="sidebar-menu">
      <router-link
        v-for="item in menuItems"
        :key="item.to"
        :to="item.to"
        class="sidebar-item"
        :class="{ active: isActive(item.to), student: isActive(item.to) }"
      >
        <component :is="item.icon" /> {{ item.label }}
      </router-link>
    </nav>

    <div class="sidebar-spacer"></div>

    <router-link to="/profile" class="user-card">
      <div class="user-avatar student-av">{{ auth.user.initials }}</div>
      <div class="user-info">
        <p class="user-name">{{ auth.user.name }}</p>
        <p class="user-sub">{{ auth.user.sub }}</p>
      </div>
    </router-link>
  </aside>
</template>
