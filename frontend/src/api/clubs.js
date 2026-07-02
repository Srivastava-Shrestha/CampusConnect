const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockClubs = [
  {
    id: 1,
    name: 'Robotics & Automation Club',
    members: 84,
    banner: 'banner-orange',
    emoji: '\u{1F916}',
    description: 'Build real robots, compete in national-level challenges, and work on automation projects with peers.',
    tags: ['Robotics', 'IoT', 'Tech'],
    category: 'Tech',
    recommended: true,
    founded: 2019,
    eventsRun: 12,
    college: 'KNIT Sultanpur',
    about: 'We are a student-run community focused on robotics, embedded systems, and automation. Our members participate in national-level robotics competitions, build IoT projects, and run weekly hands-on workshops. Whether you have zero experience or are already building things, you will find a project to contribute to.'
  },
  {
    id: 2,
    name: 'Photography Circle',
    members: 112,
    banner: 'banner-blue',
    emoji: '\u{1F4F7}',
    description: 'Weekly photo walks, darkroom sessions, and monthly critique workshops for all skill levels.',
    tags: ['Photography', 'Arts'],
    category: 'Arts',
    recommended: false,
    founded: 2017,
    eventsRun: 21,
    college: 'KNIT Sultanpur',
    about: 'A community of photographers of every level. We organise weekly photo walks, darkroom sessions, and monthly critique workshops.'
  },
  {
    id: 3,
    name: 'Coding Society',
    members: 203,
    banner: 'banner-green',
    emoji: '\u{1F4BB}',
    description: 'Hackathons, competitive programming contests, and open-source contribution drives every semester.',
    tags: ['Coding', 'Open Source', 'Tech'],
    category: 'Tech',
    recommended: true,
    founded: 2015,
    eventsRun: 34,
    college: 'KNIT Sultanpur',
    about: 'The largest technical club on campus. We run hackathons, competitive programming contests, and open-source contribution drives every semester.'
  },
  {
    id: 4,
    name: 'Music Collective',
    members: 67,
    banner: 'banner-yellow',
    emoji: '\u{1F3B5}',
    description: 'Jam sessions, open mic nights, and collaborative song writing across all genres and instruments.',
    tags: ['Music', 'Performance'],
    category: 'Music',
    recommended: false,
    founded: 2018,
    eventsRun: 18,
    college: 'KNIT Sultanpur',
    about: 'Jam sessions, open mic nights, and collaborative song writing across all genres and instruments.'
  },
  {
    id: 5,
    name: 'Drama Society',
    members: 45,
    banner: 'banner-pink',
    emoji: '\u{1F3AD}',
    description: 'Annual theatre productions, improv workshops, and script writing bootcamps through the year.',
    tags: ['Theatre', 'Writing'],
    category: 'Arts',
    recommended: false,
    founded: 2016,
    eventsRun: 9,
    college: 'KNIT Sultanpur',
    about: 'Annual theatre productions, improv workshops, and script writing bootcamps through the year.'
  },
  {
    id: 6,
    name: 'Entrepreneurship Cell',
    members: 91,
    banner: 'banner-mint',
    emoji: '\u{1F4BC}',
    description: 'Startup pitches, founder talks, and mentorship sessions with working entrepreneurs and investors.',
    tags: ['Startup', 'Business'],
    category: 'Business',
    recommended: true,
    founded: 2020,
    eventsRun: 15,
    college: 'KNIT Sultanpur',
    about: 'Startup pitches, founder talks, and mentorship sessions with working entrepreneurs and investors.'
  },
  {
    id: 7,
    name: 'Astronomy Club',
    members: 38,
    banner: 'banner-blue',
    emoji: '\u{1F52D}',
    description: 'Telescope nights, space documentaries, and participation in national Astronomy Olympiads every year.',
    tags: ['Space', 'Science'],
    category: 'Science',
    recommended: false,
    founded: 2021,
    eventsRun: 7,
    college: 'KNIT Sultanpur',
    about: 'Telescope nights, space documentaries, and participation in national Astronomy Olympiads every year.'
  },
  {
    id: 8,
    name: 'Sports Council',
    members: 156,
    banner: 'banner-orange',
    emoji: '\u{26BD}',
    description: 'Coordinates inter-college tournaments, fitness events, and weekly sports leagues on campus.',
    tags: ['Sports', 'Fitness'],
    category: 'Sports',
    recommended: false,
    founded: 2014,
    eventsRun: 28,
    college: 'KNIT Sultanpur',
    about: 'Coordinates inter-college tournaments, fitness events, and weekly sports leagues on campus.'
  },
  {
    id: 9,
    name: 'Bharatnatyam & Folk Dance',
    members: 72,
    banner: 'banner-yellow',
    emoji: '\u{1F483}',
    description: 'Classical and folk dance training, cultural fest performances, and inter-college dance competitions.',
    tags: ['Dance', 'Culture'],
    category: 'Culture',
    recommended: false,
    founded: 2019,
    eventsRun: 11,
    college: 'KNIT Sultanpur',
    about: 'Classical and folk dance training, cultural fest performances, and inter-college dance competitions.'
  }
]

