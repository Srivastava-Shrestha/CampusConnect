const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockClubs = [
  {
    id: 1,
    name: 'Robotics & Automation Club',
    members: 84,
    banner: 'banner-orange',
    icon: 'robot',
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
    icon: 'camera',
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
    icon: 'laptop',
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
    icon: 'music',
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
    icon: 'drama',
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
    icon: 'briefcase',
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
    icon: 'telescope',
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
    icon: 'sports',
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
    icon: 'dance',
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
  {
    id: 1,
    name: 'Robotics & Automation',
    sub: '84 members · Tech',
    banner: 'banner-orange',
    icon: 'robot',
    badge: '2 new events',
    alert: true
  },
  {
    id: 3,
    name: 'Coding Society',
    sub: '203 members · Tech',
    banner: 'banner-green',
    icon: 'laptop',
    badge: 'Hackathon this week',
    alert: true
  },
  {
    id: 2,
    name: 'Photography Circle',
    sub: '112 members · Arts',
    banner: 'banner-blue',
    icon: 'camera',
    badge: 'Member',
    alert: false
  },
  {
    id: 4,
    name: 'Music Collective',
    sub: '67 members · Music',
    banner: 'banner-yellow',
    icon: 'music',
    badge: 'Open mic Friday',
    alert: true
  }
]

const mockLeaderboard = {
  podium: [
    {
      rank: '2nd',
      tier: 'silver',
      name: 'Coding Society',
      score: '1,090',
      icon: 'laptop',
      category: 'tech'
    },
    {
      rank: '1st',
      tier: 'gold',
      name: 'Robotics & Automation',
      score: '1,240',
      icon: 'robot',
      category: 'tech'
    },
    {
      rank: '3rd',
      tier: 'bronze',
      name: 'Music Collective',
      score: '920',
      icon: 'music',
      category: 'culture'
    }
  ],
  rows: [
    {
      rank: 4,
      name: 'Photography Circle',
      cat: 'Arts · 38 members',
      score: 780,
      dot: 'banner-blue',
      icon: 'camera',
      category: 'arts'
    },
    {
      rank: 5,
      name: 'Entrepreneurship Cell',
      cat: 'Business · 54 members',
      score: 640,
      dot: 'banner-mint',
      icon: 'briefcase',
      category: 'business'
    },
    {
      rank: 6,
      name: 'Drama & Theatre Club',
      cat: 'Culture · 29 members',
      score: 520,
      dot: 'banner-pink',
      icon: 'drama',
      category: 'culture'
    },
    {
      rank: 7,
      name: 'Chess Club',
      cat: 'Sports · 22 members',
      score: 380,
      dot: 'banner-yellow',
      icon: 'chess',
      category: 'sports'
    },
    {
      rank: 8,
      name: 'Astronomy Club',
      cat: 'Tech · 17 members',
      score: 290,
      dot: 'banner-orange',
      icon: 'microscope',
      category: 'tech'
    },
    {
      rank: 9,
      name: 'Fine Arts Society',
      cat: 'Arts · 19 members',
      score: 210,
      dot: 'banner-mint',
      icon: 'palette',
      category: 'arts'
    },
    {
      rank: 10,
      name: 'Literary Circle',
      cat: 'Culture · 14 members',
      score: 160,
      dot: 'banner-yellow',
      icon: 'book',
      category: 'culture'
    }
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

const mockApprovals = [
  {
    id: 1,
    name: 'Astronomy Club',
    banner: 'banner-blue',
    icon: 'gear',
    status: 'pending',
    meta: 'Submitted by Dr. Priya Nair · Science · 2 days ago',
    metaFull: 'Submitted by Dr. Priya Nair · Science · 2 days ago · 12 founding members',
    applicationLink: 'https://drive.google.com/file/d/astronomy-club-application/view'
  },
  {
    id: 2,
    name: 'Chess Club',
    banner: 'banner-yellow',
    icon: 'chess',
    status: 'pending',
    meta: 'Submitted by Arjun Mehra · Culture · 4 days ago',
    metaFull: 'Submitted by Arjun Mehra · Culture · 4 days ago · 8 founding members',
    applicationLink: 'https://drive.google.com/file/d/chess-club-application/view'
  },
  {
    id: 3,
    name: 'Dance Fusion Club',
    banner: 'banner-pink',
    icon: 'dance',
    status: 'pending',
    meta: 'Submitted by Priyanka Das · Culture · 1 day ago',
    metaFull: 'Submitted by Priyanka Das · Culture · 1 day ago · 15 founding members',
    applicationLink: 'https://drive.google.com/file/d/dance-fusion-application/view'
  },
  {
    id: 4,
    name: 'Robotics & Automation Club',
    banner: 'banner-orange',
    icon: 'robot',
    status: 'approved',
    meta: 'Submitted by Aayansh Yadav · Tech · Approved 14 Jan 2026 · 84 members',
    metaFull: 'Submitted by Aayansh Yadav · Tech · Approved 14 Jan 2026 · 84 members',
    applicationLink: 'https://drive.google.com/file/d/robotics-club-application/view'
  },
  {
    id: 5,
    name: 'Photography Circle',
    banner: 'banner-blue',
    icon: 'camera',
    status: 'approved',
    meta: 'Submitted by Meera Krishnan · Arts · Approved 3 Feb 2026 · 112 members',
    metaFull: 'Submitted by Meera Krishnan · Arts · Approved 3 Feb 2026 · 112 members',
    applicationLink: 'https://drive.google.com/file/d/photography-circle-application/view'
  },
  {
    id: 6,
    name: 'Cricket Betting Analysis Club',
    banner: 'banner-mint',
    icon: 'medal',
    status: 'rejected',
    meta: 'Submitted by Rahul Bose · Sports · Rejected 5 Apr 2026 · Reason: club name and stated objectives violate campus policy',
    metaFull: 'Submitted by Rahul Bose · Sports · Rejected 5 Apr 2026 · Reason: club name and stated objectives violate campus policy',
    applicationLink: 'https://drive.google.com/file/d/cricket-analysis-application/view'
  }
]

// TODO: replace with real endpoint when backend is ready
export async function getClubApprovals() {
  try {
    const response = await fetch(BASE_URL + '/clubs/approvals')
    return await response.json()
  } catch (error) {
    return mockApprovals
  }
}

// TODO: replace with real endpoint when backend is ready
export async function approveClubRequest(approvalId) {
  try {
    const response = await fetch(BASE_URL + '/clubs/approvals/' + approvalId + '/approve', { method: 'POST' })
    return await response.json()
  } catch (error) {
    return { ok: true, status: 'approved' }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function rejectClubRequest(approvalId, reason) {
  try {
    const response = await fetch(BASE_URL + '/clubs/approvals/' + approvalId + '/reject', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason })
    })
    return await response.json()
  } catch (error) {
    return { ok: true, status: 'rejected', reason }
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

export { BASE_URL, mockClubs, mockJoinedClubs, mockLeaderboard, mockApprovals }
