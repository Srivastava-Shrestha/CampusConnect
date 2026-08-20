# Handoff — machine-readable context

Written for an AI agent or LLM picking up this branch cold. Terse and factual.
Human-facing version: [`HANDOFF-TEAM.md`](HANDOFF-TEAM.md).

```yaml
project: Campus Connect (IITM BS Software Engineering, Team-003 NexMind)
repo: https://github.com/Srivastava-Shrestha/MAY2026-Team-003
branch: feature/atharv-ai-module   # cut from origin/dev, clean history
target: dev
stack: Vue 3 + Vite + Pinia frontend; FastAPI + async SQLAlchemy + Postgres backend
package_manager: uv (backend), npm (frontend)
```

## Hard rules

```yaml
never_run_git: true          # emit commands as text for the human to run
never_claude_coauthor: true  # no Claude/Anthropic trailer in commits or PRs; academic integrity
work_dir: UI/MAY2026-Team-003/ only
css: single file frontend/src/assets/style.css, new numbered section at end + STYLE-INDEX.md row
vue: Composition API <script setup>, no <style scoped>, multi-line literals, named helper functions
```

## Environment

**No SQLite, anywhere.** `scripts/dev_seed.py` and `.env.local.example` were
deleted after backend review — this project runs Postgres only, including
local dev (Neon branch or `docker run postgres:16`, then `alembic upgrade
head`). Do not reintroduce a SQLite path.

Windows cannot import the backend: `app/core/certificate.py` imports `cairosvg`
at module level, reached via `app/services/__init__.py`, and the native Cairo
library is not pip-installable there. **Use WSL.**

```bash
# backend venv (Linux), separate from the Windows .venv
wsl -e bash -lc "cd /mnt/g/SE-project/FINAL-Campus-Connect/UI/MAY2026-Team-003/backend \
  && UV_PROJECT_ENVIRONMENT=.venv-linux uv sync"

# required env vars for any import of app/ or main (all real Postgres now)
DATABASE_URL='postgresql+asyncpg://user:pass@host/db?ssl=require'
TEST_DATABASE_URL='postgresql+asyncpg://user:pass@host/db2?ssl=require'  # a SEPARATE db - conftest.py drops all tables on it
JWT_SECRET_KEY=<random> JWT_ALGORITHM=HS256 FRONTEND_URL=http://localhost:5173
AWS_REGION=... S3_BUCKET_NAME=... AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=...
SMTP_HOST=... SMTP_PORT=... SMTP_USER=... SMTP_PASSWORD=... MAIL_FROM=...
# GOOGLE_CLIENT_ID and ANTHROPIC_API_KEY have defaults; empty key => deterministic mode
# Neon URLs need ?ssl=require for asyncpg - NOT ?sslmode=require&channel_binding=require
# (those are libpq-only query params; asyncpg raises TypeError on them)
```

Verification commands that are known to work:

```bash
.venv-linux/bin/python -c "from main import app; print(len(app.openapi()['paths']))"   # 48
cd frontend && npm run build          # passes
cd frontend && npx vitest run src/api/ai.test.js src/api/leaderboard.test.js   # 10 passed
```

**Do not run `pytest` against a `.env` where `TEST_DATABASE_URL` points at the
same database as `DATABASE_URL`.** `tests/conftest.py`'s `setup_db` fixture
runs `Base.metadata.drop_all` on `TEST_DATABASE_URL` at session end — pointing
both URLs at the same database means running the suite wipes real data.

## AI module architecture

```yaml
endpoint: POST /ai/chat
auth: Security(get_user_info, scopes=["STUDENT"])
request: {messages: [{role, content}], interest_text: str}
response: {reply, kind, items[], degraded, offline, tools_used[], iterations, budget_exhausted}
never_5xx: true   # degrades instead; `degraded` is the health signal, not the status code
```

```yaml
files:
  app/api/ai.py:        router; injects club/event/announcement/student services
  app/agent/tools.py:   7 read-only tools + JSON schemas; Services dataclass
  app/agent/loop.py:    bounded loop (iterations<=4, tool_calls<=6, tokens<=12000, deadline 20s)
  app/agent/grounding.py: allow-list + output gates
  app/agent/memory.py:  deterministic facts; NO model write path
  app/agent/budget.py:  per-turn accounting
  app/agent/demo_data.py: sample campus + resolve_services() tiering
  app/agent/recommender.py: deterministic scoring, derive_tags, resolve_entities
  app/agent/llm_client.py:  Claude client + mock fallback
  app/agent/voice_budget.py: Sarvam spend meter, unused until voice mode is built
# ^ all of app/agent/* - moved here from app/services/ after review flagged
#   pure functions / a stateless client sitting in the DB-service-class dir.
#   If you see an import from app.services.recommender or
#   app.services.llm_client anywhere, that is stale - fix the import, do not
#   move the files back.
```

