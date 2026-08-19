<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Printer, Download, GraduationCap } from 'lucide-vue-next'
import { verifyCertificate, getCertificateDownload } from '../api/certificates'
import { useAuthStore } from '../stores/auth'
import { toast } from '../composables/useToast'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

// The download endpoint requires a token and only returns a link for the
// certificate's own owner - anyone else gets a 404. This page is public
// (a certificate can be shared with anyone), so downloading only makes
// sense to offer when a student is signed in; everyone else still has Print.
const downloading = ref(false)

// The certificate is looked up by its serial through the same public verify
// endpoint the /verify page uses, rather than trusting whatever a query
// string claims - a link with hand-edited query params used to be able to
// display a fabricated certificate.
const certificate = ref(null)
const notFound = ref(false)

const actionTextMap = {
  WINNER: 'has been awarded the title of Winner in',
  RUNNER_UP: 'has been awarded Runner-up in',
  PARTICIPANT: 'has successfully participated in'
}

const certTitleMap = {
  WINNER: 'Certificate of Excellence',
  RUNNER_UP: 'Certificate of Merit',
  PARTICIPANT: 'Certificate of Participation'
}

const resultLabelMap = {
  WINNER: '\u{1F947} Winner',
  RUNNER_UP: '\u{1F948} Runner-up',
  PARTICIPANT: '\u{2B50} Participant'
}

const resultClassMap = {
  WINNER: 'winner',
  RUNNER_UP: 'runner-up',
  PARTICIPANT: 'participant'
}

function formatDate(value) {
  if (!value) return ''

  return new Date(value).toLocaleDateString(undefined, {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const certName = computed(() => certificate.value?.student_name || '')
const certEvent = computed(() => certificate.value?.event_title || '')
const certClub = computed(() => certificate.value?.club_name || '')
const certDate = computed(() => formatDate(certificate.value?.event_date))
const certSerial = computed(() => certificate.value?.serial || route.params.serial)
const certCollege = computed(() => certificate.value?.college_name || '')

const certResult = computed(() => certificate.value?.result || 'PARTICIPANT')
const typeHeading = computed(() => certTitleMap[certResult.value])
const actionText = computed(() => actionTextMap[certResult.value])
const resultLabel = computed(() => resultLabelMap[certResult.value])
const resultClass = computed(() => resultClassMap[certResult.value])

function goBack() {
  router.back()
}

function printCert() {
  window.print()
}

async function downloadCert() {
  if (downloading.value) return

  downloading.value = true

  try {
    const result = await getCertificateDownload(certSerial.value)
    window.open(result.download_url, '_blank', 'noopener')
  } catch (error) {
    toast.error(error.message || 'Could not download this certificate. It may not belong to your account.')
  } finally {
    downloading.value = false
  }
}

onMounted(async function loadCertificate() {
  const serial = String(route.params.serial || '').trim()

  if (!serial) {
    notFound.value = true
    return
  }

  try {
    const result = await verifyCertificate(serial)

    if (result.valid) {
      certificate.value = result.certificate
      document.title = 'Certificate – ' + certificate.value.student_name + ' – Campus Connect'
    } else {
      notFound.value = true
    }
  } catch (error) {
    toast.error(error.message || 'Could not load this certificate.')
    notFound.value = true
  }
})
</script>

<template>
  <div class="cert-toolbar">
    <button class="btn-secondary" @click="goBack">
      <ArrowLeft /> Back
    </button>
    <div class="cert-toolbar-spacer"></div>
    <button
      v-if="auth.isLoggedIn"
      class="btn-secondary"
      :disabled="downloading"
      @click="downloadCert"
    >
      <Download /> {{ downloading ? 'Preparing...' : 'Download PDF' }}
    </button>
    <button class="btn-secondary" @click="printCert">
      <Printer /> Print
    </button>
  </div>

  <div v-if="notFound" class="cert-page cert-page-empty">
    <p class="empty-state">No certificate found for this serial number.</p>
  </div>

  <div v-else-if="certificate" class="cert-page">

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

        <div class="cert-result-pill" :class="resultClass">
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
            <!-- The verify endpoint identifies the club, not the leader who
                 signed off - showing a specific name here would be a guess. -->
            <p class="cert-sig-name">{{ certClub }}</p>
            <p class="cert-sig-role">On behalf of the club</p>
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
