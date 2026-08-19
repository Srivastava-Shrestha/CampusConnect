const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function extractMessage(body) {
  // AppException replies with {"message": ...}; FastAPI validation errors reply
  // with {"detail": [{msg, loc}, ...]} and auth failures with {"detail": "..."}.
  if (typeof body.message === 'string') return body.message
  if (typeof body.detail === 'string') return body.detail
  if (Array.isArray(body.detail) && body.detail.length) {
    return body.detail[0].msg || 'Request failed'
  }
  return 'Request failed'
}

async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem('cc_token')

  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers })

  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(extractMessage(body))
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

function buildQuery(params) {
  const query = new URLSearchParams()

  Object.keys(params).forEach(function appendParam(key) {
    const value = params[key]
    if (value !== undefined && value !== null && value !== '') {
      query.append(key, value)
    }
  })

  const queryString = query.toString()
  return queryString ? `?${queryString}` : ''
}

export async function getEvents(filters = {}) {
  return apiRequest(`/events${buildQuery(filters)}`)
}

export async function getEventById(eventId) {
  return apiRequest(`/events/${eventId}`)
}

// Event create/update take multipart/form-data for the same reason club
// create/update do: a JSON string in `data` plus an optional `image` file.
// Content-Type stays unset so the browser supplies the multipart boundary.
async function multipartRequest(endpoint, method, payload, image) {
  const token = localStorage.getItem('cc_token')
  const headers = {}

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const form = new FormData()
  form.append('data', JSON.stringify(payload))

  if (image) {
    form.append('image', image)
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, { method, headers, body: form })

  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(extractMessage(body))
  }

  return response.json()
}

export async function createEvent(eventData, image = null) {
  return multipartRequest('/events', 'POST', eventData, image)
}

export async function updateEvent(eventId, eventData, image = null) {
  return multipartRequest(`/events/${eventId}`, 'PUT', eventData, image)
}

export async function publishEvent(eventId) {
  return apiRequest(`/events/${eventId}/publish`, { method: 'PATCH' })
}

export async function cancelEvent(eventId) {
  return apiRequest(`/events/${eventId}/cancel`, { method: 'PATCH' })
}

export async function registerForEvent(eventId) {
  return apiRequest(`/events/${eventId}/register`, { method: 'POST' })
}

export async function unregisterFromEvent(eventId) {
  return apiRequest(`/events/${eventId}/register`, { method: 'DELETE' })
}

export async function getEventParticipants(eventId) {
  return apiRequest(`/events/${eventId}/registrations`)
}

export async function markAttendance(eventId, registrationId, checkedIn) {
  return apiRequest(`/events/${eventId}/registrations/${registrationId}/attendance`, {
    method: 'PATCH',
    body: JSON.stringify({ checked_in: checkedIn })
  })
}

export async function setResult(eventId, registrationId, result) {
  return apiRequest(`/events/${eventId}/registrations/${registrationId}/result`, {
    method: 'PATCH',
    body: JSON.stringify({ result })
  })
}

export async function getMyRegistrations() {
  return apiRequest('/events/me/registrations')
}

export async function getMyResults() {
  return apiRequest('/events/me/results')
}

// TODO: Razorpay integration is deferred to a later milestone
export async function payForEvent(eventId, amount) {
  return { ok: true, eventId, amount, paymentStatus: 'simulated' }
}

// ==== presentation helpers ====
// The API speaks ISO timestamps and a DRAFT/PUBLISHED/CANCELLED lifecycle, while the
// cards were built around a split date box and an upcoming/registered/past pill. The
// shape is adapted here in one place instead of in every view.

const ACCENTS = [
  'banner-orange',
  'banner-blue',
  'banner-mint',
  'banner-yellow',
  'banner-pink',
  'banner-green'
]

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

const WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

const MONTHS_LONG = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

export function accentForClub(clubId) {
  return ACCENTS[Math.abs(Number(clubId) || 0) % ACCENTS.length]
}

export function formatTime(date) {
  const hours = date.getHours()
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const suffix = hours >= 12 ? 'PM' : 'AM'
  const hour12 = hours % 12 === 0 ? 12 : hours % 12

  return `${hour12}:${minutes} ${suffix}`
}

export function formatDateLong(date) {
  return `${WEEKDAYS[date.getDay()]}, ${date.getDate()} ${MONTHS_LONG[date.getMonth()]} ${date.getFullYear()}`
}

export function deriveStatus(event, registeredEventIds = new Set()) {
  if (event.status === 'CANCELLED') return 'cancelled'
  if (event.status === 'DRAFT') return 'draft'
  if (new Date(event.ends_at) < new Date()) return 'past'
  if (event.is_registered || registeredEventIds.has(event.id)) return 'registered'
  return 'upcoming'
}

export function normalizeEvent(event, registeredEventIds = new Set()) {
  const startsAt = new Date(event.starts_at)
  const endsAt = new Date(event.ends_at)

  return {
    id: event.id,
    club_id: event.club_id,
    club: event.club_name,
    title: event.title,
    description: event.description || '',
    venue: event.venue,
    day: String(startsAt.getDate()),
    month: MONTHS[startsAt.getMonth()],
    time: formatTime(startsAt),
    dateLong: formatDateLong(startsAt),
    timeLong: `${formatTime(startsAt)} to ${formatTime(endsAt)}`,
    starts_at: event.starts_at,
    ends_at: event.ends_at,
    capacity: event.capacity,
    registered: event.registration_count,
    seats_left: event.seats_left,
    image_url: event.image_url,
    lifecycle: event.status,
    status: deriveStatus(event, registeredEventIds),
    accent: accentForClub(event.club_id),
    is_registered: event.is_registered === true || registeredEventIds.has(event.id),
    my_registration_id: event.my_registration_id ?? null
  }
}

export function initialsOf(fullName) {
  return String(fullName || '')
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((word) => word[0])
    .join('')
    .toUpperCase()
}

function yearLabel(year) {
  const suffixes = { 1: 'st', 2: 'nd', 3: 'rd' }
  return `${year}${suffixes[year] || 'th'} Year`
}

export function normalizeParticipant(participant) {
  const details = []
  if (participant.branch) details.push(participant.branch)
  if (participant.year) details.push(yearLabel(participant.year))
  if (!details.length && participant.roll_no) details.push(participant.roll_no)

  return {
    id: participant.registration_id,
    registration_id: participant.registration_id,
    student_id: participant.student_id,
    name: participant.full_name,
    initials: initialsOf(participant.full_name),
    sub: details.join(' · ') || participant.email,
    regId: `#${participant.registration_id}`,
    email: participant.email,
    checked_in: participant.checked_in,
    checked_in_at: participant.checked_in_at,
    result: participant.result,
    registered_at: participant.registered_at
  }
}

export { BASE_URL }
