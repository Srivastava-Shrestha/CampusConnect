import { mockClubs } from './clubs'
import { mockEvents } from './events'
import { selectRecommendations } from '../utils/recommender'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// The backend's discovery DTOs (see backend/app/schemas/discovery.py) only
// carry the fields the design doc documents - id, name, category,
// description, activity_score, leader_name, tags for clubs; no banner
// colour or member count, since those are presentational, not data. Fill
// them in here so ClubCard/EventCard (built against the richer local mock
// shape) always have something to render.
const CARD_ACCENTS = ['banner-orange', 'banner-blue', 'banner-green', 'banner-yellow', 'banner-mint']

function accentFor(id) {
  return CARD_ACCENTS[id % CARD_ACCENTS.length]
}

function normalizeClub(club) {
  return {
    ...club,
    banner: club.banner || accentFor(club.id),
    members: club.members ?? club.activity_score ?? 0
  }
}

function normalizeEvent(event) {
  return {
    ...event,
    accent: event.accent || accentFor(event.id),
    day: event.day || '•',
    month: event.month || '',
    time: event.time || 'TBA',
    venue: event.venue || 'Ask the organiser',
    status: event.status || 'upcoming'
  }
}

function normalizeResult(result) {
  if (result.kind === 'event_fallback') {
    return { ...result, items: result.items.map(normalizeEvent) }
  }
  return { ...result, items: result.items.map(normalizeClub) }
}

// TODO: replace with real endpoint when the FastAPI backend is ready
export async function findMatchingClubs(interestText) {
  try {
    const response = await fetch(BASE_URL + '/ai/club-finder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ interest_text: interestText })
    })
    if (!response.ok) {
      throw new Error('Request failed: ' + response.status)
    }
    const result = await response.json()
    return normalizeResult(result)
  } catch (error) {
    await simulateThinkingDelay()
    return selectRecommendations(interestText, mockClubs, mockEvents)
  }
}

function simulateThinkingDelay() {
  return new Promise((resolve) => setTimeout(resolve, 1200))
}

export { BASE_URL }
