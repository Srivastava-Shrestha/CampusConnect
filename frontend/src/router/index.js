import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { startLoading, finishLoading } from '../composables/useLoadingBar'

const publicRoutes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: {
      role: 'public',
      bodyClass: 'landing-body'
    }
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../views/SignupView.vue'),
    meta: {
      role: 'public',
      bodyClass: 'auth-body'
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    meta: {
      role: 'public',
      bodyClass: 'auth-body'
    }
  },
  {
    path: '/forgot-password',
    name: 'forgot-password',
    component: () => import('../views/ForgotPasswordView.vue'),
    meta: {
      role: 'public',
      bodyClass: 'auth-body'
    }
  },
  {
    path: '/verify-email',
    name: 'verify-email',
    component: () => import('../views/VerifyEmailView.vue'),
    meta: {
      role: 'public',
      bodyClass: 'auth-body'
    }
  },
  {
    path: '/verify/:serial',
    name: 'verify-cert',
    component: () => import('../views/VerifyCertView.vue'),
    meta: {
      role: 'public',
      bodyClass: 'verify-body'
    }
  },
  {
    path: '/cert/view',
    name: 'view-cert',
    component: () => import('../views/ViewCertView.vue'),
    meta: {
      role: 'public',
      bodyClass: 'cert-viewer-body'
    }
  }
]

const studentRoutes = [
  {
    path: '/onboard',
    name: 'onboard',
    component: () => import('../views/OnboardView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'onboard-body'
    }
  },
  {
    path: '/clubs',
    name: 'clubs',
    component: () => import('../views/ClubDirectoryView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/clubs/:id',
    name: 'club-profile',
    component: () => import('../views/ClubProfileView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/find-clubs',
    name: 'find-clubs',
    component: () => import('../views/FindClubsView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/events',
    name: 'events',
    component: () => import('../views/EventsView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/events/:id',
    name: 'event-detail',
    component: () => import('../views/EventDetailView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/announcements',
    name: 'announcements',
    component: () => import('../views/AnnouncementsView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/issues',
    name: 'issues',
    component: () => import('../views/IssuesView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/profile',
    name: 'profile',
    component: () => import('../views/ProfileView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leaderboard',
    name: 'leaderboard',
    component: () => import('../views/LeaderboardView.vue'),
    meta: {
      role: 'student',
      bodyClass: 'portal-body'
    }
  }
]

const leaderRoutes = [
  {
    path: '/leader/club',
    name: 'leader-club',
    component: () => import('../views/LeaderClubView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/events',
    name: 'leader-events',
    component: () => import('../views/LeaderEventsView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/events/new',
    name: 'create-event',
    component: () => import('../views/CreateEventView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/events/:id/attend',
    name: 'attendance',
    component: () => import('../views/AttendanceView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/events/:id/results',
    name: 'results',
    component: () => import('../views/ResultsView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/members',
    name: 'members',
    component: () => import('../views/MembersView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/announcements',
    name: 'leader-announcements',
    component: () => import('../views/LeaderAnnouncementsView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/announcements/new',
    name: 'post-announcement',
    component: () => import('../views/PostAnnouncementView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/issues',
    name: 'leader-issues',
    component: () => import('../views/LeaderIssuesView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/leader/clubs/new',
    name: 'create-club',
    component: () => import('../views/CreateClubView.vue'),
    meta: {
      role: 'leader',
      bodyClass: 'portal-body'
    }
  }
]

const adminRoutes = [
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../views/AdminOverviewView.vue'),
    meta: {
      role: 'admin',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/admin/approvals',
    name: 'admin-approvals',
    component: () => import('../views/AdminApprovalsView.vue'),
    meta: {
      role: 'admin',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/admin/colleges',
    name: 'admin-colleges',
    component: () => import('../views/AdminCollegesView.vue'),
    meta: {
      role: 'admin',
      bodyClass: 'portal-body'
    }
  },
  {
    path: '/admin/guidelines',
    name: 'admin-guidelines',
    component: () => import('../views/AdminGuidelinesView.vue'),
    meta: {
      role: 'admin',
      bodyClass: 'portal-body'
    }
  }
]

const routes = [
  ...publicRoutes,
  ...studentRoutes,
  ...leaderRoutes,
  ...adminRoutes
]

function resolveGuardTarget(routeMeta, auth) {
  if (routeMeta.role === 'public') {
    return null
  }

  if (!auth.isLoggedIn) {
    return '/login'
  }

  // Club-leader pages are reachable by a member who leads a club, since
  // leadership is no longer a separate login role.
  if (routeMeta.role === 'leader') {
    if (auth.canManageClubs) {
      return null
    }
    return auth.homeRoute
  }

  if (auth.role !== routeMeta.role) {
    return auth.homeRoute
  }

  return null
}

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(function guardByRole(to) {
  startLoading()

  const auth = useAuthStore()
  const target = resolveGuardTarget(to.meta, auth)

  if (target && target !== to.path) {
    return target
  }

  return true
})

router.afterEach(function stopProgress() {
  finishLoading()
})

router.onError(function stopProgressOnError() {
  finishLoading()
})

export default router
export { routes, resolveGuardTarget }
