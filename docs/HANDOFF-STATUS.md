# Campus Connect — Delivery Status and Team Actions

Where the app stands, what is broken, and what each person needs to do to get
to a client-ready build. Written on branch `feature/atharv-ai-module`, before
its PR into `dev`.

Companion documents:
- [`BRANCH-STATUS.md`](BRANCH-STATUS.md) — which branch is current for what
- [`AI_MODULE_INTEGRATION.md`](AI_MODULE_INTEGRATION.md) — AI endpoint contract and how to run it
- [`AI_ARCHITECTURE_DECISIONS.md`](AI_ARCHITECTURE_DECISIONS.md) — why the AI module is built the way it is

---

## 1. What this branch changes

### Backend — new

| File | What it does |
|---|---|
| `app/api/ai.py` | `POST /ai/chat`, behind `Security(get_user_info, scopes=["STUDENT"])` |
| `app/agent/tools.py` | Seven read-only tools over the existing services |
| `app/agent/loop.py` | Bounded tool-calling loop (iteration, tool-call, token and deadline caps) |
| `app/agent/grounding.py` | Allow-list and output gates |
| `app/agent/memory.py` | Deterministic memory — no model write path |
| `app/agent/budget.py` | Per-turn budget and cost accounting |
| `app/agent/demo_data.py` | Sample campus used when the database is unreachable or unseeded |
| `app/schemas/ai.py` | `AgentChatRequest` / `AgentChatResponse` |
| `app/agent/recommender.py` | Deterministic scoring core, grounding helpers |
| `app/agent/llm_client.py` | Claude client with a deterministic mock fallback |
| `scripts/dev_seed.py` | Throwaway SQLite database — run the whole app without Postgres |

### Backend — changes to shared code

All additive. Each one was needed and none narrows an existing response.

| File | Change | Why it is safe |
|---|---|---|
| `app/models/student.py` | `interests` → `ARRAY(Text).with_variant(JSON, "sqlite")`, `default=list` | Postgres DDL identical (`interests TEXT[] DEFAULT '{}' NOT NULL`, verified). **No migration.** Exists so the app can run on SQLite for review |
| `app/schemas/event.py`, `app/services/event.py` | `EventListItem` gains `description` | The column already existed on `Event`; this only projects it. Fixes event matching, which previously scored on title and venue alone |
| `app/core/database.py` | `statement_cache_size=0` applied only when the URL is asyncpg | It is an asyncpg-only argument and was a `TypeError` on every other driver. **Postgres path unchanged** |
| `app/core/config.py` | AI / Sarvam / agent settings appended, all with defaults | An existing `.env` keeps working. Empty `ANTHROPIC_API_KEY` means deterministic mode, not a crash |
| `main.py`, `app/api/__init__.py`, `app/schemas/__init__.py` | Register `ai_router` and AI schemas | Alongside dev's routers, not instead of |
| `pyproject.toml` | `anthropic` added; `aiosqlite` in the dev group | `httpx` and `websockets` dropped — nothing imports them any more |

### Frontend — changes

| File | Change |
|---|---|
| `src/api/students.js` | **New.** Wraps `GET /students/me` and `PATCH /students/me` |
| `src/api/clubs.js` | `createClub` / `updateClub` converted to `multipart/form-data` — **fixes the 422 on club creation** |
| `src/api/events.js` | `createEvent` / `updateEvent` converted the same way |
| `src/views/OnboardView.vue` | Saves through `PATCH /students/me` instead of the dead `POST /auth/onboarding` |
| `src/composables/useAuthSession.js` | Routes students with an empty profile to `/:slug/onboard` — **fixes onboarding never appearing** |
| `src/components/ui/ClubCard.vue` | Derives banner colour and icon — **fixes blank club cards** |
| `src/views/FindClubsView.vue` | Question renders immediately in a pending state; failed turns keep the question |
| `src/api/ai.js`, `src/api/ai.test.js` | Real `/ai/chat` client, tests rewritten for it (7 passing) |
| `src/assets/style.css` | Sections 55 and 56 |

---

## 2. Bugs found — and their status

### Fixed on this branch

| # | Problem | Root cause |
|---|---|---|
| 1 | **Club creation returned 422** | Backend moved to `multipart/form-data` for the image upload; frontend still sent JSON |
| 2 | **Onboarding screen never appeared after signup** | `completeSignIn` sent every student to `homeRoute`; nothing ever navigated to `/:slug/onboard` |
| 3 | **Onboarding data was silently discarded** | Posted to `POST /auth/onboarding`, which returns 404, behind a mock fallback that reported success |
| 4 | **Club cards rendered blank** | Cards relied on a colour/icon field the real API never returned |
| 5 | **Every first AI question fell back to the deterministic path** | The finder sends an empty transcript, so the opening turn posted zero messages and the API rejected it |
| 6 | **"Photography Circle Photography Circle"** | The model writes the club name *and* the reference tag; expanding the tag printed the name twice |
| 7 | **Backend would not start on any non-asyncpg driver** | `statement_cache_size` passed unconditionally |

### Open — needs a decision or another owner

