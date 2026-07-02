const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockMembers = [
  { id: 1, name: 'Priya Sharma', sub: 'ECE · 2nd Year', initials: 'PS', role: 'Officer' },
  { id: 2, name: 'Rahul Verma', sub: 'ME · 3rd Year', initials: 'RV', role: 'Member' }
]

const mockJoinRequests = [
  { id: 11, name: 'Shikha Singh', sub: 'CS · 1st Year', initials: 'SK' }
]

// TODO: replace with real endpoint when backend is ready
export async function getMembers(clubId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/members')
    return await response.json()
  } catch (error) {
    return mockMembers
  }
}

// TODO: replace with real endpoint when backend is ready
export async function getJoinRequests(clubId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/join-requests')
    return await response.json()
  } catch (error) {
    return mockJoinRequests
  }
}

// TODO: replace with real endpoint when backend is ready
export async function approveJoinRequest(clubId, requestId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/join-requests/' + requestId + '/approve', { method: 'POST' })
    return await response.json()
  } catch (error) {
    return { ok: true, approved: requestId }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function rejectJoinRequest(clubId, requestId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/join-requests/' + requestId + '/reject', { method: 'POST' })
    return await response.json()
  } catch (error) {
    return { ok: true, rejected: requestId }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function removeMember(clubId, memberId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/members/' + memberId, { method: 'DELETE' })
    return await response.json()
  } catch (error) {
    return { ok: true, removed: memberId }
  }
}

export { BASE_URL, mockMembers, mockJoinRequests }
