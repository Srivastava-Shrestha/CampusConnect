<script setup>
import { useRouter } from 'vue-router'
import { GraduationCap, Compass, ArrowRight, Users, ShieldCheck } from 'lucide-vue-next'

const router = useRouter()

const menuLinks = [
  { label: 'Clubs', to: '/clubs' },
  { label: 'Events', to: '/events' },
  { label: 'Leaderboard', to: '/leaderboard' },
  { label: 'For Leaders', to: '/signup' }
]

const roleCards = [
  {
    title: 'Students',
    desc: 'Discover clubs, attend events, track results, and download verified participation certificates.',
    icon: Compass,
    cardClass: 'saturated-orange',
    iconClass: '',
    sparkleFill: 'rgba(255,255,255,0.4)',
    tags: ['Discovery', 'Certificates']
  },
  {
    title: 'Club Leaders',
    desc: 'Create events, manage membership, mark attendance, post announcements, and issue certificates.',
    icon: Users,
    cardClass: 'saturated-green',
    iconClass: 'identity-icon-green',
    sparkleFill: 'rgba(255,255,255,0.3)',
    tags: ['Events', 'Members']
  },
  {
    title: 'Administrators',
    desc: 'Register your college, review club applications, and monitor campus-wide activity at a glance.',
    icon: ShieldCheck,
    cardClass: 'saturated-navy',
    iconClass: 'identity-icon-blue',
    sparkleFill: 'rgba(110,151,201,0.3)',
    tags: ['Governance', 'Leaderboard']
  }
]

function goTo(path) {
  router.push(path)
}
</script>

