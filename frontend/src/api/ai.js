const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockMatches = [
  {
    id: 1,
    name: 'Robotics & Automation Club',
    reason: 'You mentioned building things and hardware. This club runs hands-on robot builds every month.'
  },
  {
    id: 2,
    name: 'Coding Society',
    reason: 'Your interest in problem solving fits their weekly competitive programming contests.'
  },
  {
    id: 3,
    name: 'Entrepreneurship Cell',
    reason: 'You want to turn ideas into projects. Their startup pitch nights are a great starting point.'
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
