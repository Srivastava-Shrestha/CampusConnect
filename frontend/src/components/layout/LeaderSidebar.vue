<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { GraduationCap, LayoutDashboard, UsersRound, CalendarDays, Megaphone, TriangleAlert, PlusCircle, Compass } from 'lucide-vue-next'
import MobileNav from './MobileNav.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const menuItems = [
  { label: 'My Club', to: '/leader/club', icon: LayoutDashboard },
  { label: 'Members', to: '/leader/members', icon: UsersRound },
  { label: 'Events', to: '/leader/events', icon: CalendarDays },
  { label: 'Announcements', to: '/leader/announcements', icon: Megaphone },
  { label: 'Issues', to: '/leader/issues', icon: TriangleAlert },
  { label: 'Create Club', to: '/clubs/propose', icon: PlusCircle },
  { label: 'Member Area', to: '/clubs', icon: Compass }
]

const mobileItems = [
  { label: 'Club', to: '/leader/club', icon: LayoutDashboard },
  { label: 'Members', to: '/leader/members', icon: UsersRound },
  { label: 'Events', to: '/leader/events', icon: CalendarDays },
  { label: 'Posts', to: '/leader/announcements', icon: Megaphone },
  { label: 'Issues', to: '/leader/issues', icon: TriangleAlert },
  { label: 'Member', to: '/clubs', icon: Compass }
]

function isActive(itemPath) {
  return route.path === itemPath || route.path.startsWith(itemPath + '/')
}

function logout() {
  auth.logout()
  router.push('/login')
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

    <p class="nav-label">Leader</p>

    <nav class="sidebar-menu">
      <router-link
        v-for="item in menuItems"
        :key="item.to"
        :to="item.to"
        class="sidebar-item"
        :class="{ active: isActive(item.to), leader: isActive(item.to) }"
      >
        <component :is="item.icon" /> {{ item.label }}
      </router-link>
    </nav>

    <div class="sidebar-spacer"></div>

    <div>
    <div class="user-card">
      <div class="user-avatar leader-av">{{ auth.user.initials }}</div>
      <div class="user-info">
        <p class="user-name">{{ auth.user.name }}</p>
        <p class="user-sub">{{ auth.user.email }}</p>
      </div>
    </div>

    <button class="logout-btn" @click="logout">
        Logout
    </button>
    </div>
  </aside>

  <MobileNav :items="mobileItems" role-class="leader" />
</template>
