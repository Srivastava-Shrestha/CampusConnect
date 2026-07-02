const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockAnnouncements = [
  {
    id: 1,
    title: 'RoboWars registrations open',
    club: 'Robotics & Automation Club',
    category: 'Tech',
    body: 'Registrations for RoboWars 2026 are now open. Limited slots available.',
    pinned: true,
    unread: true
  },
  {
    id: 2,
    title: 'Weekly coding contest this Saturday',
    club: 'Coding Society',
    category: 'Tech',
    body: 'Join us for the weekly contest. Top three win goodies.',
    pinned: false,
    unread: false
  }
]

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

export { BASE_URL, mockAnnouncements }
