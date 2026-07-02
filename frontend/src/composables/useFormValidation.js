export function useFormValidation() {
  function isValidEmail(email) {
    const trimmed = String(email).trim()
    return trimmed.length > 0 && trimmed.includes('@')
  }

  function allFieldsFilled(fields) {
    return Object.values(fields).every(function checkField(value) {
      return String(value).trim().length > 0
    })
  }

  function isStrongEnough(password) {
    return String(password).length >= 6
  }

  return { isValidEmail, allFieldsFilled, isStrongEnough }
}
