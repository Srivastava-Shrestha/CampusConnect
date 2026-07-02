const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockClubs = [
  {
    id: 1,
    name: 'Robotics & Automation Club',
    members: 84,
    banner: 'banner-orange',
    description: 'Build real robots, compete in national-level challenges, and work on automation projects with peers.',
    tags: ['Robotics', 'IoT', 'Tech'],
    category: 'Tech',
    recommended: true
  },
  {
    id: 2,
    name: 'Coding Society',
    members: 203,
    banner: 'banner-green',
    description: 'Hackathons, competitive programming contests, and open-source contribution drives every semester.',
    tags: ['Coding', 'Open Source', 'Tech'],
    category: 'Tech',
    recommended: true
  },
  {
    id: 3,
    name: 'Entrepreneurship Cell',
    members: 91,
    banner: 'banner-mint',
    description: 'Startup pitches, founder talks, and mentorship sessions with working entrepreneurs and investors.',
    tags: ['Startup', 'Business'],
    category: 'Business',
    recommended: true
  }
]

// TODO: replace with real endpoint when backend is ready
export async function getClubs() {
  try {
    const response = await fetch(BASE_URL + '/clubs')
    return await response.json()
  } catch (error) {
    return mockClubs
  }
}

// TODO: replace with real endpoint when backend is ready
export async function getClubById(clubId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId)
    return await response.json()
  } catch (error) {
    return mockClubs.find((club) => club.id === Number(clubId)) || mockClubs[0]
  }
}

// TODO: replace with real endpoint when backend is ready
export async function requestToJoinClub(clubId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/' + clubId + '/join', { method: 'POST' })
    return await response.json()
  } catch (error) {
    return { ok: true, status: 'pending' }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function createClub(clubData) {
  try {
    const response = await fetch(BASE_URL + '/clubs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(clubData)
    })
    return await response.json()
  } catch (error) {
    return { ok: true, status: 'pending_approval', club: clubData }
  }
}

export { BASE_URL, mockClubs }
