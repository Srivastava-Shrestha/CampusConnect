<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Printer, GraduationCap } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const actionTextMap = {
  'winner': 'has been awarded the title of Winner in',
  'runner-up': 'has been awarded Runner-up in',
  'participant': 'has successfully participated in'
}

const certTitleMap = {
  'winner': 'Certificate of Excellence',
  'runner-up': 'Certificate of Merit',
  'participant': 'Certificate of Participation'
}

const resultLabelMap = {
  'winner': '\u{1F947} Winner',
  'runner-up': '\u{1F948} Runner-up',
  'participant': '\u{2B50} Participant'
}

function getParam(name, fallback) {
  const value = route.query[name]
  return value || fallback
}

const certName = computed(() => getParam('name', 'Shikha Singh'))
const certEvent = computed(() => getParam('event', 'Photography Walk: Old City'))
const certClub = computed(() => getParam('club', 'Photography Circle'))
const certDate = computed(() => getParam('date', '8 July 2026'))
const certSerial = computed(() => getParam('serial', 'CC-CERT-2026-1841'))
const certCollege = computed(() => getParam('college', 'KNIT Sultanpur'))
const certLeader = computed(() => getParam('leader', 'Aayansh Yadav'))

const certResult = computed(function readResult() {
  const raw = String(getParam('result', 'participant')).toLowerCase()

  if (actionTextMap[raw]) {
    return raw
  }

  return 'participant'
})

const typeHeading = computed(() => certTitleMap[certResult.value])
const actionText = computed(() => actionTextMap[certResult.value])
const resultLabel = computed(() => resultLabelMap[certResult.value])

function goBack() {
  router.back()
}

function printCert() {
  window.print()
}

onMounted(function setPageTitle() {
  document.title = 'Certificate – ' + certName.value + ' – Campus Connect'
})
</script>

