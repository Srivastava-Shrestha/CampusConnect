const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockCertificates = [
  {
    serial: 'CC-2026-RB-0042',
    name: 'Shikha Singh',
    event: 'RoboWars 2026',
    club: 'Robotics & Automation Club',
    result: 'Winner',
    date: '2026-03-14',
    college: 'KNIT Sultanpur',
    leader: 'Aayansh Yadav'
  },
  {
    serial: 'CC-2026-CS-0107',
    name: 'Shikha Singh',
    event: 'CodeSprint Hackathon',
    club: 'Coding Society',
    result: 'Participant',
    date: '2026-02-02',
    college: 'KNIT Sultanpur',
    leader: 'Pawan Kumar'
  }
]

// TODO: replace with real endpoint when backend is ready
export async function getMyCertificates() {
  try {
    const response = await fetch(BASE_URL + '/certificates/me')
    return await response.json()
  } catch (error) {
    return mockCertificates
  }
}

// TODO: replace with real endpoint when backend is ready
export async function verifyCertificate(serial) {
  try {
    const response = await fetch(BASE_URL + '/certificates/verify/' + serial)
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
  return mockCertificates.find((cert) => cert.serial === cleaned) || null
}

export { BASE_URL, mockCertificates, findCertificateBySerial }