| # | Problem | Owner | Notes |
|---|---|---|---|
| 8 | **The model sometimes answers without calling a tool**, and its invented names get scrubbed to *"that option"* | Atharv | The grounding gate works — nothing false reaches the user — but the reply is useless when it happens. Needs prompt work to force a tool call |
| 9 | **`PATCH /events/{id}/registrations/{rid}/result` does not exist** | Shrishti / Pawan | `ResultsView.vue:68` calls it once per row. Real endpoint is `PATCH /events/{event_id}/results`, taking winner and runner-up in **one** call. Result declaration is broken in the UI today |
| 10 | **Leaderboard shows fabricated data** | Shrishti | `clubs.js:239` calls `/clubs/leaderboard`; the real path is `GET /leaderboard`. It always falls back to `mockLeaderboard` |
| 11 | **Certificate wallet shows fabricated data** | Shrishti | `certificates.js` uses raw `fetch` with **no `Authorization` header** and a `/api/v1` prefix that does not exist. `/certificates/me` 401s and falls back to mocks. `GET /certificates/{serial}/download` is not wired at all |
| 12 | **`/auth/verify-email` and `/auth/resend-otp` do not exist** | Shrestha | `VerifyEmailView` calls both |
| 13 | **Public landing page cannot list clubs** | Shrestha | `GET /clubs` requires auth; the trending strip is silently empty for logged-out visitors. Needs a public variant |
| 14 | **`cairosvg` breaks local dev on Windows** | Shrestha | `app/core/certificate.py` imports it at module level, reached via `app/services/__init__.py`. The whole backend fails to import. **One-line fix: move the import inside the render function.** Until then, use WSL |
| 15 | **No notification when a club request is submitted** | Shrestha | `NotificationType` has no "pending approval" case, so admins get no bell signal. The approvals queue itself is fine |
| 16 | **`src/api/members.js` targets endpoints that do not exist** | Shrishti | Dead file — imported by nothing. Delete it |
| 17 | **~33 frontend tests fail** | Pawan | Pre-existing. They assert the old "fall back to mock data" contract the API layer abandoned. Not caused by this branch |

---

## 3. AI module — what it needs, and what it does not

**It ships as-is.** Nothing below blocks it; each item improves answer quality.

| Now working | Still limited by |
|---|---|
| Chat with real tool calls over clubs, events, announcements | — |
| Grounded recommendations, allow-list enforced | — |
| Deterministic fallback when the model is unreachable | — |
| Interests persist through onboarding | — |
| Tags on club cards (derived, see below) | No curated tags column |
| Event matching on real descriptions | — |

**On tags:** the schema has no `tags` column. Rather than add a migration against
the shared database, `recommender.derive_tags()` reads tags out of each club's
own name, category and description using the vocabulary the recommender already
scores against. Every tag is a word the club used about itself. If a curated
`clubs.tags` column is added later, swap the call — nothing else changes.

**One deployment note:** `/ai/chat` only exists on this branch. Until it merges
**and the backend redeploys**, the hosted frontend will 404 on it. That is
expected, not a bug.

---

## 4. To finish the app — by owner

### Shrestha (Backend)
- [ ] **Move `import cairosvg` inside the render function** — one line, unblocks local dev and testing on Windows for the whole team (#14)
- [ ] Public clubs endpoint so the landing page works logged-out (#13)
- [ ] `/auth/verify-email` and `/auth/resend-otp`, or remove the screens (#12)
- [ ] Decide on a notification type for "club request submitted" (#15)
- [ ] Redeploy after this PR merges, so `/ai/chat` goes live

### Shrishti (Frontend integration)
- [ ] Fix result declaration to use `PATCH /events/{event_id}/results` with winner + runner-up in one call (#9)
- [ ] Point the leaderboard at `GET /leaderboard` and delete `mockLeaderboard` (#10)
- [ ] Fix certificates: add the auth header, drop the `/api/v1` prefix, wire the download endpoint, remove the mock fallback (#11)
- [ ] Delete `src/api/members.js` (#16)

### Pawan (Testing)
- [ ] Update the ~33 stale frontend tests to the real API contract (#17)
- [ ] Write tests for `app/agent/` and `POST /ai/chat` — **currently zero coverage**
- [ ] Pytest output for the report from **CI**, not a local run
- [ ] Note: `backend/tests/conftest.py` defines `db_session` **twice**; Python keeps the second, so every test uses the SAVEPOINT fixture and the simple one is dead code. Confirm whether that is intended

### Atharv (AI / PM)
- [ ] Fix the model occasionally answering without a tool call (#8)
- [ ] Merge this PR, then verify `/ai/chat` against the deployed backend
- [ ] Sarvam voice mode — deferred to M5

### Kavisha (Docs)
- [ ] Milestone 4 report corrections — see the verdicts in the review notes: leaderboard is delivered now, F-04 and F-05 claims are not supported by the endpoints cited, and the result endpoint must be written one way throughout

---

## 5. Proposed: club application status list

Small, self-contained, and it closes a real gap — a student proposes a club and
then has no way to see what happened to it.

**Where:** below the form card on the Propose Club tab, and on the club leader's
My Club page.

**Shape:** a simple stacked card list, one row per application — club name,
category, submitted date, and a status pill (`Pending` / `Approved` /
`Rejected`), reusing the existing `StatusPill` component.

**Data:** no backend work needed. `GET /clubs/me` already returns the caller's
clubs with `membership_status` and the club `status`, which is exactly what the
pill needs. A student whose club is still `PENDING` is already the club head, so
the row exists.

**Effort:** frontend only, roughly one component plus a section in each of the
two views. Good candidate for Shrishti, or for whoever picks up the UI polish
pass.

**Worth noting for the client demo:** rejected clubs currently carry no reason
(`PATCH /clubs/{club_id}/reject` accepts no message field — logged as F-03,
deferred to M5), so a `Rejected` pill can show the status but not the why.