```yaml
two_degradation_axes:
  offline: true   # DB unreachable or college has zero clubs -> demo_data campus
  degraded: true  # model unreachable -> deterministic recommender
  independent: true  # either can occur without the other
```

**Security invariants — do not violate:**
- No tool schema accepts `college_id` or `user_id`. Scoping comes from the JWT
  `payload` passed to each service. Every schema sets `additionalProperties: false`.
- Only `.list()`, `.get()`, `.my_clubs()`, `.feed()`, `.my_profile()` are reachable.
- The model may only name entities a tool returned this turn (`AllowList`);
  unknown ids resolve to `"that option"`.
- `Services.student` holds the full `StudentService`, which *does* expose
  `update_my_profile`. Nothing calls it, but the "read-only by construction"
  claim is weaker than it reads. Do not add a tool that reaches it.

## Changes on this branch

### Backend, new files
`app/api/ai.py`, `app/agent/*` (7 files, includes `recommender.py`/`llm_client.py`/
`voice_budget.py` — see note above, these do **not** live in `app/services/`),
`app/schemas/ai.py`.
`scripts/dev_seed.py` and `.env.local.example` were added, then **deleted** in
session 2 (Postgres-only, see below) — do not recreate them.

### Backend, modified shared code

| File | Before | After | Why |
|---|---|---|---|
| `app/models/student.py` | `ARRAY(Text)` | unchanged (SQLite variant reverted) | Shrestha's review: Postgres-only, no dialect branching |
| `app/schemas/event.py` | `EventListItem` had no `description` | added `description: str` | Recommender scored events on title+venue only |
| `app/services/event.py` | list projection omitted description | `description=event.description` | Column already existed; only projection was missing |
| `app/core/database.py` | — | unconditional `connect_args={"statement_cache_size":0}` (asyncpg-only, matches prod) | Reverted the dialect guard per review — this file stays untouched otherwise |
| `app/core/config.py` | core settings only | + AI/Sarvam/agent settings, all defaulted; plain `env_file=".env"` (no `ENV_PATH` resolution) | Reverted the pathlib resolution per review |
| `main.py`, `app/api/__init__.py`, `app/schemas/__init__.py` | — | register `ai_router`, AI schemas | Alongside dev's routers |
| `pyproject.toml` | — | `+anthropic` (dev group); `aiosqlite` added then removed | SQLite path banned |
| `app/agent/recommender.py` | — | `+derive_tags()`, `+mapped_category()`, `+_collapse_repeated_names()` | See below |

### Session 2 (2026-08-19) — real Neon DB, backend feature additions, app-wide manual QA

Full context in `HANDOFF-TEAM.md` §0. Summary for an agent picking this up:

**Backend, additive (new endpoint + fields, nothing removed):**

| File | Change | Why |
|---|---|---|
| `app/schemas/club.py` | `ClubListItem` gained `links: list[ClubLinkSchema]` | Frontend needs a club's external links on list pages |
| `app/repository/club.py`, `app/repository/membership.py` | list queries gained `.options(selectinload(Club.links))` | Avoid N+1 when serializing `links` |
| `app/services/club.py`, `app/services/membership.py` | list methods populate `links=[...]` | See above |
| `app/repository/membership.py` | + `async def delete(self, membership)` | Backing method for remove-member |
| `app/services/membership.py` | + `remove_member(payload, club_id, student_id)` | Leader-only; blocks removing the leader's own row |
| `app/schemas/membership.py` | + `RemoveMemberResponse` | Response model for the new route |
| `app/core/messages.py` | + `MembershipMessages.MEMBER_REMOVED` | — |
| `app/api/club.py` | + `DELETE /clubs/{club_id}/members/{student_id}` | Closed a dead "Remove" stub in `MembersView.vue` |
| `app/agent/demo_data.py` | fixed duplicate `description=` kwarg (`EventDetailResponse`) | Broke every offline-tier `get_event` call after `EventListItem` gained `description` |
| `app/agent/memory.py` | `record_memberships` reads `membership_status`/`id` (was `status`/`club_id`) | Tool projects the former field names; memory silently recorded nothing |
| `app/agent/memory.py` | `record_interest` filters tokens through `mapped_category()` | Was storing words like "already"/"part" as fake interests |
| `app/agent/recommender.py` | + `_collapse_repeated_names()` | Fixed "Photography Circle Photography Circle" duplication |

