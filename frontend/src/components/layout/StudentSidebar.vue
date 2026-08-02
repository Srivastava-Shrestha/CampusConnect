<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { GraduationCap, Compass, CalendarDays, Megaphone, Trophy, Sparkles, CircleUserRound, Briefcase } from 'lucide-vue-next'
import MobileNav from './MobileNav.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const slug = computed(() => auth.user.collegeSlug)

// The "Manage Clubs" entry only appears for a member who also leads a club.
const manageClubsItem = computed(() => ({
  label: 'Manage Clubs',
  to: `/${slug.value}/leader/club`,
  icon: Briefcase
}))

const menuItems = computed(function buildMenu() {
  const base = [
  { label: 'Clubs', to: `/${slug.value}/clubs`, icon: Compass },
  { label: 'Propose Club', to: `/${slug.value}/clubs/propose`, icon: Briefcase },
  { label: 'Events', to: `/${slug.value}/events`, icon: CalendarDays },
  { label: 'Announcements', to: `/${slug.value}/announcements`, icon: Megaphone },
  { label: 'Leaderboard', to: `/${slug.value}/leaderboard`, icon: Trophy },
  { label: 'AI Finder', to: `/${slug.value}/find-clubs`, icon: Sparkles }
]
  if (auth.canManageClubs) {
    base.push(manageClubsItem.value)
  }
  return base
})

const mobileItems = computed(function buildMobileMenu() {
  const base = [
    { label: 'Clubs', to: `/${slug.value}/clubs`, icon: Compass },
    { label: 'Events', to: `/${slug.value}/events`, icon: CalendarDays },
    { label: 'News', to: `/${slug.value}/announcements`, icon: Megaphone },
    { label: 'Ranks', to: `/${slug.value}/leaderboard`, icon: Trophy },
    { label: 'Finder', to: `/${slug.value}/find-clubs`, icon: Sparkles },
    { label: 'Profile', to: `/${slug.value}/profile`, icon: CircleUserRound },
    { label: 'Propose', to: `/${slug.value}/clubs/propose`, icon: Briefcase }
  ]
  if (auth.canManageClubs) {
    base.push({ label: 'Manage', to: `/${slug.value}/leader/club`, icon: Briefcase })
  }
  return base
})

function isActive(itemPath) {
  // The Manage Clubs entry stays highlighted across every leader page.
  // Require the trailing slash so /leaderboard does not match /leader.
  if (itemPath.endsWith('/leader/club')) {
    return route.path.startsWith(`/${slug.value}/leader/`)
  }
  return route.path === itemPath || route.path.startsWith(itemPath + '/')
}

function logout() {
  const collegeSlug = auth.user.collegeSlug

  auth.logout()

  router.push(`/${collegeSlug}/login`)
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

  <div>
    <router-link v-if="slug" :to="`/${slug}/profile`" class="user-card">
      <div class="user-avatar student-av">{{ auth.user.initials }}</div>
      <div class="user-info">
        <p class="user-name">{{ auth.user.name }}</p>
      </div>
    </router-link>

    <button class="logout-btn" @click="logout">
        Logout
    </button>
  </div>
  </aside>

  <MobileNav :items="mobileItems" role-class="student" />
</template>
