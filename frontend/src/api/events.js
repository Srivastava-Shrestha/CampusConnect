const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const mockEvents = [
  {
    id: 1,
    title: 'Line Follower Robot Build',
    club: 'Robotics & Automation Club',
    day: '12',
    month: 'Jul',
    time: '3:00 PM',
    venue: 'Main Lab',
    status: 'upcoming',
    accent: 'banner-orange',
    registered: 30,
    capacity: 50
  },
  {
    id: 2,
    title: 'Automation Hackathon 2026',
    club: 'Robotics & Automation Club',
    day: '19',
    month: 'Jul',
    time: '9:00 AM',
    venue: 'Seminar Hall',
    status: 'upcoming',
    accent: 'banner-orange',
    registered: 45,
    capacity: 80,
    about: 'Build an automation solution in 8 hours. Teams of 2 to 4 students will tackle real-world problem statements provided on the day. All experience levels welcome. Refreshments, mentorship sessions, and prizes for the top 3 teams.',
    dateLong: 'Saturday, 19 July 2026',
    timeLong: '9:00 AM to 6:00 PM',
    venueLong: 'Seminar Hall, Block A, KNIT Sultanpur',
    type: 'Hackathon',
    closesNote: 'Registration closes 18 July at 11:59 PM.'
  },
  {
    id: 3,
    title: 'Open Mic Night',
    club: 'Music Collective',
    day: '10',
    month: 'Jul',
    time: '6:00 PM',
    venue: 'Amphitheatre',
    status: 'registered',
    accent: 'banner-yellow',
    registered: 62,
    capacity: 100
  },
  {
    id: 4,
    title: 'Startup Pitch Night',
    club: 'Entrepreneurship Cell',
    day: '22',
    month: 'Jul',
    time: '5:00 PM',
    venue: 'Auditorium',
    status: 'upcoming',
    accent: 'banner-mint',
    registered: 18,
    capacity: 30
  },
  {
    id: 5,
    title: 'Introduction to Arduino',
    club: 'Robotics & Automation Club',
    day: '28',
    month: 'Jul',
    time: '2:00 PM',
    venue: 'Electronics Lab',
    status: 'upcoming',
    accent: 'banner-orange',
    registered: 12,
    capacity: 40
  },
  {
    id: 6,
    title: 'Photography Walk: Old City',
    club: 'Photography Circle',
    day: '8',
    month: 'Jul',
    time: '7:00 AM',
    venue: 'Main Gate',
    status: 'past',
    accent: 'banner-blue',
    registered: 28,
    capacity: 30
  }
]

const mockLeaderEvents = [
  {
    id: 1,
    title: 'Line Follower Robot Build',
    type: 'Workshop',
    day: '12',
    month: 'Jul',
    time: '3:00 PM',
    venue: 'Main Lab',
    status: 'upcoming',
    statusLabel: 'Upcoming',
    accent: 'banner-orange',
    countText: '30 / 50',
    action: 'attendance'
  },
  {
    id: 2,
    title: 'Automation Hackathon 2026',
    type: 'Hackathon',
    day: '19',
    month: 'Jul',
    time: '9:00 AM',
    venue: 'Seminar Hall',
    status: 'upcoming',
    statusLabel: 'Upcoming',
    accent: 'banner-orange',
    countText: '45 / 80',
    action: 'attendance'
  },
  {
    id: 5,
    title: 'Introduction to Arduino',
    type: 'Workshop',
    day: '28',
    month: 'Jul',
    time: '2:00 PM',
    venue: 'Electronics Lab',
    status: 'upcoming',
    statusLabel: 'Upcoming',
    accent: 'banner-orange',
    countText: '12 / 40',
    action: 'attendance'
  },
  {
    id: 7,
    title: 'IoT Project Showcase',
    type: 'Competition',
    day: '5',
    month: 'Jul',
    time: '4:00 PM',
    venue: 'Main Lab',
    status: 'needs-action',
    statusLabel: 'Needs Action',
    accent: 'banner-yellow',
    countText: '22 attended',
    action: 'set-results'
  },
  {
    id: 8,
    title: 'Circuit Design 101',
    type: 'Workshop',
    day: '28',
    month: 'Jun',
    time: '3:00 PM',
    venue: 'Electronics Lab',
    status: 'past',
    statusLabel: 'Completed',
    accent: 'banner-blue',
    countText: '36 attended',
    action: 'view-results'
  },
  {
    id: 9,
    title: 'Robotics Club Open House',
    type: 'Meet & Greet',
    day: '14',
    month: 'Jun',
    time: '11:00 AM',
    venue: 'Seminar Hall',
    status: 'past',
    statusLabel: 'Completed',
    accent: 'banner-mint',
    countText: '58 attended',
    action: 'view-results'
  }
]

