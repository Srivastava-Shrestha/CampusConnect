const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockAnnouncements = [
  {
    id: 1,
    club: 'Robotics & Automation Club',
    dot: 'banner-orange',
    emoji: '\u{1F916}',
    time: '2 hours ago',
    title: 'Hackathon preparations: what to bring on the day',
    body: 'The Automation Hackathon is on 19 July. Please arrive by 8:45 AM at Seminar Hall, Block A for check-in. Bring your student ID and your Registration ID (CC-2026-XXXX). Teams of 2 to 4 are confirmed at the gate. Laptops with Arduino IDE pre-installed are strongly recommended. Power strips will be provided per table.',
    tags: ['Hackathon', 'Important'],
    category: 'tech',
    pinned: true,
    unread: true
  },
  {
    id: 2,
    club: 'Music Collective',
    dot: 'banner-yellow',
    emoji: '\u{1F3B5}',
    time: 'Yesterday at 5:30 PM',
    title: 'Open Mic Night is this Friday, last call for performers',
    body: 'We still have 3 open slots for performers at Open Mic Night (Jul 10, Amphitheatre, 6 PM). If you want to sing, recite, or play an instrument for 5 to 8 minutes, reply to this announcement or DM the club email before Thursday midnight. Audience registrations are open until capacity fills.',
    tags: ['Open Mic', 'Culture'],
    category: 'culture',
    pinned: false,
    unread: true
  },
  {
    id: 3,
    club: 'Robotics & Automation Club',
    dot: 'banner-orange',
    emoji: '\u{1F916}',
    time: '3 days ago',
    title: 'New equipment now available in the Main Lab',
    body: 'We have received 4 new Raspberry Pi 4 kits and a set of servo motor modules thanks to the department grant. These are available for club project use with booking. Use the equipment register sheet kept at the lab entrance. Return by the deadline noted in the register or your booking slot will be revoked.',
    tags: ['Lab', 'Resources'],
    category: 'tech',
    pinned: false,
    unread: false
  },
  {
    id: 4,
    club: 'Photography Circle',
    dot: 'banner-blue',
    emoji: '\u{1F4F7}',
    time: '5 days ago',
    title: 'Photo Walk recap, thank you for joining us',
    body: 'A huge thank you to all 28 members who joined the Old City Photo Walk on 8 July. We covered Masjid Gully, the Old Clock Tower, and the riverside market at dawn. Selected shots from the walk will be featured in our next digital zine. Submit your best 3 photos to our club email by 15 July.',
    tags: ['Event Recap', 'Photography'],
    category: 'event',
    pinned: false,
    unread: false
  },
  {
    id: 5,
    club: 'Coding Society',
    dot: 'banner-mint',
    emoji: '\u{1F4BB}',
    time: '1 week ago',
    title: 'Competitive programming series starts next Monday',
    body: 'Starting 7 July, every Monday at 4 PM in CS Lab 2, we will run weekly competitive programming practice sessions on Codeforces. Problems will be rated 800 to 1400 for beginners and 1500 to 2000 for advanced. All skill levels welcome. Bring your laptop. First session will cover complexity analysis and greedy algorithms.',
    tags: ['Workshop', 'Competitive'],
    category: 'tech',
    pinned: false,
    unread: false
  }
]

const mockLeaderAnnouncements = [
  {
    id: 1,
    club: 'Robotics & Automation Club',
    dot: 'banner-orange',
    emoji: '\u{1F916}',
    time: '2 hours ago',
    title: 'Hackathon preparations: what to bring on the day',
    body: 'The Automation Hackathon is on 19 July. Please arrive by 8:45 AM at Seminar Hall, Block A for check-in. Bring your student ID and your Registration ID. Teams of 2 to 4 are confirmed at the gate. Laptops with Arduino IDE pre-installed are strongly recommended.',
    tags: ['Hackathon', 'Important'],
    category: 'tech',
    pinned: true,
    unread: false
  },
  {
    id: 2,
    club: 'Robotics & Automation Club',
    dot: 'banner-orange',
    emoji: '\u{1F916}',
    time: '3 days ago',
    title: 'New equipment now available in the Main Lab',
    body: 'We have received 4 new Raspberry Pi 4 kits and a set of servo motor modules thanks to the department grant. These are available for club project use with booking. Use the equipment register sheet kept at the lab entrance.',
    tags: ['Lab', 'Resources'],
    category: 'tech',
    pinned: false,
    unread: false
  },
  {
    id: 3,
    club: 'Robotics & Automation Club',
    dot: 'banner-orange',
    emoji: '\u{1F916}',
    time: '5 days ago',
    title: 'Registrations open for Line Follower Robot Build',
    body: 'We are running our next hands-on workshop on 12 July in the Main Lab. All experience levels are welcome. Slots are limited to 50 participants. Register on the Events page and carry your student ID on the day. Materials will be provided.',
    tags: ['Workshop', 'Registration'],
    category: 'event',
    pinned: false,
    unread: false
  },
  {
    id: 4,
    club: 'Robotics & Automation Club',
    dot: 'banner-orange',
    emoji: '\u{1F916}',
    time: '1 week ago',
    title: 'Project submission deadline extended to 20 July',
    body: 'Due to requests from several teams, the final project submission deadline for the semester mini-project has been extended by one week to 20 July. Please upload your project report and working demo video to the shared drive link sent to members.',
    tags: ['Projects', 'Deadline'],
    category: 'tech',
    pinned: false,
    unread: false
  },
  {
    id: 5,
    club: 'Robotics & Automation Club',
    dot: 'banner-orange',
    emoji: '\u{1F916}',
    time: '2 weeks ago',
    title: 'Club anniversary celebration recap and photo gallery link',
    body: 'Thank you to everyone who joined our 7th anniversary celebration last week. It was a wonderful evening. Photos from the event have been compiled into a gallery linked in the club bio. Please share and tag your fellow members.',
    tags: ['Anniversary', 'Community'],
    category: 'culture',
    pinned: false,
    unread: false
  }
]

// TODO: replace with real endpoint when backend is ready
export async function getLeaderAnnouncements() {
  try {
    const response = await fetch(BASE_URL + '/announcements/mine')
    return await response.json()
  } catch (error) {
    return mockLeaderAnnouncements
  }
}

// TODO: replace with real endpoint when backend is ready
export async function getAnnouncements() {
  try {
    const response = await fetch(BASE_URL + '/announcements')
    return await response.json()
  } catch (error) {
    return mockAnnouncements
  }
}

// TODO: replace with real endpoint when backend is ready
export async function postAnnouncement(announcement) {
  try {
    const response = await fetch(BASE_URL + '/announcements', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(announcement)
    })
    return await response.json()
  } catch (error) {
    return { ok: true, announcement }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function togglePin(announcementId, pinned) {
  try {
    const response = await fetch(BASE_URL + '/announcements/' + announcementId + '/pin', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pinned })
    })
    return await response.json()
  } catch (error) {
    return { ok: true, pinned }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function deleteAnnouncement(announcementId) {
  try {
    const response = await fetch(BASE_URL + '/announcements/' + announcementId, { method: 'DELETE' })
    return await response.json()
  } catch (error) {
    return { ok: true, deleted: announcementId }
  }
}

export { BASE_URL, mockAnnouncements, mockLeaderAnnouncements }
