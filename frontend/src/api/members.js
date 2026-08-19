const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockMembers = [
  {
    id: 1,
    name: 'Shikha Singh',
    initials: 'SK',
    sub: 'Computer Science · 1st Year · Joined Jun 2026',
    role: 'member',
    roleLabel: 'Member'
  },
  {
    id: 2,
    name: 'Rishi Agarwal',
    initials: 'RA',
    sub: 'Electronics · 2nd Year · Joined Jan 2026',
    role: 'officer',
    roleLabel: 'Officer'
  },
  {
    id: 3,
    name: 'Neha Pandey',
    initials: 'NP',
    sub: 'Information Technology · 2nd Year · Joined Feb 2026',
    role: 'member',
    roleLabel: 'Member'
  },
  {
    id: 4,
    name: 'Aryan Kumar',
    initials: 'AK',
    sub: 'Mechanical Engg · 3rd Year · Joined Sep 2025',
    role: 'officer',
    roleLabel: 'Officer'
  },
  {
    id: 5,
    name: 'Divya Mishra',
    initials: 'DM',
    sub: 'Computer Science · 1st Year · Joined Jun 2026',
    role: 'member',
    roleLabel: 'Member'
  },
  {
    id: 6,
    name: 'Varun Tiwari',
    initials: 'VT',
    sub: 'Information Technology · 2nd Year · Joined Mar 2026',
    role: 'member',
    roleLabel: 'Member'
  }
]

const mockJoinRequests = [
  {
    id: 1,
    name: 'Priya Sharma',
    initials: 'PS',
    sub: 'Computer Science · 2nd Year · Requested 1 day ago'
  },
  {
    id: 2,
    name: 'Rahul Gupta',
    initials: 'RG',
    sub: 'Electronics · 1st Year · Requested 2 days ago'
  },
  {
    id: 3,
    name: 'Ananya Das',
    initials: 'AD',
    sub: 'Information Technology · 3rd Year · Requested 3 days ago'
  }
]

// TODO: replace with real endpoint when backend is ready
export async function getMembers(clubId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/members')
    if (!response.ok) {
      throw new Error('Request failed: ' + response.status)
    }
    return await response.json()
  } catch (error) {
    return mockMembers
  }
}

// TODO: replace with real endpoint when backend is ready
export async function getJoinRequests(clubId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/join-requests')
    if (!response.ok) {
      throw new Error('Request failed: ' + response.status)
    }
    return await response.json()
  } catch (error) {
    return mockJoinRequests
  }
}

// TODO: replace with real endpoint when backend is ready
export async function approveJoinRequest(clubId, requestId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/join-requests/' + requestId + '/approve', { method: 'POST' })
    if (!response.ok) {
      throw new Error('Request failed: ' + response.status)
    }
    return await response.json()
  } catch (error) {
    return { ok: true, approved: requestId }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function rejectJoinRequest(clubId, requestId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/join-requests/' + requestId + '/reject', { method: 'POST' })
    if (!response.ok) {
      throw new Error('Request failed: ' + response.status)
    }
    return await response.json()
  } catch (error) {
    return { ok: true, rejected: requestId }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function removeMember(clubId, memberId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/members/' + memberId, { method: 'DELETE' })
    if (!response.ok) {
      throw new Error('Request failed: ' + response.status)
    }
    return await response.json()
  } catch (error) {
    return { ok: true, removed: memberId }
  }
}

export { BASE_URL, mockMembers, mockJoinRequests }
