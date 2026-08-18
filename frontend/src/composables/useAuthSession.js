import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import { useAuthStore } from '../stores/auth'
import { getMyClubs } from '../api/clubs'

export function useAuthSession() {
  const router = useRouter()
  const auth = useAuthStore()

  async function completeSignIn(result) {
    auth.setToken(result.access_token)

    const payload = jwtDecode(result.access_token)
    const role = payload.role?.toUpperCase()

    auth.setUser({
      name: payload.full_name,
      email: payload.email,
      collegeSlug: payload.college_slug,
      collegeName: auth.user.collegeName,
      initials: (payload.full_name || '')
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase()
    })

    auth.setRole(
      role === 'ADMIN' || role === 'CAMPUS_ADMIN' ? 'admin' : 'student'
    )

    if (auth.role === 'student') {
      try {
        const ledClubs = await getMyClubs({ role: 'LEADER' })
        auth.setClubLeader(ledClubs.length > 0)
      } catch {
        auth.setClubLeader(false)
      }
    }

    if (auth.role === 'admin') {
      router.push(payload.college_slug ? `/${payload.college_slug}/admin` : '/admin/onboard')
      return
    }

    const slug = payload.college_slug
    if (auth.canManageClubs) {
      router.push(`/${slug}/leader/club`)
    } else {
      router.push(auth.homeRoute)
    }
  }

  return { completeSignIn }
}
