import { defineStore } from 'pinia'
import { getEvents, getEventById } from '../api/events'

export const useEventsStore = defineStore('events', {
  state: () => ({
    events: [],
    currentEvent: null,
    loaded: false
  }),

  getters: {
    upcomingEvents: (state) => state.events.filter((event) => event.status === 'upcoming')
  },

  actions: {
    async loadEvents() {
      if (this.loaded) return
      this.events = await getEvents()
      this.loaded = true
    },

    async loadEvent(eventId) {
      this.currentEvent = await getEventById(eventId)
    }
  }
})
