const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockMatches = [
  {
    id: 1,
    name: 'Robotics & Automation Club',
    reason: 'Matched because you mentioned building things with electronics and hands-on projects.'
  },
  {
    id: 2,
    name: 'Photography Circle',
    reason: 'Matched because you mentioned photography on weekends.'
  },
  {
    id: 6,
    name: 'Entrepreneurship Cell',
    reason: 'Matched because you mentioned wanting to meet people who care about startups.'
  }
]

// TODO: replace with real endpoint when backend is ready
export async function findMatchingClubs(interestsText) {
  try {
    const response = await fetch(BASE_URL + '/ai/find-clubs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ interests: interestsText })
    })
    return await response.json()
  } catch (error) {
    await simulateThinkingDelay()
    return mockMatches
  }
}

function simulateThinkingDelay() {
  return new Promise((resolve) => setTimeout(resolve, 1200))
}

export { BASE_URL, mockMatches }
