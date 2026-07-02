<script setup>
import { ref, computed, onMounted } from 'vue'
import { Megaphone } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import AnnounceCard from '../components/ui/AnnounceCard.vue'
import FilterChips from '../components/ui/FilterChips.vue'
import { getAnnouncements } from '../api/announcements'
import { useChipFilter } from '../composables/useChipFilter'

const announcements = ref([])

const filterChips = [
  { id: 'all', label: 'All' },
  { id: 'pinned', label: 'Pinned' },
  { id: 'tech', label: 'Tech' },
  { id: 'culture', label: 'Culture' },
  { id: 'event', label: 'Events' }
]

const announcementsList = computed(() => announcements.value)

const { activeFilter, filteredItems } = useChipFilter(announcementsList, function matchesCategory(announcement, filter) {
  if (filter === 'pinned') return announcement.pinned
  return announcement.category === filter
})

onMounted(async function loadFeed() {
  announcements.value = await getAnnouncements()
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content">

    <Topbar title="Announcements" sub="Updates from your clubs" />

    <main class="content-body custom-scrollbar">

      <div class="announce-layout">

        <div>
          <FilterChips :chips="filterChips" v-model="activeFilter" />

          <div class="announce-feed">
            <AnnounceCard
              v-for="announcement in filteredItems"
              :key="announcement.id"
              :announcement="announcement"
            />
          </div>

          <div v-if="filteredItems.length === 0" class="empty-state">
            <Megaphone />
            <p>No announcements match this filter.</p>
          </div>
        </div>

      </div>

    </main>

  </div>
</template>
