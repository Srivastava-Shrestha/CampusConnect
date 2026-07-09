import { mockClubs } from './clubs'
import { mockEvents } from './events'
import { selectRecommendations } from '../utils/recommender'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// TODO: replace with real endpoint when the FastAPI backend is ready
export async function findMatchingClubs(interestText) {
  try {
    const response = await fetch(BASE_URL + '/ai/club-finder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ interest_text: interestText })
    })
    return await response.json()
  } catch (error) {
    await simulateThinkingDelay()
    return selectRecommendations(interestText, mockClubs, mockEvents)
  }
}

function simulateThinkingDelay() {
  return new Promise((resolve) => setTimeout(resolve, 1200))
}

export { BASE_URL }
