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
