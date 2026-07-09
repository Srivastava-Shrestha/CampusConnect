<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { GraduationCap, Compass, CalendarDays, Megaphone, Trophy, Sparkles, CircleUserRound, Briefcase } from 'lucide-vue-next'
import MobileNav from './MobileNav.vue'

const route = useRoute()
const auth = useAuthStore()

// The "Manage Clubs" entry only appears for a member who also leads a club.
const manageClubsItem = { label: 'Manage Clubs', to: '/leader/club', icon: Briefcase }

const menuItems = computed(function buildMenu() {
  const base = [
    { label: 'Clubs', to: '/clubs', icon: Compass },
    { label: 'Events', to: '/events', icon: CalendarDays },
    { label: 'Announcements', to: '/announcements', icon: Megaphone },
    { label: 'Leaderboard', to: '/leaderboard', icon: Trophy },
    { label: 'AI Finder', to: '/find-clubs', icon: Sparkles }
  ]
  if (auth.canManageClubs) {
    base.push(manageClubsItem)
  }
  return base
})

const mobileItems = computed(function buildMobileMenu() {
  const base = [
    { label: 'Clubs', to: '/clubs', icon: Compass },
    { label: 'Events', to: '/events', icon: CalendarDays },
    { label: 'News', to: '/announcements', icon: Megaphone },
    { label: 'Ranks', to: '/leaderboard', icon: Trophy },
    { label: 'Finder', to: '/find-clubs', icon: Sparkles },
    { label: 'Profile', to: '/profile', icon: CircleUserRound }
  ]
  if (auth.canManageClubs) {
    base.push({ label: 'Manage', to: '/leader/club', icon: Briefcase })
  }
  return base
})

function isActive(itemPath) {
  // The Manage Clubs entry stays highlighted across every leader page.
  // Require the trailing slash so /leaderboard does not match /leader.
  if (itemPath === '/leader/club') {
    return route.path.startsWith('/leader/')
  }
  return route.path === itemPath || route.path.startsWith(itemPath + '/')
}
</script>

<template>
  <aside class="sidebar">
    <div class="logo-row">
      <div class="logo-mark">
        <GraduationCap />
      </div>
      <span class="brand">Campus Connect</span>
    </div>

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

  <MobileNav :items="mobileItems" role-class="student" />
</template>
