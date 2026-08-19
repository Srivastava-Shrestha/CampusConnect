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

Windows cannot import the backend: `app/core/certificate.py` imports `cairosvg`
at module level, reached via `app/services/__init__.py`, and the native Cairo
library is not pip-installable there. **Use WSL.**

```bash
# backend venv (Linux), separate from the Windows .venv
wsl -e bash -lc "cd /mnt/g/SE-project/FINAL-Campus-Connect/UI/MAY2026-Team-003/backend \
  && UV_PROJECT_ENVIRONMENT=.venv-linux uv sync"

# required env vars for any import of app/ or main
DATABASE_URL='sqlite+aiosqlite:///./dev.db' TEST_DATABASE_URL='sqlite+aiosqlite:///./t.db'
JWT_SECRET_KEY=s JWT_ALGORITHM=HS256 FRONTEND_URL=http://localhost:5173
AWS_REGION=x S3_BUCKET_NAME=x AWS_ACCESS_KEY_ID=x AWS_SECRET_ACCESS_KEY=x
SMTP_HOST=x SMTP_PORT=25 SMTP_USER=x SMTP_PASSWORD=x MAIL_FROM=x
# GOOGLE_CLIENT_ID and ANTHROPIC_API_KEY have defaults; empty key => deterministic mode
```

```bash
# seed a throwaway SQLite campus (stop the API first: Windows locks the file)
.venv-linux/bin/python scripts/dev_seed.py
# accounts, all password123:
#   student@nexmind.edu  (member of Photography Circle only)
#   riya@nexmind.edu     (heads Robotics & Automation)
#   admin@nexmind.edu    (campus admin)
# slug: nexmind-institute-of-technology
```

Verification commands that are known to work:

```bash
.venv-linux/bin/python -c "from main import app; print(len(app.openapi()['paths']))"   # 47
.venv-linux/bin/python -m pytest tests/test_recommender.py tests/test_llm_client.py tests/unit -q  # 60 passed
cd frontend && npm run build          # passes
cd frontend && npx vitest run src/api/ai.test.js   # 7 passed
```

`tests/integration/` fails wholesale (needs real Postgres + MailHog). Not caused
by this branch — do not treat as a regression.

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
  app/services/recommender.py: deterministic scoring, derive_tags, resolve_entities
  app/services/llm_client.py:  Claude client + mock fallback
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
`app/api/ai.py`, `app/agent/*` (7 files), `app/schemas/ai.py`,
`app/services/{recommender,llm_client,voice_budget}.py`, `scripts/dev_seed.py`,
`.env.local.example`.

### Backend, modified shared code

| File | Before | After | Why |
|---|---|---|---|
| `app/models/student.py` | `interests: ARRAY(Text)` | `ARRAY(Text).with_variant(JSON,"sqlite")`, `default=list` | SQLite has no array type. **Postgres DDL byte-identical, no migration** (verified against migration `138b941be66b`) |
| `app/schemas/event.py` | `EventListItem` had no `description` | added `description: str` | Recommender scored events on title+venue only |
| `app/services/event.py` | list projection omitted description | `description=event.description` | Column already existed; only projection was missing |
| `app/core/database.py` | `connect_args={"statement_cache_size":0}` unconditional | applied only when `"asyncpg" in DATABASE_URL` | asyncpg-only arg; `TypeError` on every other driver. Postgres path unchanged |
| `app/core/config.py` | core settings only | + AI/Sarvam/agent settings, all defaulted; `ENV_PATH` resolved absolutely | Plain `load_dotenv()` silently no-ops when uvicorn starts outside `backend/` |
| `main.py`, `app/api/__init__.py`, `app/schemas/__init__.py` | — | register `ai_router`, AI schemas | Alongside dev's routers |
| `pyproject.toml` | — | `+anthropic`, `+aiosqlite` (dev); `-httpx`, `-websockets` | Neither was imported after the rebuild |
| `app/services/recommender.py` | — | `+derive_tags()`, `+mapped_category()`, `+_collapse_repeated_names()` | See below |

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
