import { mockClubs } from './clubs'
import { mockEvents } from './events'
import { selectRecommendations } from '../utils/recommender'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// The backend's discovery DTOs (see backend/app/schemas/discovery.py) carry
// only real/derived data fields - for clubs: id, name, category, description,
// activity_score, leader_name, tags; for events: id, club_id, title,
// description, venue, starts_at, club_name, leader_name. Presentational bits
// the cards need (banner colour, member count, date parts) are derived here so
// ClubCard/EventCard always have something to render.
const CARD_ACCENTS = ['banner-orange', 'banner-blue', 'banner-green', 'banner-yellow', 'banner-mint']
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

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
  const startsAt = event.starts_at ? new Date(event.starts_at) : null
  const isValidDate = startsAt && !Number.isNaN(startsAt.getTime())

  return {
    ...event,
    accent: event.accent || accentFor(event.id),
    club: event.club || event.club_name || '',
    day: event.day || (isValidDate ? String(startsAt.getDate()) : '•'),
    month: event.month || (isValidDate ? MONTHS[startsAt.getMonth()] : ''),
    time: event.time || (isValidDate
      ? startsAt.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
      : 'TBA'),
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
