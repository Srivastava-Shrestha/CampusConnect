import { defineStore } from 'pinia'
import { getClubs, getMyClubs, getClubById } from "../api/clubs"

export const useClubsStore = defineStore('clubs', {
  state: () => ({
    clubs: [],
    joinedClubs: [],
    currentClub: null,
    loaded: false
  }),

  getters: {
    recommendedClubs: (state) => {
      const joinedIds = new Set(state.joinedClubs.map(club => club.id))

      return state.clubs.filter(club => !joinedIds.has(club.id))
}
  },

  actions: {
  async loadClubs() {
  if (this.loaded) return

  try {
    const clubs = await getClubs()
    this.clubs = Array.isArray(clubs) ? clubs : []
  } catch (error) {
    console.error("Failed to load clubs:", error)
    this.clubs = []
  }

  try {
    const myClubs = await getMyClubs()

    this.joinedClubs = Array.isArray(myClubs)
      ? myClubs.filter(club => club.status !== 'ARCHIVED')
      : []

} catch (error) {
    console.error("Failed to load my clubs:", error)
    this.joinedClubs = []
}

  this.loaded = true
},

  async refreshClubs() {
    this.loaded = false
    await this.loadClubs()
},
  async loadClub(clubId) {
    try {
    this.currentClub = await getClubById(clubId)
  } catch (error) {
    console.error("Failed to load club:", error)
    this.currentClub = null
  }
}
  }
})
