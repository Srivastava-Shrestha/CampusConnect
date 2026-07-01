<template>
  <div class="auth-body">
    <div class="auth-frame">


      <aside class="auth-sidebar orange-auth">


        <div class="auth-sidebar-logo">
          <div class="auth-sidebar-logo-mark">
            🎓
          </div>

          <span class="brand">
            Campus Connect
          </span>
        </div>


        <div class="auth-content">
          <h2 class="auth-sidebar-title">
            Welcome<br>
            back.
          </h2>

          <p class="auth-sidebar-desc">
            Pick up where you left off.
            Your clubs, events and certificates
            are all waiting.
          </p>

          <p class="auth-quote">
            Connect. Collaborate. Grow.
          </p>
        </div>


        <div class="auth-sidebar-circle-1"></div>

        <div class="auth-sidebar-char">
          <svg class="svg-fill" viewBox="0 0 240 240">
            <rect x="6" y="6" width="228" height="228" rx="46" fill="#6E3A2E"/>
            <path d="M58 234 Q58 176 120 176 Q182 176 182 234 Z" fill="#C23E3E"/>
            <rect x="104" y="148" width="32" height="42" rx="14" fill="#E7B58E"/>
            <ellipse cx="120" cy="110" rx="50" ry="54" fill="#E7B58E"/>
            <path d="M70 110 Q68 50 120 50 Q172 50 170 110 Q150 80 120 80 Q90 80 70 110 Z" fill="#241712"/>
            <path
              d="M64 112 Q62 44 120 44 Q178 44 176 112"
              fill="none"
              stroke="#F2802B"
              stroke-width="13"
              stroke-linecap="round"
            />
            <rect x="50" y="98" width="22" height="46" rx="11" fill="#F2802B"/>
            <rect x="168" y="98" width="22" height="46" rx="11" fill="#F2802B"/>
            <circle cx="104" cy="113" r="5" fill="#2E1D16"/>
            <circle cx="136" cy="113" r="5" fill="#2E1D16"/>
            <path
              d="M104 134 Q120 151 136 134"
              fill="none"
              stroke="#2E1D16"
              stroke-width="5"
              stroke-linecap="round"
            />
          </svg>
        </div>

      </aside>


      <section class="auth-form-panel">

        <h2>Sign in</h2>

        <p class="auth-form-subtitle">
          New here?

          <span @click="goSignup">
            Create an account
          </span>
        </p>


        <div class="form-group">
          <label>College Email Address</label>

          <div class="input-icon-wrapper">
            <input
              type="email"
              placeholder="shikha@knit.ac.in"
              v-model="email"
            />
          </div>
        </div>


        <div class="form-group">
          <label>Password</label>

          <div class="input-icon-wrapper login-password-row">

            <input
              :type="showPassword ? 'text' : 'password'"
              placeholder="Enter your password"
              v-model="password"
            />

            <button
              type="button"
              class="icon-clickable"
              @click="togglePassword"
            >
              👁
            </button>

          </div>
        </div>

        <div class="auth-checkbox-row">

          <div class="auth-checkbox">
            <input
              type="checkbox"
              v-model="remember"
            />

            <span>
              Remember me
            </span>
          </div>

          <a href="#" class="auth-forgot-link">
            Forgot password?
          </a>

        </div>

        <button
          class="btn-auth-submit"
          @click="handleLogin"
        >
          Sign in
        </button>

      </section>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const email = ref("")
const password = ref("")
const remember = ref(true)
const showPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const goSignup = () => {
  router.push("/signup")
}

const handleLogin = () => {
  if (!email.value || !password.value) {
    alert("Please enter email and password.")
    return
  }

  alert("Login successful")
}
</script>