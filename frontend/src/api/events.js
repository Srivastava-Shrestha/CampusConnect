const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockEvents = [
  {
    id: 1,
    title: 'RoboWars 2026',
    club: 'Robotics & Automation Club',
    date: '2026-07-18',
    status: 'upcoming',
    registered: false
  },
  {
    id: 2,
    title: 'CodeSprint Hackathon',
    club: 'Coding Society',
    date: '2026-07-25',
    status: 'upcoming',
    registered: true
  }
]

// TODO: replace with real endpoint when backend is ready
export async function getEvents() {
  try {
    const response = await fetch(BASE_URL + '/events')
    return await response.json()
  } catch (error) {
    return mockEvents
  }
}

// TODO: replace with real endpoint when backend is ready
export async function getEventById(eventId) {
  try {
    const response = await fetch(BASE_URL + '/events/' + eventId)
    return await response.json()
  } catch (error) {
    return mockEvents.find((event) => event.id === Number(eventId)) || mockEvents[0]
  }
}

// TODO: replace with real endpoint when backend is ready
export async function registerForEvent(eventId) {
  try {
    const response = await fetch(BASE_URL + '/events/' + eventId + '/register', { method: 'POST' })
    return await response.json()
  } catch (error) {
    return { ok: true, registrationId: 'REG-2026-000' + eventId }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function createEvent(eventData) {
  try {
    const response = await fetch(BASE_URL + '/events', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(eventData)
    })
    return await response.json()
  } catch (error) {
    return { ok: true, event: eventData }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function saveAttendance(eventId, presentIds) {
  try {
    const response = await fetch(BASE_URL + '/events/' + eventId + '/attendance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ presentIds })
    })
    return await response.json()
  } catch (error) {
    return { ok: true, marked: presentIds.length }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function saveResults(eventId, results) {
  try {
    const response = await fetch(BASE_URL + '/events/' + eventId + '/results', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ results })
    })
    return await response.json()
  } catch (error) {
    return { ok: true, published: true }
  }
}

// TODO: Razorpay integration is deferred to a later milestone
export async function payForEvent(eventId, amount) {
  return { ok: true, eventId, amount, paymentStatus: 'simulated' }
}

export { BASE_URL, mockEvents }
