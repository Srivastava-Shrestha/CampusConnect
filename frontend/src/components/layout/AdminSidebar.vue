<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { GraduationCap, LayoutDashboard, CheckCircle2, Building2, Settings } from 'lucide-vue-next'
import MobileNav from './MobileNav.vue'

const route = useRoute()
const auth = useAuthStore()

const menuItems = [
  { label: 'Overview', to: '/admin', icon: LayoutDashboard },
  { label: 'Approvals', to: '/admin/approvals', icon: CheckCircle2 },
  { label: 'Colleges', to: '/admin/colleges', icon: Building2 }
]

const mobileItems = [
  { label: 'Overview', to: '/admin', icon: LayoutDashboard, exact: true },
  { label: 'Approvals', to: '/admin/approvals', icon: CheckCircle2 },
  { label: 'Colleges', to: '/admin/colleges', icon: Building2 }
]

function isActive(itemPath) {
  if (itemPath === '/admin') {
    return route.path === '/admin'
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

    <p class="nav-label">Admin</p>

    <nav class="sidebar-menu">
      <router-link
        v-for="item in menuItems"
        :key="item.to"
        :to="item.to"
        class="sidebar-item"
        :class="{ active: isActive(item.to), admin: isActive(item.to) }"
      >
        <component :is="item.icon" /> {{ item.label }}
      </router-link>
      <a href="#" class="sidebar-item">
        <Settings /> Settings
      </a>
    </nav>

    <div class="sidebar-spacer"></div>

    <a href="#" class="user-card">
      <div class="user-avatar admin-av">{{ auth.user.initials }}</div>
      <div class="user-info">
        <p class="user-name">{{ auth.user.name }}</p>
        <p class="user-sub">{{ auth.user.sub }}</p>
      </div>
    </a>
  </aside>

  <MobileNav :items="mobileItems" role-class="admin" />
</template>
