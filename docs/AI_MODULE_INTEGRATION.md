# AI Module — Integration Notes

For backend reviewers and testers looking at the AI Club Finder branch.

This document answers three questions: what actually changed outside the AI
module, how to run and check it yourself, and what is still owed by other parts
of the project before this can be considered finished.

The design rationale lives in [`AI_ARCHITECTURE_DECISIONS.md`](AI_ARCHITECTURE_DECISIONS.md).
This file is only about integration.

---

## 1. What this adds

One endpoint:

```
POST /ai/chat        Security(get_user_info, scopes=["STUDENT"])
```

Request:

```json
{
  "messages": [ { "role": "user", "content": "..." } ],
  "interest_text": "what the student typed"
}
```

Response:

```json
{
  "reply": "grounded prose answer",
  "kind": "chat | clubs | events | popularity | event_fallback",
  "items": [],
  "degraded": false,
  "tools_used": ["get_my_clubs", "recommend_clubs"],
  "iterations": 2,
  "budget_exhausted": false
}
```

`messages` is the transcript so far, owned by the client and trimmed to the last
10 turns server-side. There is no server-side session state.

`degraded: true` means Claude could not be reached and a deterministic
recommender answered instead. The endpoint does not return 5xx on a model
outage — that is the point of the fallback — so treat `degraded` as the health
signal rather than the status code.

### How it reaches data

The module does **not** query the database and does **not** call the deployed
API over HTTP. It calls `ClubService`, `EventService` and `AnnouncementService`
through the same `Depends(get_*_service)` wiring every other router uses:

```python
services = Services(club=club_service, event=event_service,
                    announcement=announcement_service)
```

Seven read-only tools sit on top of those three services. None of them mutates
anything, and none takes a `college_id` argument — scoping comes from the
verified JWT payload that the services already expect as their first argument.
That means the AI module inherits your authorisation rules automatically. If
you change what a student may see in `ClubService.list()`, the assistant's view
changes with it, with no edit here.

---

## 2. Files a reviewer should look at

| Path | What it is |
|---|---|
| `app/api/ai.py` | The router. ~50 lines, same shape as the other routers. |
| `app/agent/tools.py` | The seven tools and their JSON schemas. |
| `app/agent/loop.py` | The bounded tool-calling loop. |
| `app/agent/grounding.py` | The allow-list and output gates. |
| `app/agent/budget.py` | Per-turn caps and cost accounting. |
| `app/agent/memory.py` | Deterministic memory. No model write path. |
| `app/schemas/ai.py` | Request and response models. |

---

## 3. Changes outside the AI module

These are the only edits that touch shared code. They are small and worth
reviewing carefully, because they affect everyone.

**`app/core/config.py`** — the five existing required settings are unchanged and
still required. AI and voice settings were appended, all with defaults, so an
existing `.env` keeps working untouched. An empty `ANTHROPIC_API_KEY` puts the
module in deterministic mode rather than breaking startup.

**`app/models/student.py`** — `interests` is now
`ARRAY(Text).with_variant(JSON, "sqlite")` with `default=list`.

On Postgres this is still a plain `text[]` and the generated DDL is identical,
so **no migration is needed**. The variant exists purely so the app can run
against a throwaway SQLite file for manual testing (section 4). `default=list`
makes the ORM always send a value instead of relying on the server default,
which is also the safer behaviour on Postgres.

**`main.py`** — registers `ai_router`.

**`pyproject.toml`** — adds `anthropic`, `httpx`, `websockets` to dependencies
and `aiosqlite` to the dev group.

**`backend/uv.lock`** — regenerated. The merge from `dev` had left literal
conflict markers inside it, which made `uv sync` fail to parse the file.

---

## 4. Running it locally, without Postgres

There is a seed script that builds a disposable SQLite database so a reviewer
can click through the feature without provisioning anything.

```bash
cd backend
cp .env.local.example .env.local
uv sync
uv run python scripts/dev_seed.py
uv run --env-file .env.local uvicorn main:app --reload --port 8000
```

Then the frontend, in a second terminal:

```bash
cd frontend
printf 'VITE_API_URL=http://localhost:8000\n' > .env.local
npm install
npm run dev
```

Sign in as `student@nexmind.edu` / `password123` and open
`/nexmind-institute-of-technology/find-clubs`.

The seed creates one college, seven students, six clubs across different
categories, seven events and three announcements. The demo student belongs to
exactly one club on purpose — it makes "what am I already in?" checkable by eye
and leaves the recommender something new to suggest.

