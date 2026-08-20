# Campus Connect

> Find your club. Build your story.

A student club management platform for higher-education institutions: club discovery and
membership, the full event lifecycle from draft to results and certificates, announcements,
issue tracking, and an AI club-finder assistant.

**Team 003 (Nexmind)** · BSCS3001 Software Engineering Project, May 2026 · IIT Madras BS Degree

| Layer | Stack |
|---|---|
| Backend | FastAPI · SQLAlchemy 2 (async) · PostgreSQL + asyncpg · Alembic · JWT · uv |
| Frontend | Vue 3 (Composition API) · Vue Router 4 · Pinia · Vite · Vitest |
| Services | AWS S3 (certificate PDFs) · SMTP (mail) · Google OAuth · Anthropic Claude (AI assistant) |

---

## Setup

### Backend — requires Python 3.12+, [uv](https://docs.astral.sh/uv/), PostgreSQL

```bash
cd backend
uv sync                          # install dependencies
cp .env.example .env             # fill in DATABASE_URL, JWT_SECRET_KEY, AWS, SMTP
uv run alembic upgrade head      # create the schema
uv run uvicorn main:app --reload # http://localhost:8000
```

API docs at `/docs` (Swagger) and `/redoc`. Run tests with `uv run pytest`.

> ⚠️ The test suite **drops every table on teardown**. Point `TEST_DATABASE_URL` at a
> throwaway database — never at the same one as `DATABASE_URL`, or the demo data goes with it.

### Frontend — requires Node 20+, npm 10+

```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env
npm run dev                      # http://localhost:5173
```

`npm run build` to bundle, `npm test` for the Vitest suite.

---

## Demo credentials

Password for **every** account: `12345678`

| Role | Email | Use it to show |
|---|---|---|
| Campus admin | `shrestha@ds.study.iitm.ac.in` | Club approval queue (1 pending), all clubs by status, college-wide leaderboard |
| Club leader | `aarav.menon@ds.study.iitm.ac.in` | Leads **CodeCrafters** (5 members) — create/publish events, mark attendance, declare results, answer the issue queue, post announcements |
| Member + certificates | `sara.khan@ds.study.iitm.ac.in` | 3 certificates — WINNER, RUNNER_UP and PARTICIPANT — plus notifications and event registrations |

Other students: `diya.sharma@`, `kabir.rao@`, `ananya.iyer@`, `meera.nair@`, `rohan.gupta@`,
`ishita.bose@`, `vikram.reddy@`, `aditya.verma@`, `nikita.joshi@`, `arjun.pillai@`
— all `@ds.study.iitm.ac.in`.

---

## Demo walkthrough

**College:** IIT Madras BS Degree · `ds.study.iitm.ac.in`

**Clubs (7)** — all four statuses represented, so every admin view has content:

| Status | Clubs |
|---|---|
| ACTIVE | CodeCrafters (Technology), IRIS (Arts & Media), AKORD (Music), RAAHAT (Health & Wellness) |
| PENDING | Women in Tech — sits in the admin approval queue |
| REJECTED | Heighers eSports — the one UNOFFICIAL club |
| ARCHIVED | Deva-Bhasha Sanskrit Society |

**Events (9)** — 4 past (checked in, results declared), 3 upcoming (open for registration),
1 DRAFT, 1 CANCELLED. One event has no capacity limit.

**Certificates (15)** — real PDFs from the app's own renderer, with QR verification.
13 on S3, 2 deliberately on the Postgres fallback path so both storage routes are demoable.
Verify publicly at `/verify/<serial>` — e.g. Sara's WINNER certificate `CC-C22-2026-86883`.


---

## Team contributions

| Member | Commits | PRs (merged) | Branches |
|---|---|---|---|
| **Shrestha** — backend, DB, auth, certificates | 226 | 30 (27) | 21 |
| **Atharv** — AI module, design system, UI | 61 | 7 (7) | 8 |
| **Pawan** — test suites | 42 | 12 (11) | 11 |
| **Shrishti** — frontend API integration | 11 | 12 (10) | 10 |
| **Kavisha** | 4 | 0 | 0 |
| **Total** | **344** | **61 (55)** | **52** |


---

## Documentation

| Where | What |
|---|---|
| [`backend/README.md`](backend/README.md) | Backend setup, configuration, testing |
| [`frontend/README.md`](frontend/README.md) | Frontend setup, structure, design system |
| [`backend/openapi.yaml`](backend/openapi.yaml) | Full API spec — endpoints, user-story mapping, role matrix, error catalogue |
| [`RULES.md`](RULES.md) | Team working agreement |