const mockJoinedClubs = [
  { id: 1, name: 'Robotics & Automation', sub: '84 members · Tech', banner: 'banner-orange', emoji: '\u{1F916}', badge: '2 new events', alert: true },
  { id: 3, name: 'Coding Society', sub: '203 members · Tech', banner: 'banner-green', emoji: '\u{1F4BB}', badge: 'Hackathon this week', alert: true },
  { id: 2, name: 'Photography Circle', sub: '112 members · Arts', banner: 'banner-blue', emoji: '\u{1F4F7}', badge: 'Member', alert: false },
  { id: 4, name: 'Music Collective', sub: '67 members · Music', banner: 'banner-yellow', emoji: '\u{1F3B5}', badge: 'Open mic Friday', alert: true }
]

const mockLeaderboard = {
  podium: [
    { rank: '2nd', tier: 'silver', name: 'Coding Society', score: '1,090', emoji: '\u{1F4BB}', category: 'tech' },
    { rank: '1st', tier: 'gold', name: 'Robotics & Automation', score: '1,240', emoji: '\u{1F916}', category: 'tech' },
    { rank: '3rd', tier: 'bronze', name: 'Music Collective', score: '920', emoji: '\u{1F3B5}', category: 'culture' }
  ],
  rows: [
    { rank: 4, name: 'Photography Circle', cat: 'Arts · 38 members', score: 780, dot: 'banner-blue', emoji: '\u{1F4F7}', category: 'arts' },
    { rank: 5, name: 'Entrepreneurship Cell', cat: 'Business · 54 members', score: 640, dot: 'banner-mint', emoji: '\u{1F4BC}', category: 'business' },
    { rank: 6, name: 'Drama & Theatre Club', cat: 'Culture · 29 members', score: 520, dot: 'banner-pink', emoji: '\u{1F3AA}', category: 'culture' },
    { rank: 7, name: 'Chess Club', cat: 'Sports · 22 members', score: 380, dot: 'banner-yellow', emoji: '\u{265E}\u{FE0F}', category: 'sports' },
    { rank: 8, name: 'Astronomy Club', cat: 'Tech · 17 members', score: 290, dot: 'banner-orange', emoji: '\u{1F52C}', category: 'tech' },
    { rank: 9, name: 'Fine Arts Society', cat: 'Arts · 19 members', score: 210, dot: 'banner-mint', emoji: '\u{1F3A8}', category: 'arts' },
    { rank: 10, name: 'Literary Circle', cat: 'Culture · 14 members', score: 160, dot: 'banner-yellow', emoji: '\u{1F97A}', category: 'culture' }
  ]
}

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
export async function getJoinedClubs() {
  try {
    const response = await fetch(BASE_URL + '/clubs/joined')
    return await response.json()
  } catch (error) {
    return mockJoinedClubs
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

// TODO: replace with real endpoint when backend is ready
export async function getLeaderboard() {
  try {
    const response = await fetch(BASE_URL + '/clubs/leaderboard')
    return await response.json()
  } catch (error) {
    return mockLeaderboard
  }
}

export { BASE_URL, mockClubs, mockJoinedClubs, mockLeaderboard }