const mockParticipants = [
  {
    id: 1,
    name: 'Shikha Singh',
    initials: 'SK',
    sub: 'CS · 1st Year',
    regId: 'CC-2026-0482'
  },
  {
    id: 2,
    name: 'Rishi Agarwal',
    initials: 'RA',
    sub: 'ECE · 2nd Year',
    regId: 'CC-2026-0491'
  },
  {
    id: 3,
    name: 'Neha Pandey',
    initials: 'NP',
    sub: 'IT · 2nd Year',
    regId: 'CC-2026-0503'
  },
  {
    id: 4,
    name: 'Aryan Kumar',
    initials: 'AK',
    sub: 'ME · 3rd Year',
    regId: 'CC-2026-0517'
  },
  {
    id: 5,
    name: 'Divya Mishra',
    initials: 'DM',
    sub: 'CS · 1st Year',
    regId: 'CC-2026-0528'
  },
  {
    id: 6,
    name: 'Pratham Verma',
    initials: 'PV',
    sub: 'ECE · 1st Year',
    regId: 'CC-2026-0534'
  },
  {
    id: 7,
    name: 'Simran Joshi',
    initials: 'SJ',
    sub: 'CS · 3rd Year',
    regId: 'CC-2026-0541'
  },
  {
    id: 8,
    name: 'Varun Tiwari',
    initials: 'VT',
    sub: 'IT · 2nd Year',
    regId: 'CC-2026-0556'
  }
]

// TODO: replace with real endpoint when backend is ready
export async function getLeaderEvents() {
  try {
    const response = await fetch(BASE_URL + '/events/managed')
    return await response.json()
  } catch (error) {
    return mockLeaderEvents
  }
}

// TODO: replace with real endpoint when backend is ready
export async function getEventParticipants(eventId) {
  try {
    const response = await fetch(BASE_URL + '/events/' + eventId + '/participants')
    return await response.json()
  } catch (error) {
    return mockParticipants
  }
}

export async function getEvents() {
  try {
    const response = await fetch(BASE_URL + '/events')

    if (!response.ok) {
      return mockEvents
    }

    return await response.json()
  } catch (error) {
    return mockEvents
  }
}

// TODO: replace with real endpoint when backend is ready
export async function getEventById(eventId) {
  try {
    const response = await fetch(BASE_URL + '/events/' + eventId)

    if (!response.ok) {
      return mockEvents.find(
        (event) => event.id === Number(eventId)
      ) || mockEvents[1]
    }

    return await response.json()
  } catch (error) {
    return mockEvents.find(
      (event) => event.id === Number(eventId)
    ) || mockEvents[1]
  }
}

// TODO: replace with real endpoint when backend is ready
export async function registerForEvent(eventId) {
  try {
    const response = await fetch(BASE_URL + '/events/' + eventId + '/register', { method: 'POST' })
    return await response.json()
  } catch (error) {
    return { ok: true, registrationId: 'CC-2026-0482' }
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

export { BASE_URL, mockEvents, mockLeaderEvents, mockParticipants }
