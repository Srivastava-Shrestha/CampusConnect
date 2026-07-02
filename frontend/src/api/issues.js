const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockIssues = [
  {
    id: 1,
    title: 'Practice room double booked',
    club: 'Music Club',
    status: 'open',
    body: 'The practice room was double booked twice this week.',
    response: ''
  },
  {
    id: 2,
    title: 'Certificate name misspelled',
    club: 'Coding Society',
    status: 'resolved',
    body: 'My name is misspelled on the hackathon certificate.',
    response: 'A corrected certificate has been issued.'
  }
]

// TODO: replace with real endpoint when backend is ready
export async function getIssues() {
  try {
    const response = await fetch(BASE_URL + '/issues')
    return await response.json()
  } catch (error) {
    return mockIssues
  }
}

// TODO: replace with real endpoint when backend is ready
export async function raiseIssue(issue) {
  try {
    const response = await fetch(BASE_URL + '/issues', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(issue)
    })
    return await response.json()
  } catch (error) {
    return { ok: true, issue: { ...issue, status: 'open' } }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function replyToIssue(issueId, reply) {
  try {
    const response = await fetch(BASE_URL + '/issues/' + issueId + '/reply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reply })
    })
    return await response.json()
  } catch (error) {
    return { ok: true, status: 'in_progress', reply }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function resolveIssue(issueId) {
  try {
    const response = await fetch(BASE_URL + '/issues/' + issueId + '/resolve', { method: 'PATCH' })
    return await response.json()
  } catch (error) {
    return { ok: true, status: 'resolved' }
  }
}

export { BASE_URL, mockIssues }
