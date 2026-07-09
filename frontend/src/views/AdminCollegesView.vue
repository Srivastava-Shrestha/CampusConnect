<script setup>
import { ref } from 'vue'
import { Users, Layers, CalendarCheck, Save, Pencil, School } from 'lucide-vue-next'
import AdminSidebar from '../components/layout/AdminSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import StatCard from '../components/ui/StatCard.vue'
import StatusPill from '../components/ui/StatusPill.vue'
import { toast } from '../composables/useToast'

const collegeName = ref('KNIT Sultanpur')
const fullName = ref('Kamla Nehru Institute of Technology')
const emailDomain = ref('@knit.ac.in')
const adminEmail = ref('studentaffairs@knit.ac.in')
const city = ref('Sultanpur')
const state = ref('Uttar Pradesh')
const maxClubs = ref(30)
const maxMembers = ref(200)

const allowedCategories = [
  'Tech',
  'Culture',
  'Sports',
  'Arts',
  'Science',
  'Social',
  'Business',
  'Literary'
]

function saveSettings() {
  if (!collegeName.value.trim() || !emailDomain.value.trim()) {
    toast.error('College name and email domain are required.')
    return
  }

  toast.success('College settings saved successfully.')
}

function showCategoryHint() {
  toast.info('Category management will be available after the backend is connected.')
}
</script>

<template>
  <AdminSidebar />

  <div class="main-content">

    <Topbar title="Colleges" sub="Platform configuration for KNIT Sultanpur" />

    <main class="content-body custom-scrollbar">

      <div class="stats-grid">
        <StatCard num="1,243" label="Total Students" :icon="Users" color-class="blue-stat" />
        <StatCard :num="18" label="Active Clubs" :icon="Layers" color-class="green-stat" />
        <StatCard :num="47" label="Events This Month" :icon="CalendarCheck" color-class="pink-stat" />
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Registered College</h2>
          <StatusPill status="approved" label="Active" />
        </div>

        <div class="card">
          <div class="approval-card">
            <div class="approval-club-icon banner-blue">
              <School />
            </div>
            <div class="approval-info">
              <p class="approval-club-name">KNIT Sultanpur</p>
              <p class="approval-meta">Kamla Nehru Institute of Technology · Sultanpur, Uttar Pradesh · Active since 2024 · Domain: @knit.ac.in</p>
            </div>
            <div class="approval-actions">
              <StatusPill status="approved" label="Active" />
            </div>
          </div>
        </div>
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">College Settings</h2>
        </div>
        <div class="admin-settings-card">
          <div class="admin-settings-grid">
            <div class="form-group">
              <label for="college-name">College Name</label>
              <input type="text" id="college-name" v-model="collegeName" class="input-field">
            </div>
            <div class="form-group">
              <label for="full-name">Full Official Name</label>
              <input type="text" id="full-name" v-model="fullName" class="input-field">
            </div>
            <div class="form-group">
              <label for="email-domain">Verified Student Email Domain</label>
              <input type="text" id="email-domain" v-model="emailDomain" class="input-field">
            </div>
            <div class="form-group">
              <label for="admin-email">Admin Contact Email</label>
              <input type="email" id="admin-email" v-model="adminEmail" class="input-field">
            </div>
            <div class="form-group">
              <label for="city">City</label>
              <input type="text" id="city" v-model="city" class="input-field">
            </div>
            <div class="form-group">
              <label for="state">State</label>
              <input type="text" id="state" v-model="state" class="input-field">
            </div>
            <div class="form-group">
              <label for="max-clubs">Maximum Clubs Allowed</label>
              <input type="number" id="max-clubs" v-model="maxClubs" class="input-field">
            </div>
            <div class="form-group">
              <label for="max-members">Max Members per Club</label>
              <input type="number" id="max-members" v-model="maxMembers" class="input-field">
            </div>
          </div>
          <button class="btn-primary" @click="saveSettings">
            <Save /> Save Settings
          </button>
        </div>
      </div>

      <div>
        <div class="clubs-section-header">
          <h2 class="clubs-section-title">Allowed Club Categories</h2>
        </div>
        <div class="card">
          <p class="body-text">Configure which club categories students can register under at your institution.</p>
          <div class="clubs-section-header" style="margin-top: 14px; flex-wrap: wrap; gap: 8px;">
            <span v-for="category in allowedCategories" :key="category" class="cat-chip">{{ category }}</span>
          </div>
          <button class="btn-secondary" style="margin-top: 16px;" @click="showCategoryHint">
            <Pencil /> Manage Categories
          </button>
        </div>
      </div>

    </main>

  </div>
</template>
