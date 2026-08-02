<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Plus, Pin, PinOff, Trash2, Megaphone } from 'lucide-vue-next'
import LeaderSidebar from '../components/layout/LeaderSidebar.vue'
import Topbar from '../components/layout/Topbar.vue'
import AnnounceCard from '../components/ui/AnnounceCard.vue'
import FilterChips from '../components/ui/FilterChips.vue'
import { getLeaderAnnouncements, togglePin, deleteAnnouncement } from '../api/announcements'
import { toast } from '../composables/useToast'

const router = useRouter()
const route = useRoute()

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
  try {
    const newPinnedState = !post.pinned

    await togglePin(post.id, newPinnedState)
    post.pinned = newPinnedState
  } catch (error) {
    toast.error(error.message)
  }
}

async function handleDelete(post) {
  const confirmed = window.confirm(
    'Delete this announcement? Members will no longer see it.'
  )

  if (!confirmed) {
    return
  }

  try {
    await deleteAnnouncement(post.id)

    posts.value = posts.value.filter(function keepOthers(item) {
      return item.id !== post.id
    })
  } catch (error) {
    toast.error(error.message)
  }
}

function goToPostAnnouncement() {
  router.push(`/${route.params.slug}/leader/announcements/new`)
}

onMounted(async function loadPosts() {
  try {
    posts.value = await getLeaderAnnouncements()
  } catch (error) {
    toast.error(error.message)
  }
})
</script>

<template>
  <LeaderSidebar />

  <div class="main-content">

    <Topbar title="Announcements" :sub="club ? `Posted by ${club.name}` : 'Loading...'">
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
