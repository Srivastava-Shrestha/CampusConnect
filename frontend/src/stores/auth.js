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
  // Only two account types log in now: a member (student) or an institute admin.
  // Club leadership is a capability layered on a member account, not a login role.
  const stored = localStorage.getItem('cc_role')
  if (stored === 'admin') {
    return stored
  }
  return 'student'
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    role: readStoredRole(),
    token: localStorage.getItem('cc_token') || '',
    user: personas[readStoredRole()],
    // Whether this member also leads at least one club. In the real app this
    // comes from the backend after login; kept true here so the leader tools
    // are reachable in the mock build.
    isClubLeader: true
  }),

  getters: {
    isLoggedIn: (state) => state.role !== '',
    homeRoute: (state) => roleHomes[state.role] || '/login',
    // A member who leads a club may open the club-leader tools.
    canManageClubs: (state) => state.role === 'student' && state.isClubLeader
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
