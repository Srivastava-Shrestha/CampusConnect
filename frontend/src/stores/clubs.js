import { defineStore } from 'pinia'
import { getClubs, getJoinedClubs, getClubById } from '../api/clubs'

export const useClubsStore = defineStore('clubs', {
  state: () => ({
    clubs: [],
    joinedClubs: [],
    currentClub: null,
    loaded: false
  }),

  getters: {
    recommendedClubs: (state) => state.clubs.filter((club) => club.recommended)
  },

  actions: {
    async loadClubs() {
      if (this.loaded) return
      this.clubs = await getClubs()
      this.joinedClubs = await getJoinedClubs()
      this.loaded = true
    },

    async loadClub(clubId) {
      this.currentClub = await getClubById(clubId)
    }
  }
})
