import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import { useAuthStore } from '../stores/auth'
import { getMyClubs } from '../api/clubs'
import { getMyProfile } from '../api/students'

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

    // A student who has never filled in their profile is sent to onboarding
    // first. There is no "onboarded" flag on the account, so an empty branch
    // and no interests is what stands in for one - which means the screen
    // stops appearing by itself once the profile is saved.
    if (await needsOnboarding()) {
      router.push(`/${slug}/onboard`)
      return
    }

    if (auth.canManageClubs) {
      router.push(`/${slug}/leader/club`)
    } else {
      router.push(auth.homeRoute)
    }
  }

  async function needsOnboarding() {
    try {
      const profile = await getMyProfile()
      const hasInterests = Array.isArray(profile.interests) && profile.interests.length > 0

      return !profile.branch && !hasInterests
    } catch {
      // Never block sign-in on this check - if the profile cannot be read,
      // send the student to their normal landing page.
      return false
    }
  }

  return { completeSignIn }
}
