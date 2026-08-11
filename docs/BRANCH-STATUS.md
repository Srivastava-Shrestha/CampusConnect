# Branch status — Atharv

Which branch is current for each piece of work, and what the backend team needs
from it. Updated 2026-08-11.

---

## Active branches

| Branch | Area | State |
|---|---|---|
| `feature/atharv-fix-shell-nav-logout` | UI bug fixes (issue #46) | **Merged** into `dev` (PR #49) |
| `feature/atharv-design-system` | Admin + club-leader visual redesign | Pushed, ready for PR |
| `feature/atharv-ai-module` | AI Club Finder | **Use this one.** Ready for PR |

### ⚠ Do not use these

`feature/atharv-ai-club-finder` and `feature/atharv-ai-module-v2` are the older
AI branches. They are superseded by `feature/atharv-ai-module` and are being
deleted. Anything reviewed on them is out of date.

---

## 1. `feature/atharv-fix-shell-nav-logout` — PR #49

Frontend fixes for the eight UI bugs in issue #46. Backend-blocked items from
that issue were split out into separate tickets rather than bundled here.

- Missing logout on the admin sidebar; duplicate logout removed from the profile
  page so the sidebar is the single source
- Admin overview loaded via one `Promise.all`, so a single failing request blanked
  the whole page — now independent loads with an empty state
- Sidebar and mobile nav highlighted the wrong item because active state used
  prefix matching; now longest-match
- Club leaders with no club got a blank page and a silent redirect; now an empty
  state with a "Start a new club" action
- Signup card scrollbar and login sidebar alignment

## 2. `feature/atharv-design-system`

Response to the feedback that admin and club-leader pages looked too colourful.
Neutral workspace palette for those roles; public and student pages keep the
existing warm palette.

- `.theme-workspace` applied from the route's role, so the scope is explicit
- Neutralises the colour sources directly, not just the design tokens —
  components carried hardcoded hex values that token overrides did not reach
- Club leader empty-state layout

## 3. `feature/atharv-ai-module`

Rebuilds the AI Club Finder against the real backend. It previously called the
deployed API over HTTP against a stub; it now calls `ClubService`, `EventService`
and `AnnouncementService` through the same dependency injection every other
router uses.

Adds one endpoint: `POST /ai/chat`, guarded by
`Security(get_user_info, scopes=["STUDENT"])`.

Full detail — request/response contract, shared-code changes, how to run it
locally without Postgres, and the known test gap — is in
[`AI_MODULE_INTEGRATION.md`](AI_MODULE_INTEGRATION.md). Design rationale is in
[`AI_ARCHITECTURE_DECISIONS.md`](AI_ARCHITECTURE_DECISIONS.md).

**Known gap, stated up front:** `app/agent/` and `POST /ai/chat` have no
automated tests. Verification so far is manual against a seeded local database.
Writing those tests is the first follow-up.

---

## Merge order and one known collision

Merge in the order listed at the top. Each later branch assumes the earlier ones
are in `dev`.

**`feature/atharv-design-system` and `feature/atharv-ai-module` both add a
`style.css` section numbered 55**, and both add a row 55 to `STYLE-INDEX.md`.
Whichever merges second will conflict. Keep both sections, renumber the second
to 56, and fix its index row. The contents do not overlap — one is the workspace
theme, the other is club card artwork plus the finder pending state.

---

## For the backend team

### What the AI module does and does not need to ship

It ships as-is. Nothing below blocks it — each item degrades answer quality
rather than breaking the feature.

| Works today | Degraded until the item below lands |
|---|---|
| Chat with real tool calls over clubs, events, announcements | Cold start every session, because interests are never persisted |
| Grounded recommendations, allow-list enforced | Weak event matching, because list responses carry no description |
| Deterministic fallback when the model is unreachable | `tags` always empty on cards and in responses |

### Blocking nothing, but needed for the AI module to be good

- **`students.interests` is never written.** The column exists, but
  `POST /auth/onboarding` does not, so onboarding data is discarded. Until this
  lands the assistant only knows interests typed into the finder during the
  current session. **Highest-value item for recommendation quality.**
- **Onboarding field mismatches**, detailed in `PROPOSAL-onboarding-endpoint.md`:
  the frontend sends `dept` (column is `branch`), `year` as `"pg"`/`"diploma"`
  (column is an `int`), and `goal` (no column exists). Resolve as part of that
  endpoint.

### Response shapes

- **`EventListItem` has no `description`** — only `EventDetailResponse` does. The
  recommender therefore scores events on title and venue alone and passes an
  empty description internally. Adding the field to the list schema is a
  one-field change with a direct quality win.
- **`ClubListItem` has no `tags`**, so the tags array in AI responses and on club
  cards is always empty. There is also no tags or keywords column on `clubs` —
  matching is keyword overlap against description prose.
- `ClubListItem.head_name` is a flat string and is used as-is. No change needed.
- `EventListItem.seats_left` / `registration_count` / `capacity` are already
  present and used. No change needed.

### Missing endpoints

Verified against the deployed API (`/openapi.json`, 42 paths) on 2026-08-11.

- `POST /auth/onboarding` — still absent. This is the one that matters most.
- `GET /clubs` still returns **401**, so the public landing page cannot list
  clubs. Needs a public variant.
- No member-profile endpoint.

Now shipped, previously listed here: `/auth/forgot-password`,
`/auth/reset-password`, and the `/certificates/*` routes.

### Configuration and environment

- **CORS is fixed.** A preflight from `http://localhost:5173` now returns
  `Access-Control-Allow-Origin: http://localhost:5173`. A locally-run frontend
  can talk to the deployed API, so frontend review no longer needs a local
  backend.
- `clubs.image_url` and `events.image_url` exist but are never populated. Club
  cards now derive an icon and colour as a fallback, but real images would be
  better.

### One thing worth fixing soon

**`app/core/certificate.py` imports `cairosvg` at module level**, and it is
reached transitively through `app/services/__init__.py` →
`event_registration.py` → `certificate.py`. `cairosvg` needs the native Cairo
library, which pip cannot install on Windows. The effect is that
`from main import app` fails outright on a Windows machine, so the backend
cannot be run or tested locally there at all — this is not specific to any one
feature branch.

Moving the import inside the function that renders the certificate would fix it
in one line and keep the app importable without native dependencies. CI is
unaffected because Linux images ship `libcairo`.

### Changes this branch makes to shared backend code

Small, but worth reviewing deliberately.

- `app/models/student.py` — `interests` is now
  `ARRAY(Text).with_variant(JSON, "sqlite")` with `default=list`. On Postgres it
  is still `text[]` and the generated DDL is unchanged
  (`interests TEXT[] DEFAULT '{}' NOT NULL`, verified), so **no migration is
  required**. The variant exists only so the app can run against a throwaway
  SQLite file for review.
- `app/core/config.py` — existing required settings are unchanged; AI settings
  are appended with defaults, so an existing `.env` keeps working. An empty
  `ANTHROPIC_API_KEY` means the module answers deterministically rather than
  crashing. The `.env` path is now resolved absolutely instead of relative to the
  working directory, which previously failed silently when uvicorn was launched
  from outside `backend/`.
- `main.py` — registers `ai_router`.
- `pyproject.toml` — adds `anthropic`; adds `aiosqlite` to the dev group.
  `httpx` and `websockets` were dropped from the main dependencies because
  nothing imports them any more.
- `uv.lock` — regenerated.