**Frontend, root-caused bug fixes:**

| Symptom | Root cause | Fix |
|---|---|---|
| Data from account A visible after switching to account B in the same tab | `clubsStore`/`eventsStore` have a `loaded` flag that only clears on hard reload | `auth.js` `logout()` and `useAuthSession.js` `completeSignIn()` now call `useClubsStore().$reset()`, `useEventsStore().$reset()`, `invalidateCache()` |
| Views briefly show "not found" / "no items" before the real fetch resolves | Guard conditions were `v-if="item"` / `v-else` with no third branch for "still loading" | Added `hasLoaded` ref + `page-loading-state`-wrapped loading branch to `LeaderClubView`, `ClubProfileView`, `EventDetailView`, `ClubDirectoryView`, `EventsView`, and others |
| `registeredEventIds.has is not a function` crash | `.map(normalizeEvent)` passes `(item, index)` — `normalizeEvent` treats the numeric index as a second arg | `.map(row => normalizeEvent(row))` in `LeaderClubView.vue` |
| `Failed to resolve component: CustomSelect` | Import removed when swapping in `LeaderClubSwitcher`, but a second unrelated `<CustomSelect>` (category picker) still used it | Re-added the import alongside the new one |
| Member count on `LeaderClubView`/`ClubProfileView` one too high | `member_count` includes the leader's own auto-created membership row | `Math.max(member_count - 1, 0)` for the displayed "Members" stat |
| Club-page "Register" button sent students to the Events page instead of registering | `ClubProfileView.vue` had a stub `showRegisterHint()` | Real `toggleEventRegistration()` using `registerForEvent`/`unregisterFromEvent`, matching `EventDetailView`'s registration-window logic |
| No event editing | Dead route stub | New route `/:slug/leader/events/:id/edit`; `CreateEventView.vue` now doubles as editor (`isEditing` branch, `updateEvent()`) |
| Every route switch re-fetched everything from the API | No caching layer existed | `utils/apiCache.js` — `cachedFetch(key, fetchFn, ttlMs)` / `invalidateCache(key)`, applied to leaderboard/issues/profile/certificates, invalidated after the relevant mutation |
| No loading feedback on button-triggered actions | Buttons had no spinner/disabled wiring in most mutation handlers | `.btn-spinner` (CSS §62) + per-item busy `Set` pattern applied app-wide |
| Empty lists (recommended clubs, pending requests, members, issues, certificates, event history, approvals, leaderboard, attendance, results) rendered nothing when empty | No empty-state markup existed for these branches | `.empty-state-wide` (CSS §65) applied consistently across every list view, member/leader/admin |

**Backend confirmed correct, not a bug (investigated via direct Postgres query against live data):** event registration closing — `_as_utc()` in `app/schemas/event.py` only adds tzinfo to naive datetimes, comparison is timezone-safe; the reported "early close" was real elapsed time on test events. Leaderboard is computed live per-request (`app/services/leaderboard.py`), no staleness possible.

**Local dev, decided:** Postgres-only (Neon), no Docker for local dev (Docker reserved for the eventual PR pipeline), no SQLite anywhere — see Environment section above.

### Frontend

| File | Before | After | Why |
|---|---|---|---|
| `src/api/students.js` | did not exist | wraps `GET/PATCH /students/me` | Onboarding had no real endpoint to call |
| `src/api/clubs.js` | `createClub`/`updateClub` sent JSON | multipart `data` + optional `image`; signature gained 2nd `image` arg | Backend moved to `Form(...)`/`File(...)`; JSON caused **422** |
| `src/api/events.js` | same | same | same |
| `src/api/issues.js` | raw `fetch`, no auth header, mock fallbacks, wrong payload keys | authenticated `apiRequest`, correct `RaiseIssueRequest` shape, API→UI mappers | Submissions silently faked success against 401 |
| `src/api/ai.js` | `findMatchingClubs` (client-side mock) | `askAssistant` → `POST /ai/chat` | Real endpoint |
| `src/api/ai.test.js` | tested deleted function | 7 tests against the real contract | Branch had broken its own tests |
| `src/views/OnboardView.vue` | `POST /auth/onboarding` (404) | `PATCH /students/me`, correct field mapping | Endpoint never existed |
| `src/composables/useAuthSession.js` | always `homeRoute` | routes empty-profile students to `/:slug/onboard` | Onboarding was unreachable |
| `src/views/IssuesView.vue` | hardcoded 4 fake clubs, `{club,desc}` | real `getMyClubs()`, `{club_id,description}`, loading/error states | Form was disconnected from the API |
| `src/components/ui/IssueCard.vue` | flat reply block | thread: "You asked" → "*X* replied · date" / awaiting note | Reply attribution was invisible |
| `src/components/ui/ClubCard.vue` | no colour/icon → blank banners | derives via `utils/clubVisuals.js`; uses `image_url` when set | API returns neither field |
| `src/components/ui/ClubProposalList.vue` | did not exist | reuses `approval-card` classes | Students could not see proposal status |
| `src/utils/clubVisuals.js` | did not exist | shared `bannerColourFor` / `iconNameFor` | Was duplicated in ClubCard |
| `src/views/CreateClubView.vue` | sent `image_url:null`; redirected away on submit | field removed; stays and shows the proposal stack | `image_url` is not on `CreateClubRequest`; redirect hid the outcome |
| `src/views/LeaderClubView.vue` | — | + proposal stack | Same list for leaders |
| `src/components/layout/StudentSidebar.vue` | no Issues link | + "Help & Issues" | Route existed but nothing linked to it |
| `src/assets/style.css` | ends at §54 | + §55–59 | See `STYLE-INDEX.md` |