<template>
  <div class="landing-wrapper custom-scrollbar">

    <header class="landing-nav">
      <div class="logo-row logo-row-flat">
        <div class="logo-mark">
          <GraduationCap />
        </div>
        <span class="brand">Campus Connect</span>
      </div>

      <div class="topbar-spacer"></div>

      <nav class="landing-menu">
        <span
          v-for="link in menuLinks"
          :key="link.to"
          @click="goTo(link.to)"
        >
          {{ link.label }}
        </span>
      </nav>

      <div class="topbar-spacer"></div>

      <div class="landing-nav-btn-group">
        <button class="btn-pill-white" @click="goTo('/login')">Log in</button>
        <button class="btn-pill-dark" @click="goTo('/signup')">Get started</button>
      </div>
    </header>

    <section class="hero-section">

      <div class="hero-copy">
        <div class="hero-badge">
          <span class="hero-badge-dot"></span>
          Discover · Join · Achieve
        </div>

        <h1 class="hero-title">
          Find your<br>
          club. Build<br>
          your <span>story.</span>
        </h1>

        <p class="hero-desc">
          One platform for discovering student clubs, registering for events,
          tracking results, and earning verifiable participation certificates,
          all in one place.
        </p>

        <div class="hero-actions">
          <button class="btn-hero-primary" @click="goTo('/signup')">
            <Compass /> Start exploring
          </button>
          <button class="btn-tour" @click="goTo('/clubs')">
            <span class="btn-tour-icon">
              <ArrowRight />
            </span>
            Browse clubs
          </button>
        </div>

        <div class="social-proof">
          <div class="avatar-stack">
            <div class="stack-avatar">AR</div>
            <div class="stack-avatar">TN</div>
            <div class="stack-avatar">MR</div>
            <div class="stack-avatar stack-avatar-accent">+</div>
          </div>
          <p class="social-proof-text">
            <span>Trusted</span> by students and club leaders across campus
          </p>
        </div>
      </div>

      <div class="hero-graphic">
        <div class="graphic-bg-circle blue"></div>
        <div class="graphic-bg-circle yellow"></div>
        <div class="graphic-bg-circle green"></div>

        <div class="sound-wave-sticker">
          <span class="sound-bar bar-xs"></span>
          <span class="sound-bar bar-lg"></span>
          <span class="sound-bar bar-sm"></span>
          <span class="sound-bar bar-xl"></span>
          <span class="sound-bar bar-xs"></span>
        </div>

        <div class="speech-sticker">Welcome! 👋</div>
        <div class="tag-sticker">Joined Robotics 🤖</div>

        <div class="char-overlay-1">
          <svg class="svg-fill" viewBox="0 0 240 240">
            <rect x="6" y="6" width="228" height="228" rx="46" fill="#F2802B" />
            <path d="M58 234 Q58 176 120 176 Q182 176 182 234 Z" fill="#EFE7DA" />
            <rect x="104" y="148" width="32" height="42" rx="14" fill="#B5764A" />
            <ellipse cx="120" cy="110" rx="50" ry="54" fill="#B5764A" />
            <path d="M70 110 Q68 50 120 50 Q172 50 170 110 Q150 80 120 80 Q90 80 70 110 Z" fill="#241712" />
            <path d="M64 112 Q62 44 120 44 Q178 44 176 112" fill="none" stroke="#F5C13D" stroke-width="13" stroke-linecap="round" />
            <rect x="50" y="98" width="22" height="46" rx="11" fill="#F5C13D" />
            <rect x="168" y="98" width="22" height="46" rx="11" fill="#F5C13D" />
            <circle cx="104" cy="113" r="5" fill="#2E1D16" />
            <circle cx="136" cy="113" r="5" fill="#2E1D16" />
            <circle cx="95" cy="129" r="7" fill="#C9603A" opacity=".55" />
            <circle cx="145" cy="129" r="7" fill="#C9603A" opacity=".55" />
            <path d="M104 134 Q120 151 136 134" fill="none" stroke="#2E1D16" stroke-width="5" stroke-linecap="round" />
          </svg>
        </div>

        <div class="char-overlay-2">
          <svg class="svg-fill" viewBox="0 0 240 240">
            <rect x="6" y="6" width="228" height="228" rx="46" fill="#4F9D57" />
            <path d="M58 234 Q58 176 120 176 Q182 176 182 234 Z" fill="#F2802B" />
            <rect x="104" y="148" width="32" height="42" rx="14" fill="#D49A68" />
            <ellipse cx="120" cy="110" rx="50" ry="54" fill="#D49A68" />
            <path d="M70 110 Q68 50 120 50 Q172 50 170 110 Q150 80 120 80 Q90 80 70 110 Z" fill="#34241A" />
            <path d="M64 112 Q62 44 120 44 Q178 44 176 112" fill="none" stroke="#88C3E8" stroke-width="13" stroke-linecap="round" />
            <rect x="50" y="98" width="22" height="46" rx="11" fill="#88C3E8" />
            <rect x="168" y="98" width="22" height="46" rx="11" fill="#88C3E8" />
            <circle cx="104" cy="113" r="5" fill="#2E1D16" />
            <circle cx="136" cy="113" r="5" fill="#2E1D16" />
            <circle cx="95" cy="129" r="7" fill="#B5604A" opacity=".55" />
            <circle cx="145" cy="129" r="7" fill="#B5604A" opacity=".55" />
            <path d="M104 134 Q120 151 136 134" fill="none" stroke="#2E1D16" stroke-width="5" stroke-linecap="round" />
          </svg>
        </div>
      </div>
    </section>

    <section class="landing-sections">
      <div class="sections-header">
        <h2>Built for every role</h2>
        <span>One unified system · tailored views</span>
      </div>

      <div class="roles-grid">
        <div
          v-for="card in roleCards"
          :key="card.title"
          class="identity-card"
          :class="card.cardClass"
        >
          <svg class="identity-sparkle s1" viewBox="0 0 24 24">
            <path d="M12 0 C13 7 17 11 24 12 C17 13 13 17 12 24 C11 17 7 13 0 12 C7 11 11 7 12 0Z" :fill="card.sparkleFill"/>
          </svg>
          <div>
            <div class="identity-icon" :class="card.iconClass">
              <component :is="card.icon" />
            </div>
            <h3>{{ card.title }}</h3>
            <p>{{ card.desc }}</p>
          </div>
          <div class="identity-tags">
            <span v-for="tag in card.tags" :key="tag" class="identity-tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </section>

    <footer class="cta-banner">
      <div class="cta-circle-orange"></div>
      <div class="cta-circle-blue"></div>
      <div class="cta-content">
        <h2 class="cta-title">Your community is waiting.</h2>
        <p class="cta-desc">Sign up in under a minute — free forever, no credit card needed.</p>
      </div>
      <button class="btn-cta" @click="goTo('/signup')">
        <ArrowRight /> Create account
      </button>
    </footer>

  </div>
</template>