<template>
  <div class="cert-toolbar">
    <button class="btn-secondary" @click="goBack">
      <ArrowLeft /> Back
    </button>
    <div class="cert-toolbar-spacer"></div>
    <button class="btn-secondary" @click="printCert">
      <Printer /> Print / Save PDF
    </button>
  </div>

  <div class="cert-page">

    <div class="cert-top-strip"></div>
    <div class="cert-bot-strip"></div>

    <div class="cert-border-outer"></div>
    <div class="cert-border-inner"></div>

    <svg v-for="corner in ['tl', 'tr', 'bl', 'br']" :key="corner" class="corner-ornament" :class="corner" width="74" height="74" viewBox="0 0 74 74">
      <path d="M6 54 L6 6 L54 6" fill="none" stroke="#C79A2B" stroke-width="2.2"/>
      <path d="M13 46 L13 13 L46 13" fill="none" stroke="#C79A2B" stroke-width="0.8" opacity="0.4"/>
      <circle cx="6" cy="6" r="3.5" fill="#C79A2B"/>
      <circle cx="30" cy="6" r="1.6" fill="#C79A2B" opacity="0.5"/>
      <circle cx="6" cy="30" r="1.6" fill="#C79A2B" opacity="0.5"/>
      <rect x="17" y="3" width="5" height="5" fill="none" stroke="#C79A2B" stroke-width="1" transform="rotate(45 19.5 5.5)" opacity="0.6"/>
      <rect x="3" y="17" width="5" height="5" fill="none" stroke="#C79A2B" stroke-width="1" transform="rotate(45 5.5 19.5)" opacity="0.6"/>
      <circle cx="48" cy="6" r="1" fill="#C79A2B" opacity="0.35"/>
      <circle cx="6" cy="48" r="1" fill="#C79A2B" opacity="0.35"/>
    </svg>

    <div class="cert-content">

      <div class="cert-top-group">

        <div class="cert-header-row">
          <div class="cert-logo-circle">
            <GraduationCap />
          </div>
          <div class="cert-org-block">
            <p class="cert-org-name">Campus Connect</p>
            <p class="cert-org-college">{{ certCollege }}</p>
          </div>
        </div>

        <div class="cert-divider">
          <div class="cert-divider-line"></div>
          <div class="cert-divider-diamond"></div>

          <svg width="44" height="24" viewBox="0 0 44 24">
            <path d="M22 12 C17 7 10 5 6 7 C3 9 3 14 7 16 C11 18 17 16 20 13" fill="none" stroke="#C79A2B" stroke-width="1.3" opacity="0.75"/>
            <path d="M22 12 C19 8 14 6 10 8 C7 9 7 13 10 15 C13 17 17 15 19 13" fill="none" stroke="#C79A2B" stroke-width="0.8" opacity="0.35"/>
            <circle cx="5" cy="11" r="1.5" fill="#C79A2B" opacity="0.5"/>
            <circle cx="9" cy="5" r="1.5" fill="#C79A2B" opacity="0.5"/>
            <circle cx="15" cy="4" r="1.5" fill="#C79A2B" opacity="0.5"/>
            <circle cx="20" cy="7" r="1.5" fill="#C79A2B" opacity="0.5"/>
          </svg>

          <p class="cert-type-heading">{{ typeHeading }}</p>

          <svg width="44" height="24" viewBox="0 0 44 24" style="transform:scaleX(-1)">
            <path d="M22 12 C17 7 10 5 6 7 C3 9 3 14 7 16 C11 18 17 16 20 13" fill="none" stroke="#C79A2B" stroke-width="1.3" opacity="0.75"/>
            <path d="M22 12 C19 8 14 6 10 8 C7 9 7 13 10 15 C13 17 17 15 19 13" fill="none" stroke="#C79A2B" stroke-width="0.8" opacity="0.35"/>
            <circle cx="5" cy="11" r="1.5" fill="#C79A2B" opacity="0.5"/>
            <circle cx="9" cy="5" r="1.5" fill="#C79A2B" opacity="0.5"/>
            <circle cx="15" cy="4" r="1.5" fill="#C79A2B" opacity="0.5"/>
            <circle cx="20" cy="7" r="1.5" fill="#C79A2B" opacity="0.5"/>
          </svg>

          <div class="cert-divider-diamond"></div>
          <div class="cert-divider-line"></div>
        </div>

      </div>

      <div class="cert-body-group">

        <p class="cert-intro-text">This is to certify that</p>

        <p class="cert-recipient-name">{{ certName }}</p>
        <div class="cert-name-bar"></div>

        <p class="cert-action-text">{{ actionText }}</p>

        <p class="cert-event-title">{{ certEvent }}</p>
        <p class="cert-event-sub">{{ certClub }} · {{ certDate }}</p>

        <div class="cert-result-pill" :class="certResult">
          {{ resultLabel }}
        </div>

        <div class="cert-ornament-row">
          <div class="cert-ornament-thin-line"></div>
          <span class="cert-ornament-dot">&#10022;</span>
          <span class="cert-ornament-dot-sm">&#10022;</span>
          <span class="cert-ornament-dot">&#10022;</span>
          <div class="cert-ornament-thin-line"></div>
        </div>

        <p class="cert-authority-text">Issued under the authority of {{ certCollege }}</p>
        <p class="cert-authority-sub">Accredited by Campus Connect · India</p>

      </div>

      <div class="cert-bottom-group">

        <div class="cert-sig-divider"></div>

        <div class="cert-footer-row">

          <div class="cert-sig-block">
            <div class="cert-sig-line"></div>
            <p class="cert-sig-name">{{ certLeader }}</p>
            <p class="cert-sig-role">Club Leader</p>
          </div>

          <div class="cert-seal">
            <svg width="96" height="96" viewBox="0 0 96 96">
              <defs>
                <path id="top-arc" d="M 11,48 A 37,37 0 0,1 85,48"/>
                <path id="bot-arc" d="M 13,50 A 35,35 0 0,0 83,50"/>
              </defs>
              <circle cx="48" cy="48" r="44" fill="#FFFBF2" stroke="#C79A2B" stroke-width="1.5"/>
              <circle cx="48" cy="48" r="38" fill="none" stroke="#C79A2B" stroke-width="0.6" opacity="0.5"/>
              <circle cx="48" cy="48" r="30" fill="rgba(199,154,43,0.07)" stroke="none"/>
              <text font-family="Outfit, sans-serif" font-size="7.5" font-weight="700" fill="#C79A2B" letter-spacing="2.5">
                <textPath href="#top-arc" startOffset="50%" text-anchor="middle">CAMPUS CONNECT</textPath>
              </text>
              <text font-family="Outfit, sans-serif" font-size="7" font-weight="700" fill="#C79A2B" letter-spacing="2">
                <textPath href="#bot-arc" startOffset="50%" text-anchor="middle">CERTIFIED</textPath>
              </text>
              <text x="48" y="44" text-anchor="middle" font-family="Outfit, sans-serif" font-weight="800" font-size="17" fill="#C79A2B">CC</text>
              <text x="48" y="57" text-anchor="middle" font-family="Outfit, sans-serif" font-weight="600" font-size="7" fill="#9A8978" letter-spacing="0.5">INDIA</text>
              <text x="22" y="51" text-anchor="middle" font-size="8" fill="#C79A2B" opacity="0.7">&#9733;</text>
              <text x="74" y="51" text-anchor="middle" font-size="8" fill="#C79A2B" opacity="0.7">&#9733;</text>
            </svg>
            <p class="cert-serial-mono">{{ certSerial }}</p>
          </div>

          <div class="cert-sig-block">
            <div class="cert-sig-line"></div>
            <p class="cert-sig-name">Student Affairs</p>
            <p class="cert-sig-role">College Administrator</p>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>