### Bugs fixed on this branch

| # | Symptom | Root cause | Fix |
|---|---|---|---|
| 1 | Every first AI question fell back to deterministic | Finder sends empty transcript; opening turn posted zero messages, API rejects | `loop.py` seeds `interest_text` as the first user message |
| 2 | `"Photography Circle Photography Circle"` | Model writes name *and* `[[club:N]]`; expansion duplicates | `_collapse_repeated_names()` after resolution; only allow-list names, only adjacent repeats |
| 3 | `get_event` errored on the entire offline tier | `EventListItem.description` made `demo_data.py` pass `description=` twice to `EventDetailResponse` | dropped the explicit kwarg |
| 4 | "Clubs you joined" memory never populated | `record_memberships` read `status`/`club_id`; tool projects `membership_status`/`id` | read the projected keys |
| 5 | Memory stored `already`, `part`, `any`, `option` and fed them to the prompt as interests | `record_interest` kept the 3 longest tokens of any question | keep only tokens where `mapped_category(tok)` is truthy |
| 6 | Club creation 422 | JSON vs multipart | see table above |
| 7 | Backend would not start on non-asyncpg | unconditional `connect_args` | dialect guard |

## Session 3 (2026-08-20) — demo prep

Full narrative in `HANDOFF-TEAM.md` §0.1. Summary for an agent picking this up:

```yaml
certificate_storage_fallback:
  problem: Storage.upload() raises StorageError - AWS keys in .env are literal
    AWS-docs placeholders (AKIAIOSFODNN7EXAMPLE), not real credentials
  fix:
    - migration a1b2c3d4e5f6: certificates.pdf_data (LargeBinary, nullable)
    - app/services/certificate.py: issue() catches StorageError, stores pdf
      bytes on the row instead of failing
    - GET /certificates/{serial}/file: new, public (serial IS the credential,
      same trust model as GET /certificates/verify/{serial}), serves pdf_data
    - _download_url() picks this route over the S3 signed URL only when
      pdf_data is set - once real AWS keys land, new certs go to S3 and use
      the old path automatically, zero code change
  do_not: reintroduce a local-disk write path; pdf_data in Postgres is the
    only fallback, matches "no SQLite / no extra local-only abstractions"
    precedent from session 2

club_banner_by_url:
  schema: UpdateClubRequest.image_url: str | None (new field)
  service: ClubService.update() - uploaded file wins if given, else data.image_url
  frontend: LeaderClubView.vue - pencil icon on the banner (window.prompt),
    plus the pre-existing "Image URL" edit-panel field now actually works
    (it silently no-op'd before this - the field existed in the Vue form but
    UpdateClubRequest had no matching schema field)

trending_clubs_public_endpoint:
  route: GET /clubs/public/trending (no auth)
  new: app/schemas/club.py TrendingClubItem, app/repository/club.py
    list_trending() (join Club -> College, order by approved member count),
    app/services/club.py ClubService.trending()
  why: HomeView's old "Trending clubs" called GET /clubs, which requires
    auth - always 401'd for a logged-out visitor. Fixes the Shrestha
    punch-list item "Public clubs endpoint" from session 1.
  frontend_bug_fixed: useScrollReveal's IntersectionObserver only observes
    elements present in the DOM at ITS OWN onMounted - an element behind an
    async v-if that resolves later never gets observed, stays opacity:0
    forever. Fix: keep the reveal-classed wrapper mounted from first paint,
    swap only its inner content.

login_signup_google_button:
  removed_from: LoginView.vue, SignupView.vue (template + script wiring)
  NOT_deleted: composables/useGoogleAuth.js, POST /auth/google backend route
  reason: product decision, button wasn't reachable anyway (VITE_GOOGLE_CLIENT_ID
    unset), but a future "re-add Google auth" task is a UI re-wire, not a
    rebuild - check useGoogleAuth.js exists before assuming it needs writing

empty_state_sweep:
  applied: .empty-state-wide (css §65) / .page-loading-state (css §64) to
    every remaining bare .empty-state across ClubDirectoryView, EventsView,
    AttendanceView, ResultsView, AdminOverviewView, LeaderboardView
  pattern: same vocabulary already used elsewhere this session - if a new
    view needs an empty state, use these two classes, not a bespoke one
```

