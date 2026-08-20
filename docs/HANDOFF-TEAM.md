# Handoff — Campus Connect

What changed on the AI module branch, what is still broken, and who needs to do
what to get to a client-ready build.

Machine-readable version for AI tooling: [`HANDOFF-AGENT.md`](HANDOFF-AGENT.md).
Branch map: [`BRANCH-STATUS.md`](BRANCH-STATUS.md).
AI endpoint contract: [`AI_MODULE_INTEGRATION.md`](AI_MODULE_INTEGRATION.md).

---

## 0. Session update — 2026-08-19

Scope grew well past the AI module during this session, after Shrestha's review
of the first PR draft (§B below) and then a full manual click-through of every
role's flows against a real Neon database. This section is what changed since
§1–§6 were written; those sections are the original AI-module write-up and are
still accurate for that part.

### A. Local dev setup, now Postgres-only

SQLite is gone. Shrestha's review made the call explicit: this project runs
against real Postgres everywhere, including local dev — no SQLite fallback, no
dialect-branching code to support one.

- `scripts/dev_seed.py`, `.env.local.example` — **deleted**.
- `app/models/student.py` — `interests` reverted to plain `ARRAY(Text)`, no
  SQLite variant.
- `app/core/database.py` — reverted to the unconditional
  `connect_args={"statement_cache_size": 0}` (asyncpg-only, matches how the
  app is actually deployed — behind Neon's connection pooler).
- `app/core/config.py` — reverted to a plain `env_file = ".env"`; the
  `ENV_PATH` pathlib resolution was removed as unnecessary indirection.
- To run locally now: a real Postgres, either a Neon branch or
  `docker run postgres:16`, with `alembic upgrade head` applied. **Windows
  still cannot import the backend at all** — `app/core/certificate.py`'s
  module-level `import cairosvg` needs the native Cairo library, which is not
  pip-installable there. WSL remains the only way to run or test the backend
  on Windows; see §D of `HANDOFF-AGENT.md` for exact commands.

### B. Structural fix — AI code moved out of `app/services/`

Flagged in review: `recommender.py`, `llm_client.py`, `voice_budget.py` are
pure functions and a stateless API client, not DB-backed service classes like
everything else `app/services/` holds. They now live in `app/agent/` instead,
alongside the rest of the AI module. Every import site was updated; nothing
outside `app/agent/` and `app/api/ai.py` should ever import them.

### C. Additive backend changes since §2

- **`ClubListItem` / `MyClubItem` gained `links`.** The admin approval cards'
  "View Application" button had nothing to point at — the list endpoints never
  returned the club's links, only the single-club detail endpoint did. Fixed
  with `selectinload(Club.links)` on both list queries (one extra batched
  query, not N+1) and a schema field. No migration; the column already
  existed, only the projection was missing.
- **`DELETE /clubs/{club_id}/members/{student_id}`** — new. The "Remove"
  button on the members page was a stub (`toast.info('not supported yet')`)
  with no backend counterpart. Leader-only, refuses to remove the club's own
  leader (`ClubActionNotAllowedError`).

### D. Frontend — root-cause bugs (not just symptoms)

- **Cross-account data leakage.** `clubsStore` and `eventsStore` cache
  themselves with a `loaded` flag that only cleared on a hard reload.
  Switching accounts in the same tab left the next account looking at the
  previous one's data, or a failed unauthenticated fetch's empty result. This
  was the actual cause of "0 clubs" and "event not found" reports that looked
  unrelated to each other. **Fixed**: both stores `$reset()` on every login and
  logout (`stores/auth.js`, `composables/useAuthSession.js`).
- **"Not found" flashing before the real page loads**, and in one case
  (`LeaderClubView`) **a fully blank white screen** — several views used a
  plain `v-if="entity"` where `entity` starts `null` and the fetch can take a
  few seconds against Neon's real network latency. `v-if` / `v-else` alone
  means "not found" (or nothing at all) is the literal first paint, every
  time. Every affected view now has a third state distinguishing "still
  loading" from "confirmed not found": `EventDetailView`, `ClubProfileView`,
  `ClubDirectoryView` (both its lists), `LeaderClubView`, `LeaderEventsView`.
  All of them render through one shared centred `page-loading-state` CSS class
  (style.css §64) so the loading box looks the same everywhere.
- **`.map(normalizeEvent)` footgun** (`LeaderClubView.vue`) — `Array.map`
  calls its callback with `(item, index, array)`, so the numeric `index` was
  landing in `normalizeEvent`'s second parameter (`registeredEventIds`, which
  the function then calls `.has()` on) → `TypeError`, silently swallowed by a
  surrounding try/catch, which is why the page just looked broken with no
  visible error. Fixed to `.map(row => normalizeEvent(row))`.
