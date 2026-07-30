const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'


async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("cc_token")

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {})
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || error.message || "Request failed")
  }

  if (response.status === 204) {
  return null
  }

  return response.json()
}



export async function getClubs() {
  return apiRequest("/clubs")
}

export async function getMyClubs(params = {}) {
  const query = new URLSearchParams(params).toString()

  return apiRequest(`/clubs/me${query ? `?${query}` : ""}`)
}

export async function getClubById(clubId) {
  return apiRequest(`/clubs/${clubId}`)
}

export async function requestToJoinClub(clubId) {
  return apiRequest(`/clubs/${clubId}/join`, {
    method: "POST"
  })
}

export async function createClub(clubData) {
  return apiRequest("/clubs", {
    method: "POST",
    body: JSON.stringify(clubData)
  })
}

export async function updateClub(clubId, clubData) {
  return apiRequest(`/clubs/${clubId}`, {
    method: "PUT",
    body: JSON.stringify(clubData)
  })
}

export async function deleteClub(clubId) {
  return apiRequest(`/clubs/${clubId}`, {
    method: "DELETE"
  })
}

export async function getClubMembers(clubId) {
  return apiRequest(`/clubs/${clubId}/members`)
}

export async function getPendingRequests(clubId) {
  return apiRequest(`/clubs/${clubId}/requests`)
}

export async function handleMembershipRequest(
  clubId,
  membershipId,
  action
) {
  return apiRequest(`/clubs/${clubId}/requests/${membershipId}`, {
    method: "PATCH",
    body: JSON.stringify({
      action
    })
  })
}

  const mockLeaderboard = {
  podium: [
    {
      rank: '2nd',
      tier: 'silver',
      name: 'Coding Society',
      score: '1,090',
      icon: 'laptop',
      category: 'tech'
    },
    {
      rank: '1st',
      tier: 'gold',
      name: 'Robotics & Automation',
      score: '1,240',
      icon: 'robot',
      category: 'tech'
    },
    {
      rank: '3rd',
      tier: 'bronze',
      name: 'Music Collective',
      score: '920',
      icon: 'music',
      category: 'culture'
    }
  ],
  rows: [
    {
      rank: 4,
      name: 'Photography Circle',
      cat: 'Arts · 38 members',
      score: 780,
      dot: 'banner-blue',
      icon: 'camera',
      category: 'arts'
    },
    {
      rank: 5,
      name: 'Entrepreneurship Cell',
      cat: 'Business · 54 members',
      score: 640,
      dot: 'banner-mint',
      icon: 'briefcase',
      category: 'business'
    },
    {
      rank: 6,
      name: 'Drama & Theatre Club',
      cat: 'Culture · 29 members',
      score: 520,
      dot: 'banner-pink',
      icon: 'drama',
      category: 'culture'
    },
    {
      rank: 7,
      name: 'Chess Club',
      cat: 'Sports · 22 members',
      score: 380,
      dot: 'banner-yellow',
      icon: 'chess',
      category: 'sports'
    },
    {
      rank: 8,
      name: 'Astronomy Club',
      cat: 'Tech · 17 members',
      score: 290,
      dot: 'banner-orange',
      icon: 'microscope',
      category: 'tech'
    },
    {
      rank: 9,
      name: 'Fine Arts Society',
      cat: 'Arts · 19 members',
      score: 210,
      dot: 'banner-mint',
      icon: 'palette',
      category: 'arts'
    },
    {
      rank: 10,
      name: 'Literary Circle',
      cat: 'Culture · 14 members',
      score: 160,
      dot: 'banner-yellow',
      icon: 'book',
      category: 'culture'
    }
  ]
}

export async function getClubApprovals() {
  return apiRequest("/clubs?status=PENDING")
}

export async function approveClubRequest(clubId) {
  return apiRequest(`/clubs/${clubId}/approve`, {
    method: "PATCH"
  })
}

export async function rejectClubRequest(clubId) {
  return apiRequest(`/clubs/${clubId}/reject`, {
    method: "PATCH"
  })
}

// TODO: replace with real endpoint when backend is ready
export async function getLeaderboard() {
  try {
    return await apiRequest("/clubs/leaderboard")
  } catch (error) {
    return mockLeaderboard
  }
}

export { BASE_URL }
