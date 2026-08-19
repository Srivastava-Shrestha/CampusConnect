# Handoff — Campus Connect

What changed on the AI module branch, what is still broken, and who needs to do
what to get to a client-ready build.

Machine-readable version for AI tooling: [`HANDOFF-AGENT.md`](HANDOFF-AGENT.md).
Branch map: [`BRANCH-STATUS.md`](BRANCH-STATUS.md).
AI endpoint contract: [`AI_MODULE_INTEGRATION.md`](AI_MODULE_INTEGRATION.md).

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
- [ ] Public clubs endpoint — `GET /clubs` requires auth, so the landing page
      carousel is empty for logged-out visitors.
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
