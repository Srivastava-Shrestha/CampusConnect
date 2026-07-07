<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Pin, PinOff, Trash2, Megaphone } from 'lucide-vue-next'
import StudentSidebar from '../components/layout/StudentSidebar.vue'
import LeaderTopNav from '../components/layout/LeaderTopNav.vue'
import Topbar from '../components/layout/Topbar.vue'
import AnnounceCard from '../components/ui/AnnounceCard.vue'
import FilterChips from '../components/ui/FilterChips.vue'
import { getLeaderAnnouncements, togglePin, deleteAnnouncement } from '../api/announcements'

const router = useRouter()

const posts = ref([])
const activeFilter = ref('all')

const filterChips = [
  { id: 'all', label: 'All' },
  { id: 'pinned', label: 'Pinned' },
  { id: 'tech', label: 'Tech' },
  { id: 'culture', label: 'Culture' },
  { id: 'event', label: 'Events' }
]

const visiblePosts = computed(function filterPosts() {
  return posts.value.filter(function matchesFilter(post) {
    if (activeFilter.value === 'all') {
      return true
    }

    if (activeFilter.value === 'pinned') {
      return post.pinned
    }

    return post.category === activeFilter.value
  })
})

async function handleTogglePin(post) {
  const newPinnedState = !post.pinned

  await togglePin(post.id, newPinnedState)
  post.pinned = newPinnedState
}

async function handleDelete(post) {
  const confirmed = window.confirm('Delete this announcement? Members will no longer see it.')
  if (!confirmed) {
    return
  }

  await deleteAnnouncement(post.id)
  posts.value = posts.value.filter(function keepOthers(item) {
    return item.id !== post.id
  })
}

function goToPostAnnouncement() {
  router.push('/leader/announcements/new')
}

onMounted(async function loadPosts() {
  posts.value = await getLeaderAnnouncements()
})
</script>

<template>
  <StudentSidebar />

  <div class="main-content">
    <LeaderTopNav />

    <Topbar title="Announcements" sub="Posted by Robotics & Automation Club">
      <button class="btn-primary" @click="goToPostAnnouncement">
        <Plus /> Post Announcement
      </button>
    </Topbar>

    <main class="content-body custom-scrollbar">

      <div class="announce-layout">
        <div>

          <FilterChips :chips="filterChips" v-model="activeFilter" />

          <div class="announce-feed">
            <AnnounceCard
              v-for="post in visiblePosts"
              :key="post.id"
              :announcement="post"
            >
              <template #actions>
                <div class="announce-manage-row">
                  <button class="announce-action-btn" @click="handleTogglePin(post)">
                    <PinOff v-if="post.pinned" />
                    <Pin v-else />
                    {{ post.pinned ? 'Unpin' : 'Pin' }}
                  </button>
                  <button class="announce-action-btn delete" @click="handleDelete(post)">
                    <Trash2 /> Delete
                  </button>
                </div>
              </template>
            </AnnounceCard>
          </div>

          <div v-if="visiblePosts.length === 0" class="empty-state">
            <Megaphone />
            <p>No announcements match this filter.</p>
          </div>

        </div>
      </div>

    </main>

  </div>
</template>
