const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockCertificates = [
  {
    serial: 'CC-CERT-2026-1841',
    name: 'Shikha Singh',
    event: 'Photography Walk: Old City',
    club: 'Photography Circle',
    result: 'participant',
    resultLabel: 'Participant',
    date: '8 July 2026',
    dateShort: '8 Jul 2026',
    college: 'KNIT Sultanpur',
    leader: 'Aayansh Yadav'
  },
  {
    serial: 'CC-CERT-2026-0293',
    name: 'Shikha Singh',
    event: 'Open Mic Night Spring Edition',
    club: 'Music Collective',
    result: 'participant',
    resultLabel: 'Participant',
    date: '15 March 2026',
    dateShort: '15 Mar 2026',
    college: 'KNIT Sultanpur',
    leader: 'Aayansh Yadav'
  }
]

const mockCertDatabase = {
  'CC-CERT-2026-1841': {
    name: 'Shikha Singh',
    event: 'Photography Walk: Old City',
    club: 'Photography Circle',
    result: 'Participant',
    date: '8 July 2026'
  },
  'CC-CERT-2026-0293': {
    name: 'Shikha Singh',
    event: 'Open Mic Night — Spring Edition',
    club: 'Music Collective',
    result: 'Participant',
    date: '15 March 2026'
  },
  'CC-CERT-2026-0512': {
    name: 'Rishi Agarwal',
    event: 'Automation Hackathon 2026',
    club: 'Robotics & Automation Club',
    result: 'Winner',
    date: '19 July 2026'
  },
  'CC-CERT-2026-0513': {
    name: 'Neha Pandey',
    event: 'Automation Hackathon 2026',
    club: 'Robotics & Automation Club',
    result: 'Runner-up',
    date: '19 July 2026'
  }
}

// TODO: replace with real endpoint when backend is ready
export async function getMyCertificates() {
  try {
    const response = await fetch(BASE_URL + '/certificates/me')
    if (!response.ok) {
      throw new Error('Request failed: ' + response.status)
    }
    return await response.json()
  } catch (error) {
    return mockCertificates
  }
}

// TODO: replace with real endpoint when backend is ready
export async function verifyCertificate(serial) {
  try {
    const response = await fetch(BASE_URL + '/certificates/verify/' + serial)
    if (!response.ok) {
      throw new Error('Request failed: ' + response.status)
    }
    return await response.json()
  } catch (error) {
    const found = findCertificateBySerial(serial)
    if (found) {
      return { ok: true, valid: true, certificate: found }
    }
    return { ok: true, valid: false }
  }
}

function findCertificateBySerial(serial) {
  const cleaned = String(serial).trim().toUpperCase()
  const found = mockCertDatabase[cleaned]

  if (!found) {
    return null
  }

  return { serial: cleaned, ...found }
}

export { BASE_URL, mockCertificates, mockCertDatabase, findCertificateBySerial }
