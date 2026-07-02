<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { GraduationCap, CheckCircle2 } from 'lucide-vue-next'
import { verifyEmailOtp, resendOtp } from '../api/auth'

const router = useRouter()

const otpDigits = ref(['', '', '', '', '', ''])
const otpInputs = ref([])
const emailHint = ref('your college email')
const resendLabel = ref('Resend')
const resendDisabled = ref(false)

function showEmailHint() {
  const saved = sessionStorage.getItem('signupEmail')
  if (saved) {
    emailHint.value = saved
  }
}

function handleOtpInput(index) {
  const typed = otpDigits.value[index]

  if (typed.length > 1) {
    otpDigits.value[index] = typed.slice(-1)
  }

  if (otpDigits.value[index].length === 1 && index < 5) {
    otpInputs.value[index + 1].focus()
  }
}

function handleOtpBackspace(index) {
  if (otpDigits.value[index] === '' && index > 0) {
    otpInputs.value[index - 1].focus()
  }
}

function getOtpValue() {
  return otpDigits.value.join('')
}

function clearOtpBoxes() {
  otpDigits.value = ['', '', '', '', '', '']
  otpInputs.value[0].focus()
}

async function handleVerify() {
  const otp = getOtpValue()

  if (otp.length < 6) {
    window.alert('Please enter all 6 digits of the OTP.')
    return
  }

  await verifyEmailOtp(emailHint.value, otp)
  router.push('/onboard')
}

async function handleResend() {
  resendLabel.value = 'Sent!'
  resendDisabled.value = true
  clearOtpBoxes()
  await resendOtp(emailHint.value)

  setTimeout(function restoreResendLink() {
    resendLabel.value = 'Resend'
    resendDisabled.value = false
  }, 5000)
}

onMounted(function focusFirstBox() {
  showEmailHint()
  otpInputs.value[0].focus()
})
</script>

<template>
  <div class="auth-frame">

    <aside class="auth-sidebar orange-auth">

      <div class="auth-sidebar-logo" @click="router.push('/')">
        <div class="auth-sidebar-logo-mark">
          <GraduationCap />
        </div>
        <span class="brand">Campus Connect</span>
      </div>

      <div>
        <h2 class="auth-sidebar-title">Almost<br>there.</h2>
        <p class="auth-sidebar-desc">
          One quick step to confirm you are a verified student of your institution.
        </p>
      </div>

      <div class="auth-sidebar-circle-1"></div>

      <div class="auth-sidebar-char">
        <svg class="svg-fill" viewBox="0 0 240 240">
          <rect x="6" y="6" width="228" height="228" rx="46" fill="#88C3E8" />
          <path d="M58 234 Q58 176 120 176 Q182 176 182 234 Z" fill="#C8E8F7" />
          <rect x="104" y="148" width="32" height="42" rx="14" fill="#F4C9A0" />
          <ellipse cx="120" cy="110" rx="50" ry="54" fill="#F4C9A0" />
          <path d="M70 110 Q68 50 120 50 Q172 50 170 110 Q150 80 120 80 Q90 80 70 110 Z" fill="#1A2635" />
          <path d="M64 112 Q62 44 120 44 Q178 44 176 112" fill="none" stroke="#F2802B" stroke-width="13" stroke-linecap="round" />
          <rect x="50" y="98" width="22" height="46" rx="11" fill="#F2802B" />
          <rect x="168" y="98" width="22" height="46" rx="11" fill="#F2802B" />
          <circle cx="104" cy="113" r="5" fill="#2E1D16" />
          <circle cx="136" cy="113" r="5" fill="#2E1D16" />
          <circle cx="95" cy="129" r="7" fill="#C9603A" opacity=".55" />
          <circle cx="145" cy="129" r="7" fill="#C9603A" opacity=".55" />
          <path d="M104 134 Q120 151 136 134" fill="none" stroke="#2E1D16" stroke-width="5" stroke-linecap="round" />
        </svg>
      </div>

      <div class="auth-sidebar-sticker">OTP sent!</div>

    </aside>

    <section class="auth-form-panel custom-scrollbar">

      <h2>Verify your email</h2>
      <p class="auth-form-subtitle">
        We sent a 6-digit code to <span>{{ emailHint }}</span>.
        Enter it below to confirm your account.
      </p>

      <div class="form-group">
        <label>Enter the 6-digit code</label>
        <div class="otp-row">
          <input
            v-for="(digit, index) in otpDigits"
            :key="index"
            :ref="(el) => (otpInputs[index] = el)"
            v-model="otpDigits[index]"
            type="text"
            class="otp-box"
            maxlength="1"
            inputmode="numeric"
            autocomplete="off"
            @input="handleOtpInput(index)"
            @keydown.backspace="handleOtpBackspace(index)"
          >
        </div>
      </div>

      <button class="btn-auth-submit" @click="handleVerify">
        <CheckCircle2 /> Verify
      </button>

      <p class="otp-resend-row">
        Did not receive a code?
        <span v-if="!resendDisabled" @click="handleResend">{{ resendLabel }}</span>
        <span v-else>{{ resendLabel }}</span>
      </p>

      <p class="otp-back-link">
        <span @click="router.push('/signup')">Back to sign up</span>
      </p>

    </section>

  </div>
</template>