### E. Demo data — `demoinstitute` college

Seeded via the real HTTP API against Neon (not raw SQL), so every business
rule (approval gates, membership checks, cert issuance) ran for real. Login
table:

```yaml
college_slug: demoinstitute
password_all_accounts: password123
accounts:
  - {email: admin@demoinstitute.edu, role: CAMPUS_ADMIN}
  - {email: leader@demoinstitute.edu, role: STUDENT, heads: [Robotics & Automation Club, Photography Circle]}
  - {email: member@demoinstitute.edu, role: STUDENT, note: 4 clubs, won Bot Building Sprint}
  - {email: member2@demoinstitute.edu, role: STUDENT, heads: [Coding Ninjas]}
  - {email: member3@demoinstitute.edu, role: STUDENT, name: Aditi Sharma, heads: [Music Society]}
  - {email: member4@demoinstitute.edu, role: STUDENT, name: Karan Verma, heads: [Literary Circle]}
  - {email: member5@demoinstitute.edu, role: STUDENT, name: Neha Gupta, heads: [Sports Club]}
  - {email: member6@demoinstitute.edu, role: STUDENT, name: Rohan Mehta, note: won Inter-Dept Football Cup}
  - {email: member7@demoinstitute.edu, role: STUDENT, name: Priya Nair, note: won Open Mic Night}
data: 6 ACTIVE clubs (each with 2 links), 6 PUBLISHED events with attendance
  + declared results, 19 certificates (winner/runner-up/participant mix)
cleanup_done: 4 duplicate "Demo Robotics Club" rows and all dependents
  (events, registrations, memberships, announcements, issues, notifications)
  hard-deleted after confirming zero certificates referenced them
```

## Open items

```yaml
ai_module:
  - id: model_skips_tool_call
    severity: medium
    detail: model sometimes answers with no tool call; invented names scrub to "that option"
    fix_direction: strengthen system prompt / consider tool_choice
  - id: no_client_timeout
    severity: medium
    file: app/agent/loop.py
    detail: AsyncAnthropic has no timeout=; deadline only checked between iterations, SDK default is 10min
  - id: poisoned_session_500
    severity: medium
    detail: resolve_services swallows a DB error but get_db still commits on teardown -> PendingRollbackError
  - id: unguarded_memory_write
    severity: low
    detail: memory._save_all has no error handling; read-only FS would 500
  - id: no_tests
    severity: high
    detail: app/agent/* and POST /ai/chat have zero automated coverage
  - id: dockerignore
    severity: low
    detail: var/ is gitignored but not dockerignored; student_memory.json bakes into images
```

```yaml
elsewhere_pre_existing:
  - ResultsView calls PATCH /events/{id}/registrations/{rid}/result (does not exist);
    real endpoint is PATCH /events/{event_id}/results taking winner+runner_up in one call
  - clubs.js getLeaderboard calls /clubs/leaderboard; real path is /leaderboard -> always mock data
  - certificates.js: no auth header, /api/v1 prefix that does not exist, download not wired -> always mock
  - auth.js calls /auth/verify-email and /auth/resend-otp; neither exists
  - HomeView calls GET /clubs unauthenticated -> 401, public carousel silently empty
  - src/api/members.js targets non-existent endpoints; imported by nothing, safe to delete
  - ~33 frontend tests assert the abandoned "fall back to mock" contract
  - backend/tests/conftest.py defines db_session twice; Python keeps the second
  - app/core/certificate.py module-level cairosvg import breaks Windows dev
```

```yaml
backend_gaps_affecting_ai:
  - clubs table has no tags column (worked around by recommender.derive_tags)
  - students.year is int(1..5); onboarding "PG"/"Diploma" cannot be stored
  - onboarding "goal" has no column; collected in UI, not persisted
  - PATCH /clubs/{id}/reject accepts no reason field (F-03, deferred to M5)
```