Two caveats, stated plainly:

- The schema is built with `Base.metadata.create_all`, not alembic. The
  migrations are Postgres-specific and will not run on SQLite. This database is
  therefore only as correct as the models. It is fine for exercising the UI and
  the AI loop; it is **not** a substitute for testing against Postgres, and it
  should not be used to validate migrations or anything schema-sensitive.
- Stop the API before re-running the seed. Windows keeps the file locked while
  uvicorn holds it open.

Without an `ANTHROPIC_API_KEY` in `.env`, everything still runs — the assistant
just answers deterministically and sets `degraded: true`.

### Checking it by hand

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@nexmind.edu","password":"password123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

curl -s -X POST http://localhost:8000/ai/chat \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"messages":[],"interest_text":"I like building robots, what should I join?"}'
```

A healthy response has `degraded: false` and a non-empty `tools_used`.

---

## 5. Test status — read this before approving

The AI module's own test coverage is **incomplete**, and that is the main known
gap in this branch.

| Area | State |
|---|---|
| `services/recommender.py` (deterministic core, grounding helpers) | Covered — 34 offline tests pass |
| `services/llm_client.py` | Covered |
| `app/agent/tools.py`, `loop.py`, `grounding.py`, `memory.py` | **No tests** |
| `POST /ai/chat` | **No tests** |

The planned `test_agent_tools.py`, `test_agent_loop.py`, `test_grounding_v2.py`
and `test_memory.py` do not exist yet. What has been done instead is manual
verification against the seeded database: the loop was confirmed to call real
tools, stay inside the caller's college, and degrade cleanly with no API key.

That is weaker evidence than a test suite, and it should be treated as such.
Writing those tests is the first follow-up task on this branch.

The rest of the suite is unaffected: 426 tests collect, and the 34 that run
without a database pass.

---

## 6. What the AI module needs from other work

These map to the backend gap issues already open (#50–#56). None of them block
merging this branch — the module works without them — but each one is a
capability the assistant cannot offer until the underlying endpoint exists.

**Student onboarding / interests persistence.** `students.interests` exists as a
column but nothing populates it, because `POST /auth/onboarding` was never
implemented and the frontend's onboarding payload is discarded. Until then the
assistant only knows the interests a student types into the finder box during
the current session. Once interests are persisted, the durable memory tier in
`app/agent/memory.py` can be seeded from the profile and recommendations get
meaningfully better on the first question rather than the third.

Note also the field mismatches recorded in `PROPOSAL-onboarding-endpoint.md`:
the frontend sends `dept` (column is `branch`), `year` as a string like `"pg"`
(column is `int`), and `goal` (no column). Those need resolving as part of that
endpoint, not here.

**CORS allowing localhost.** `main.py` uses `allow_origins=[settings.FRONTEND_URL]`,
a single origin, so a locally-run frontend cannot talk to the deployed API at
all. This is why section 4 runs the backend locally rather than pointing the
local UI at the deployed one. Changing that setting to a list would make
reviewing any frontend work substantially easier. It is deliberately **not**
changed in this branch, since it affects deployment.

**Public clubs endpoint.** `GET /clubs` requires auth. Not needed by the
assistant, which is always called by a signed-in student, but it is the reason
the public landing carousel is empty.

**Event descriptions in list responses.** `EventListItem` has no `description`
field, only `EventDetailResponse` does. The recommender therefore scores events
on title and venue alone, and `_recommend_clubs` passes `description=""` for
events. Adding the field to the list schema, or accepting an N+1 detail fetch,
would improve event matching. The current behaviour is documented in
`tools.py` rather than worked around silently.

---

## 7. Known behaviour worth knowing about

- **A cold first request can degrade.** The per-turn deadline is 20 seconds
  (`AGENT_DEADLINE_SECONDS`). On a freshly started server the first request pays
  for client setup and connection warm-up, and has been observed to trip that
  budget once, answering from the deterministic path instead. Subsequent
  requests complete in roughly 6 seconds. It fails safe rather than erroring,
  but if it proves common the deadline should be raised.
- **Voice is not in this branch.** `services/voice_budget.py` and the Sarvam
  settings are present, but there is no voice router and no frontend voice
  session. The UI uses the existing browser narrator. Realtime voice is the next
  piece of work.
- **Prompt caching does not fire.** Haiku 4.5 needs a 4096-token cacheable
  prefix; ours is around 1300. Measured, not assumed — see the decisions
  document.
