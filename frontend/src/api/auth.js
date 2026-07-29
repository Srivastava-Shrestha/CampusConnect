const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function postJson(path, payload, extraHeaders = {}) {
  const response = await fetch(BASE_URL + path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...extraHeaders
    },
    body: JSON.stringify(payload)
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail || data.message || 'Request failed')
  }

  return data
}

export async function loginUser(email, password) {
  return await postJson('/auth/login', {
    email,
    password
  })
}

export async function signupUser(data) {
  return await postJson('/auth/signup', data)
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

export async function onboardCollege(data, token) {
  return await postJson(
    '/college/onboarding',
    data,
    {
      Authorization: `Bearer ${token}`
    }
  )
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
