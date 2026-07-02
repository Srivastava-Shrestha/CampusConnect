import { defineStore } from 'pinia'

const personas = {
  student: {
    name: 'Shikha Singh',
    sub: 'CS · 1st Year',
    initials: 'SK',
    college: 'KNIT Sultanpur'
  },
  leader: {
    name: 'Aayansh Yadav',
    sub: 'Leader · Robotics Club',
    initials: 'AY',
    college: 'KNIT Sultanpur'
  },
  admin: {
    name: 'Student Affairs',
    sub: 'Admin · KNIT Sultanpur',
    initials: 'SA',
    college: 'KNIT Sultanpur'
  }
}

const roleHomes = {
  student: '/clubs',
  leader: '/leader/club',
  admin: '/admin'
}

function readStoredRole() {
  const stored = localStorage.getItem('cc_role')
  if (stored === 'leader' || stored === 'admin') {
    return stored
  }
  return 'student'
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    role: readStoredRole(),
    token: localStorage.getItem('cc_token') || '',
    user: personas[readStoredRole()]
  }),

  getters: {
    isLoggedIn: (state) => state.role !== '',
    homeRoute: (state) => roleHomes[state.role] || '/login'
  },

  actions: {
    setRole(role) {
      if (!personas[role]) {
        return
      }
      this.role = role
      this.user = personas[role]
      localStorage.setItem('cc_role', role)
    },

    setToken(token) {
      this.token = token
      localStorage.setItem('cc_token', token)
    },

    logout() {
      this.role = ''
      this.token = ''
      this.user = null
      localStorage.removeItem('cc_role')
      localStorage.removeItem('cc_token')
    }
  }
})

export { personas, roleHomes }
