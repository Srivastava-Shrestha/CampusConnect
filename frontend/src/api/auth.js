const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

async function postJson(path, payload) {
  const response = await fetch(BASE_URL + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  if (!response.ok) {
    throw new Error('Request failed: ' + response.status)
  }
  return response.json()
}

// TODO: replace with real endpoint when backend is ready
export async function loginUser(email, password) {
  try {
    return await postJson('/auth/login', { email, password })
  } catch (error) {
    return { ok: true, token: 'mock-token', role: 'student', email }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function signupUser(name, email, password, role) {
  try {
    return await postJson('/auth/signup', { name, email, password, role })
  } catch (error) {
    return { ok: true, name, email, role }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function verifyEmailOtp(email, code) {
  try {
    return await postJson('/auth/verify-email', { email, code })
  } catch (error) {
    return { ok: true, verified: true }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function resendOtp(email) {
  try {
    return await postJson('/auth/resend-otp', { email })
  } catch (error) {
    return { ok: true, sent: true }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function sendResetLink(email) {
  try {
    return await postJson('/auth/forgot-password', { email })
  } catch (error) {
    return { ok: true, sent: true }
  }
}

// TODO: replace with real endpoint when backend is ready
export async function saveOnboarding(profile) {
  try {
    return await postJson('/auth/onboarding', profile)
  } catch (error) {
    return { ok: true, saved: true }
  }
}

export { BASE_URL }