- **Registration "closing before the event started"** — investigated via a
  direct Postgres query, not assumed. Confirmed **not a bug**: the display
  code and the `registrationOpen` check both call `new Date()` on the exact
  same backend-provided instant, so a display/comparison mismatch is
  structurally impossible. The events in question had simply already started
  by the time they were viewed (test data created minutes earlier). The UI
  already disables the button and explains why.
- **Member counts off by one** (`LeaderClubView`, `ClubProfileView`) —
  `member_count` from the API counts every `APPROVED` membership, and the
  club leader has one of those too, created automatically at club creation.
  Both pages now subtract the leader from the "Members" stat.
- **Club-profile "Register" button was a dead stub** — `showRegisterHint()`
  just told the student to go to the Events page instead. Now calls the real
  register/unregister endpoints directly, with the same open/closed rule as
  `EventDetailView`.
- **Event editing existed on the backend, nowhere in the UI.** `updateEvent()`
  was a working API client function nothing called; `LeaderEventsView` even
  had a dead `goToEditEvent()` stub pointing at a route that didn't exist.
  `CreateEventView` now doubles as the editor via `/leader/events/:id/edit`;
  the Edit button is now available on any event that isn't cancelled
  (previously gated to drafts only, tighter than the backend's actual rule).

### E. Frontend — UX additions

- **Loading spinners on every action button.** A reusable `.btn-spinner`
  class (style.css §62) reusing the existing route-loader animation, wired
  into every button that hits the backend: auth, onboarding, club
  create/update/delete/join/approve/reject, member approve/reject/remove,
  event create/edit/publish/register/attendance/results, issue
  submit/reply/resolve, announcement post/pin/delete. Several of these had a
  `saving` ref declared but never actually bound to the button — clicking
  visibly did nothing, which was a real part of why the app felt
  unresponsive against Neon's latency.
- **Club switcher relocated to top-right on every leader page that needs
  one**, via one shared `components/ui/LeaderClubSwitcher.vue` instead of
  four separate implementations. `LeaderAnnouncementsView` and
  `LeaderEventsView` previously had no switcher at all — a leader with
  multiple clubs could only change context via `LeaderClubView` or
  `MembersView` and hope the choice carried over through the shared store.
- **In-memory API response cache** (`utils/apiCache.js`), applied to
  `LeaderboardView`, `IssuesView`, `LeaderIssuesView`, `ProfileView`. These
  views fetched into a local component ref inside `onMounted()`, which is
  destroyed and rebuilt on every navigation — unlike `clubsStore`/
  `eventsStore`, whose Pinia state survives route changes. A 2-minute TTL,
  cleared by an explicit `invalidateCache(key)` after any mutation that makes
  the cached read stale (raising an issue, replying/resolving, declaring
  results → leaderboard, onboarding → profile), and cleared entirely on
  login/logout so it can't leak between accounts, same as (D)'s fix.

### What's still open after this session

- `app/agent/` and `POST /ai/chat` still have **zero automated tests** — the
  single largest gap, unchanged from §1.
- Password reset has no completion half: `sendResetLink()` →
  `POST /auth/forgot-password` works, but there is no `/reset-password`
  route, no `resetPassword()` client function, no completion view. Deferred
  deliberately — the whole feature is gated on real email delivery, which the
  team has deferred to production setup.
- `VerifyEmailView` / `verifyEmailOtp()` / `resendOtp()` call endpoints that
  do not exist on the backend. Confirmed harmless: nothing in the app
  navigates there (`SignupView` goes straight to `/login`), so it is dead
  code, not a live broken flow.
- Real AWS credentials are still needed for production. See §F below for the
  interim fix that makes certificates work without them.

---

## 0.1 Session update — 2026-08-20

A second pass, done to prepare a local demo recording: a full empty-state UI
sweep, a real trending-clubs feed for the public landing page, a Postgres
fallback for certificate storage (AWS keys in `.env` are still placeholders —
`AKIAIOSFODNN7EXAMPLE`, literally AWS's own docs example), a URL-based club
banner, and a fully seeded demo college (`demoinstitute`) with real clubs,
events, results and certificates in the shared Neon database.

### F. Certificate storage now falls back to Postgres when S3 fails

`Storage.upload()` was raising `StorageError` on every certificate issued,
because the AWS credentials in `.env` are placeholders, not real keys — this
was silent before (a caught background-task exception), so certificates
looked "issued" in the UI but no PDF ever existed.

- **`Certificate.pdf_data`** — new nullable `LargeBinary` column
  (migration `a1b2c3d4e5f6`). Set only when the S3 upload fails; stays `NULL`
  for anything that uploads to S3 successfully.
- **`CertificateService.issue()`** — tries S3 first, catches `StorageError`,
  stores the already-rendered PDF bytes on the certificate row instead. PDF
  *generation* (`render_pdf`, needs Cairo/WSL) is unchanged either way — only
  the upload step has a fallback.
- **`GET /certificates/{serial}/file`** — new, public, same trust model as
  the existing `GET /certificates/verify/{serial}` (the serial is the
  credential, same idea as an S3 presigned URL). Serves the raw PDF from
  `pdf_data`. `_download_url()` points here only when `pdf_data` is set;
  once real AWS keys are added, new certificates go to S3 and use the signed
  URL exactly as before — **no code change needed to switch back.**
- Existing certificates issued before this fix were re-issued via
  `issue_certificate_job()` directly (not the API) so their PDFs now exist.

### G. Club banner can now be set by URL, no S3 required

`UpdateClubRequest` gained `image_url: str | None` — a leader-supplied URL
used when no file is uploaded in the same request. `ClubService.update()`
prefers an uploaded file's resulting URL if given, otherwise uses this field
directly. `LeaderClubView`'s banner already had a working "Image URL" text
input inside the edit panel that quietly did nothing (the field didn't exist
on the backend schema) — now it works, and there's also a pencil icon
directly on the banner (`window.prompt`-based) for a quicker edit.

### H. Landing page — real trending clubs, no more empty carousel

`HomeView`'s "Trending clubs this semester" called `GET /clubs`, which
requires auth — always 401'd for a logged-out visitor, so the carousel was
silently empty (documented in §5's Shrestha punch-list). New public,
cross-college `GET /clubs/public/trending` (repository join across
`clubs`↔`colleges`, ranked by approved member count) backs it instead, and
each card now shows a university indicator. Also fixed a real bug introduced
mid-session: `useScrollReveal`'s `IntersectionObserver` only observes
elements present in the DOM at its own `onMounted` — an element that mounts
later (behind an async-loaded `v-if`) never gets observed and stays at
`opacity: 0` forever. Fixed by keeping the `reveal`-classed wrapper element
present from first render, swapping only its *contents* on load.

### I. Empty-state / loading-state consistency sweep

Every list and loading branch across student, leader, and admin views now
uses the same `.empty-state-wide` (§65) / `.page-loading-state` (§64)
vocabulary — previously about a third of them rendered nothing at all when
empty (recommended clubs, pending requests, members, issues, certificates,
event history, admin approvals, leaderboard, attendance, results).

### J. Login/Signup — Google SSO button removed from the UI, not deleted

The Google sign-in button was already gated behind `googleEnabled`
(`VITE_GOOGLE_CLIENT_ID` unset ⇒ never rendered), but per a product decision
it's been removed from `LoginView.vue`/`SignupView.vue` entirely rather than
left as unreachable UI. **`useGoogleAuth.js` and the backend's
`POST /auth/google` are untouched** — re-wiring Google auth later is exactly
undoing this UI removal, not rebuilding a composable.

### K. Demo data — `demoinstitute` college fully seeded

Seeded through the real HTTP API (not raw SQL) so every business rule ran
exactly as production would: 6 approved clubs (with proposal-document and
social links), 6 published events with attendance and declared results, 19
certificates spread across winners/runners-up/participants, and 5 new member
accounts alongside the 4 pre-existing demo accounts. 4 leftover duplicate
"Demo Robotics Club" rows and their dependents (events, registrations,
memberships, announcements, issues, notifications) from earlier manual
testing were hard-deleted after confirming zero certificates depended on
them. Full login table in `HANDOFF-AGENT.md` §E.

---

## 1. The short version

The AI Club Finder now works end to end against the real backend. Along the way
we found and fixed seven bugs that were breaking things unrelated to the AI —
club creation, onboarding, club cards, issue submission — because the frontend
had drifted from what the backend actually serves.

Everything in this branch is additive. No migration is required. The Postgres
schema is untouched.

**The one thing to know before reviewing:** `app/agent/` and `POST /ai/chat`
have **no automated tests**. Verification was manual against a seeded database.
That is weaker evidence than a test suite and should be treated as such.

---

## 2. Bugs fixed — and what was actually wrong

These were all real, and most had nothing to do with the AI module.

**Club creation returned 422 for everyone.** The backend moved to
`multipart/form-data` for image upload, but the frontend still sent JSON.
FastAPI cannot parse a JSON body into `Form(...)` parameters, so every club
proposal failed. The same applied to event creation.
→ `clubs.js` and `events.js` now send multipart.

**The onboarding screen never appeared after signup.** `completeSignIn` sent
every student straight to their clubs page — nothing ever navigated to
`/:slug/onboard`. The screen existed and was unreachable.
→ Students with an empty profile are now routed to it, and it stops appearing
once saved.

**Onboarding data was thrown away.** It posted to `POST /auth/onboarding`,
which does not exist and returns 404 — behind a mock fallback that reported
success. Nothing was ever stored.
→ Now saves through `PATCH /students/me`, which the backend already had.

**Issue submission silently failed the same way.** `issues.js` used raw `fetch`
with no `Authorization` header and mock fallbacks, and sent `{club, desc}`
where the API expects `{club_id, description}`. The club dropdown listed four
hardcoded fake clubs.
→ Rewritten. The picker now lists clubs you are actually in.

**The Issues page had no link anywhere.** The route and the page existed; no
menu item pointed at it. That is why nobody could find it.
→ Added "Help & Issues" to the student sidebar.

**Club cards rendered blank.** They relied on a colour and icon field that the
mock fixtures used to provide and the real API never returns.
→ Both are now derived from the club itself, so cards look consistent
everywhere.

**The backend would not start on anything but Postgres.** An asyncpg-only
connection argument was passed unconditionally.
→ Now applied only when the driver is asyncpg. The Postgres path is unchanged.

Plus three inside the AI module: every conversation's first question silently
fell back to the deterministic path; club names printed twice
("Photography Circle Photography Circle"); and the memory store was recording
words like "already" and "option" from ordinary questions, then feeding them
back to the model as the student's interests.

---

## 3. New in this branch

**AI Club Finder** — `POST /ai/chat`. Seven read-only tools over the existing
services, a bounded tool-calling loop, and grounding that makes a wrong answer
structurally unreachable rather than merely detected. If the model is
unavailable it answers deterministically; if the database is unavailable it
answers from a clearly-labelled sample campus. It does not return 5xx.

**Club proposal status list** — under the form on Propose Club, and on the club
leader's page. Answers "what happened to my request?", which previously had no
answer anywhere in the product. Uses `GET /clubs/me` — no backend work needed.

**Issue conversation threads** — issue cards now read as an exchange: your
message, then the leader's reply with their name and date, or a clear note that
none has arrived yet.

**Local development without Postgres** — `scripts/dev_seed.py` builds a
throwaway SQLite campus with six clubs, seven events and three announcements.
Useful for review; not a substitute for testing against Postgres.

---

## 4. Running it locally

**Windows cannot run the backend.** `app/core/certificate.py` imports
`cairosvg` at module level, and the native library is not pip-installable on
Windows, so the whole app fails to import. Use WSL until that import is moved
(see Shrestha's list below).

Terminal 1 — backend, in WSL:

```bash
cd /mnt/g/SE-project/FINAL-Campus-Connect/UI/MAY2026-Team-003/backend
UV_PROJECT_ENVIRONMENT=.venv-linux uv sync
.venv-linux/bin/python scripts/dev_seed.py

DATABASE_URL='sqlite+aiosqlite:///./dev.db' TEST_DATABASE_URL='sqlite+aiosqlite:///./t.db' \
JWT_SECRET_KEY=localdevsecret JWT_ALGORITHM=HS256 FRONTEND_URL=http://localhost:5173 \
AWS_REGION=x S3_BUCKET_NAME=x AWS_ACCESS_KEY_ID=x AWS_SECRET_ACCESS_KEY=x \
SMTP_HOST=localhost SMTP_PORT=1025 SMTP_USER=x SMTP_PASSWORD=x MAIL_FROM=noreply@localhost \
.venv-linux/bin/python -m uvicorn main:app --reload --port 8000
```

Terminal 2 — frontend:

```bash
cd frontend && npm run dev
```

Stop the API before re-seeding; Windows keeps the database file locked.

| Role | Email | Password | Notes |
|---|---|---|---|
| Student | `student@nexmind.edu` | `password123` | In Photography Circle only |
| Club leader | `riya@nexmind.edu` | `password123` | Heads Robotics & Automation |
| Campus admin | `admin@nexmind.edu` | `password123` | Approves club requests |

College slug: `nexmind-institute-of-technology`.

For a fresh institute: sign up an admin on a new email domain, call
`/college/onboarding`, then sign up a student on that same domain — signup
resolves the college from the email suffix, so the order matters.

---

## 5. What still needs doing

### Shrestha — Backend

- [ ] **Move `import cairosvg` inside the render function.** One line. It
      currently breaks local development and testing on Windows for the entire
      team, not just this branch.
- [x] ~~Public clubs endpoint — `GET /clubs` requires auth, so the landing page
      carousel is empty for logged-out visitors.~~ Fixed 2026-08-20: new
      `GET /clubs/public/trending`, see §0.1.H.
- [ ] `/auth/verify-email` and `/auth/resend-otp` do not exist, but
      `VerifyEmailView` calls both.
- [ ] No notification fires when a student submits a club request, so admins
      get no signal that something is waiting. The approvals queue itself is
      fine. Confirm whether poll-only is intended.
- [ ] **Redeploy after this merges** — `/ai/chat` only exists on this branch,
      so the hosted frontend will 404 until then. Expected, not a bug.

### Shrishti — Frontend integration

- [ ] **Result declaration is broken.** `ResultsView` calls
      `PATCH /events/{id}/registrations/{rid}/result`, which does not exist,
      once per row. The real endpoint is `PATCH /events/{event_id}/results`
      taking winner and runner-up in a **single** call.
- [ ] **Leaderboard shows fabricated data.** `clubs.js` calls
      `/clubs/leaderboard`; the real path is `GET /leaderboard`. It falls back
      to mock data 100% of the time.
- [ ] **Certificates show fabricated data.** `certificates.js` sends no auth
      header and uses an `/api/v1` prefix that does not exist, so
      `/certificates/me` 401s into mocks. The download endpoint is not wired at
      all.
- [ ] Delete `src/api/members.js` — targets endpoints that do not exist, and
      nothing imports it.

### Pawan — Testing

- [ ] **Write tests for `app/agent/` and `POST /ai/chat`.** Currently zero
      coverage; this is the largest gap in the branch.
- [ ] Update the ~33 stale frontend tests still asserting the abandoned
      "fall back to mock data" contract.
- [ ] Take pytest output for the report from **CI**, not a local run — the
      suite needs Postgres and MailHog.
- [ ] `backend/tests/conftest.py` defines `db_session` **twice**. Python keeps
      the second, so every test silently uses the SAVEPOINT fixture and the
      simple one is dead code. Confirm whether that is intended.

### Atharv — AI

- [ ] The model sometimes answers without calling a tool; its invented names
      get scrubbed to "that option". The grounding gate works, but the reply is
      useless when it happens.
- [ ] No `timeout=` on the Anthropic client — the 20s deadline is only checked
      between iterations, so a hung call blocks for the SDK default of 10
      minutes.
- [ ] A database error swallowed during degradation can still 500 on session
      teardown.
- [ ] Add `var/` to `.dockerignore` — it is gitignored but would bake student
      memory into a built image.
- [ ] Sarvam voice mode — deferred to Milestone 5.

### Kavisha — Milestone 4 report

Verified against the deployed API on 2026-08-11:

- [ ] **Leaderboard is delivered** — `GET /leaderboard` now exists. §5.3 and
      §12.4 say deferred; update them and §7 row 7.1.
- [ ] **F-04 (event reminder) is not delivered.** The notification enum has no
      reminder type; `RESULT_POSTED` is a result notification, not a reminder.
- [ ] **F-05 (announcement seen count) is not delivered.**
      `/announcements/unread-count` returns the *caller's* unread count, not how
      many members read a post.
- [ ] **Result endpoint must be written one way throughout** —
      `PATCH /events/{event_id}/results` is the one that ships.
- [ ] §2 credits Atharv with the AI Club Finder as delivered while §5.2 says
      deferred. It is in review as of this PR.

---

## 6. Suggested next feature

Rejected club proposals currently show a status but no reason —
`PATCH /clubs/{club_id}/reject` accepts no message field (logged as F-03,
deferred to M5). Adding one is small and makes the proposal list genuinely
useful rather than just informative.
