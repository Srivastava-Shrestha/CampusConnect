const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const mockIssues = [
  {
    id: 1,
    title: 'Registration ID not received after signing up for Open Mic Night',
    meta: 'Music Collective · Event · Raised 2 days ago',
    status: 'open',
    statusLabel: 'Open',
    desc: 'I registered for Open Mic Night on 8 July but never received a confirmation email with my Registration ID. The registration page showed success but I have no record of the ID. I need it to enter the event.',
    tags: ['Event', 'Registration'],
    response: null
  },
  {
    id: 2,
    title: 'Event date conflict between Arduino Workshop and CS Lab mid-semester exam',
    meta: 'Robotics & Automation Club · Event · Raised 5 days ago',
    status: 'in-progress',
    statusLabel: 'In Progress',
    desc: 'The Introduction to Arduino workshop on 28 July clashes with our department\'s mid-semester practical exam for CS3401. Many first-year CS students will not be able to attend. Could the date be moved or an alternate slot be offered?',
    tags: ['Event', 'Scheduling'],
    response: {
      by: 'Aayansh Yadav',
      text: 'Thanks for flagging this. I have contacted the department office to confirm the practical schedule. We will announce a revised date by 14 July. Your attendance will not be marked if the exam clashes.'
    }
  },
  {
    id: 3,
    title: 'Cannot find meeting minutes from June club general body session',
    meta: 'Robotics & Automation Club · Club · Raised 12 days ago',
    status: 'resolved',
    statusLabel: 'Resolved',
    desc: 'The minutes from the June 18 general body meeting were supposed to be shared on the club page but I cannot find them. I need them for the project proposal I am submitting.',
    tags: ['Club', 'Documents'],
    response: {
      by: 'Aayansh Yadav',
      text: 'Sorry for the delay. Minutes have been uploaded to the club page under Documents. I have also emailed the PDF to all members. Issue closed.'
    }
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
    return { ok: true, status: 'in-progress', reply }
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
