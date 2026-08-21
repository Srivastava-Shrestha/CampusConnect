# Campus Connect - Session Report (2026-08-21)

Honest write-up of everything shipped in this chat window since 2026-08-19 (built on the AI
module branch, force-pushed to `dev`), how club recommendations actually work today (both the
AI module and the plain "Recommended" list on the member dashboard), the current AI agent
architecture, real test results, DB schema impact, and the frontend loading-speed tradeoff.
Nothing in this file was edited into the app - it is a report only.

---

## 1. Full changelog: everything shipped in this chat window, Aug 19 → Aug 21

This is the complete record, reconstructed from `git log` on `dev` (author `1mystic`, the
identity this session's commits were made under), not from memory - so it is accurate even
where earlier context in this conversation got compacted. All of it was built on
`feature/atharv-ai-module-v2` / directly on `dev` and is already force-pushed to `origin/dev`
(`local dev` and `origin/dev` are byte-identical as of this report - confirmed via
`git rev-list --left-right --count origin/dev...dev` returning `0  0`).

17 commits total, 2026-08-19 16:14 through 2026-08-21 (today's fix, not yet committed - see the
last row). Chronological, oldest first:

| # | Date/time | Commit | What it actually did |
|---|---|---|---|
| 1 | 08-19 16:14 | `2bf6566` | Merge commit bringing `dev`'s work (leaderboard, Google OAuth, image upload, notifications - other teammates' features) into this branch. No new code of its own. |
| 2 | 08-19 16:20 | `d1299b7` | Wired the onboarding flow to `PATCH /students/me` for real (it wasn't persisting before) and routed newly-signed-up students into onboarding instead of straight to the dashboard. Touched `api/students.js` (new, 70 lines), `useAuthSession.js`, `OnboardView.vue`. |
| 3 | 08-19 17:19 | `0891fe3` | **The AI Club Finder's first real implementation**, plus issue submission and club-proposal status. 24 files, +1784/-254. Built out `agent/loop.py`, `agent/tools.py`, `agent/memory.py`, `services/recommender.py` (its original location, before the later move into `agent/`), the `/ai` API, `IssueCard.vue`, `ClubProposalList.vue`, `clubVisuals.js` (the banner-colour helper used everywhere since), and three now-superseded handoff docs (`HANDOFF-AGENT.md`, `HANDOFF-STATUS.md`, `HANDOFF-TEAM.md`). |
| 4 | 08-19 19:11 | `f135e19` | **A large merge-reconciliation commit, not new authored work** - 300 files, +66875/-67439 lines. This is what happens when a long-lived feature branch resyncs against a fast-moving `dev`: it reverted `config.py`/`database.py` to `dev`'s versions (a divergent SQLite experiment was dropped in favour of `dev`'s Postgres-only setup), moved `llm_client.py`, `recommender.py`, `voice_budget.py` out of `services/` into their permanent home `agent/`, and picked up a huge amount of line-ending/whitespace churn across `openapi.yaml`, `style.css`, `package-lock.json`, and the entire `static-pages/` and `tests/integration/` trees from the merge itself. The honest read: almost none of that diff is hand-written change from this session - it's what the diff tool reports for a rebase-style resync, not a feature. |
| 5 | 08-19 21:29 | `cbad3b8` | Redesigned several frontend API endpoints and fixed component loading/routing. Deleted the old flat `api/members.js` and folded it into `certificates.js`/`clubs.js`; added `api/leaderboard.js`; reworked `ResultsView.vue`, `ViewCertView.vue`, `LeaderboardView.vue` layouts; backend-side added a leaderboard rank field to the membership schema. |
| 6 | 08-19 22:15 | `02753b4` | The first caching pass: added `utils/apiCache.js` (the TTL cache described in §6), wired graceful loading/empty/error states across ~20 views, added lazy component loading, fixed a wrong member-count display, fixed event-registration button timing, and general CRUD polish on events. |
| 7 | 08-19 22:24 | `629fd54` | Added member removal from a club, a public trending-clubs endpoint, a `links` field on clubs; fixed AI memory duplicate-recording bugs; continued the frontend loading/empty-state/caching overhaul; added cross-account state reset (the bug where switching demo accounts in one tab bled the previous account's data into the next - see `auth.js`'s `logout()`); added the landing-page trending-clubs marquee. |
| 8 | 08-20 10:10 → 10:17 | `3602a0a`, `40d555c` | Added a Postgres fallback for certificate storage (when S3 isn't configured - stores the PDF bytes directly in the DB, see `certificate.py`'s `_download_url`), URL-based club banners, the public trending endpoint's real backend, removed a half-built Google SSO UI, swept remaining empty states, added the `demoinstitute` demo college's seed data, and added traceback logging when the AI agent loop falls back to the deterministic path (so silent Anthropic failures would actually show up in logs). |
| 9 | 08-20 10:51 | `a17af03` | Enabled real S3 storage for certificates, restored the Google sign-in button UI, completed the reset-password flow end to end, fixed the club-leader theme colour and a wrong member-count on `LeaderClubView.vue`, added a reusable `Modal.vue`. |
| 10 | 08-20 11:04 | `15f82fb` | Added reset-password and logout to the profile page, fixed a mismatched "your reset link expired" message, wired real AWS/SMTP/Google credentials into config. |
| 11 | 08-20 11:19 | `bc2ebaa` | Renamed "reset password" to "change password" on the profile page (clearer for an already-logged-in user), fixed `/verify` requiring a serial in the URL when it should also work as a bare lookup form, made the profile logout button responsive on mobile. |
| 12 | 08-20 13:24 | `84da76e` | Restored real file-upload for club banners (it had regressed to URL-only), added profile picture upload, widened the sidebar for logo spacing. |
| 13 | 08-20 16:04 | `7e62e0c` | Added colour accents to the public club pages and the certificate-management component on the landing page - an earlier pass at what §1's `ClubProfileView.vue` fix (below) later corrected properly. |
| 14 | 08-20 16:37 | `66b4280` | **The AI latency rewrite** - collapsed the club-finder agent loop from a multi-round tool-calling loop to one deterministic-preprocess step + a single Claude call; fixed follow-up questions never reaching the model; parallelised `recommend_clubs`'s DB reads. Full architecture writeup in §3. |
| 15 | 08-20 16:49 | `68d0f69` | Same-day follow-up fix: the previous commit's grounding regex didn't yet tolerate the `[[club:7\|Label]]` tag-drift the model actually produced, so club cards weren't rendering. Fixed in both `loop.py` and `recommender.py`. |
| 16 | 08-20 17:15 | `92c8be2` | Fixed "remember me" at login not actually skipping the landing page - a logged-in visitor with "remember me" checked now goes straight to their dashboard instead of seeing the marketing page again. |
| 17 | 08-21 (today, **not yet committed**) | *(working tree)* | Today's only code change: the "Set Results" bug detailed just below. `git status` currently shows exactly three modified files - `event_registration.py`, `test_event.py`, `ResultsView.vue` - plus this report and its test-evidence folder as untracked. Not yet committed or pushed. (Everything else from this conversation - the certificate showcase section, the three club-profile bugs, the admin filter bug, the AI latency rewrite, the tag-drift fix, the remember-me fix - is already committed, in rows 13-16 above; each of those commit messages is a direct match for a fix made earlier in this same chat window before you committed it yourself.) |

### Today's bug: "Set Results" buttons showing as permanently disabled

You reported the Set Results page for "Attendance Test Event" showing every Winner/Runner-up
button disabled and a banner claiming "Results have already been published," even though you'd
only just taken attendance.

**Root cause (confirmed against the live DB):** `event_registrations` for that event held only
`PARTICIPANT` and `REGISTRANT` rows - zero `WINNER`/`RUNNER_UP` rows. Nothing had actually
declared results. The frontend's `alreadyDeclared` computed in `ResultsView.vue` was checking
`attendee.result !== 'REGISTRANT'` - but `PARTICIPANT` is the value attendance marking sets on
check-in, unrelated to result declaration. The instant you checked anyone in, the page
mis-read that as "results are already published" and locked itself.

**Fix 1 (real bug, frontend):** `alreadyDeclared` now only fires on an actual `WINNER` or
`RUNNER_UP` row.

**Fix 2 (your explicit ask - "I should be able to edit results even after the event is
complete"):** `declare_results()` in the backend used to hard-reject a second call with a 409
(`ResultsAlreadyDeclaredError`). That guard is removed. A leader can now re-declare results at
any time; whoever held the old winner/runner-up title and isn't picked again drops back to
`PARTICIPANT`. Certificate issuance was already idempotent per-registration (it diffs against
the existing certificate's `result` and only regenerates the PDF when it changed), so
re-declaring correctly updates certificates instead of duplicating them. Attendance itself is
still frozen once real results exist - that rule is unchanged and untouched.

---

## 2. How "Recommended" clubs on the member dashboard actually work

Short answer: **they aren't AI-ranked, and never call the AI module at all.**

`frontend/src/stores/clubs.js`:

```js
recommendedClubs: (state) => {
  const joinedIds = new Set(state.joinedClubs.map(club => club.id))
  return state.clubs.filter(club => !joinedIds.has(club.id))
}
```

This is "all clubs the student hasn't joined yet," full stop - no scoring, no interest
matching, no popularity weighting. `state.clubs` itself comes from `GET /clubs`, whose backend
query (`backend/app/repository/club.py`) is ordered by `Club.created_at.desc()` - newest club
first. So in practice, the "Recommended" badge on the club directory page currently means
**newest clubs you haven't joined, in creation order.**

There is a real, more sophisticated scorer sitting in the repo -
`frontend/src/utils/recommender.js` (interest-token overlap + popularity, a JS mirror of the
backend's deterministic core) - but grepping the whole frontend confirms it is **only imported
by its own test file** (`recommender.test.js`). It is not wired into any view. It appears to be
a leftover prototype from before the real backend recommender existed.

The actual AI-ranked recommendation logic (`select_recommendations()` in
`backend/app/agent/recommender.py`, described in §3) is only reached through the **AI Club
Finder** flow (`FindClubsView.vue` / `/ai/club-finder`, `/ai/chat`), not the plain club
directory page. If "Recommended" on the home/browse page is meant to reflect real interest
matching, that's a gap worth flagging to the team - right now it's presentational only.

---

## 3. How the AI module works now, and what kind of agent it is

**It is not an agentic loop, and it is not ReAct or Q-learning.** It was one earlier in this
project's history, and was deliberately downgraded for latency (see the docstring at the top of
`backend/app/agent/loop.py`, quoted in full):

> Earlier versions of this module ran a full multi-round tool-calling loop - the model called
> `get_my_clubs`, then `recommend_clubs`, then wrote its answer, each a separate Anthropic round
> trip. That measured at several seconds per turn (2-4 sequential network calls) and was the
> single biggest latency source in the whole app. The tools the model was calling were never
> actually optional... so letting the model spend two round trips *deciding* to call them
> bought nothing but slowness.

**What it is today: deterministic retrieval + one grounded generation call.** Sometimes called
"retrieve-then-generate" - closer to a single-pass RAG setup than to any agent-loop pattern:

```
1. Deterministic preprocessing (no model involved, runs in parallel via asyncio.gather):
     - get_my_clubs()       -> the student's own memberships
     - recommend_clubs()    -> select_recommendations() scores every club/event
                               (0.55*interest-overlap + 0.20*category + 0.10*branch + 0.15*popularity)
   Already-joined clubs are filtered out in code (a real filter, not a prompt instruction).

2. Exactly ONE Claude call (claude-haiku-4-5), with NO tools attached - the model
   architecturally cannot ask for another round trip. It receives a "DATA FOR THIS TURN"
   block (the clubs/events already selected above) and is told to phrase a reply from
   that data alone - it never decides what exists, only how to talk about it.

3. Output gates (grounding.py + recommender.py), unchanged from the old design:
     - allow-list: the model can only reference IDs a tool actually returned this turn
     - [[club:ID]] / [[event:ID]] tag resolution, with graceful fallback to "that option"
       for anything the model hallucinates
     - email scrubbing
     - read-only surface: nothing the model does can join a club, register for an event,
       or mutate anything

4. If Anthropic is unreachable, the API key is missing, or the call throws, it falls straight
   through to _deterministic_fallback() - the v1 path, select_recommendations() with a canned
   message and no LLM at all. This is what keeps the feature working offline / mid-outage.
```

**Contrast with the patterns named in the question, for clarity:**
- **ReAct** (reason -> act -> observe, repeated): this is what the *old* version of `loop.py`
  was, and what the (unimplemented) `docs`-referenced "mini-harness" design plan describes as a
  future bounded loop with tool schemas. It was removed from the live code specifically because
  those round trips were the dominant latency cost.
- **Q-learning / RL**: not applicable and not present anywhere in this codebase. There's no
  reward signal, no policy being learned, no exploration/exploitation - `select_recommendations`
  is a fixed, hand-weighted linear scoring function (`ScoreConfig`), not a learned one.
- What actually ships is closer to **"tool calling promoted out of the model and into
  application code, followed by a single constrained generation call."** The interesting
  engineering is in the deterministic core and the four grounding gates, not in any loop.

Also fixed this session, as a byproduct of this rewrite: **follow-up questions were being
silently dropped.** `history` used to only get seeded with the student's typed interest text
when the conversation was empty (turn 1). From turn 2 onward, whatever the student actually
typed next never reached the model. Now the current turn's text is always appended as the
newest user message.

---

## 4. AI module tests

Real pytest run, captured this session (raw terminal output saved to
`docs/test-evidence/ai-module-pytest-2026-08-21.txt` - there is no screenshot tool available
for a headless WSL pytest run, so this is a full unedited console capture rather than a PNG).

**27 / 27 passed. 0 failed. 100%.** Runtime: 0.23s (fully offline - no network, no DB, no
Anthropic API key needed; `call_finder`/`call_chat` run against a deterministic mock client).

| # | Test | Given input | Expected | Actual | Pass |
|---|---|---|---|---|---|
| 1 | `test_stopwords_and_short_tokens_removed` | `"I want to join a club for robotics"` | tokens == `{"robotics"}` | `{"robotics"}` | ✅ |
| 2 | `test_exact_interest_match_scores_high` | profile interests `["robotics","drones"]` vs Robotics Club | score ≥ 0.5 | ≥ 0.5 | ✅ |
| 3 | `test_no_overlap_below_threshold` | profile `["poetry"]` vs Robotics Club | score < 0.30 | < 0.30 | ✅ |
| 4 | `test_deterministic` | same profile+club scored twice | equal both times | equal | ✅ |
| 5 | `test_score_bounded` | 4-word interest match | 0.0 ≤ score ≤ 1.0 | in range | ✅ |
| 6 | `test_popularity_breaks_ties` | two identical-text clubs, activity 90 vs 5 | higher-activity club scores higher | did | ✅ |
| 7 | `test_empty_interests_still_ranks_via_branch_and_pop` | no interests, branch `cse` vs Robotics (technology) | score > 0.0 (branch+popularity carry it) | > 0.0 | ✅ |
| 8 | `test_event_interest_match` | interests `["astronomy","stargazing"]` vs "Astro Night" event | score ≥ 0.25 | ≥ 0.25 | ✅ |
| 9 | `test_clubs_first_when_match` | interests `["robotics"]`, clubs=[Robo,Poetry] | `kind=="clubs"`, top item id 1 | matched | ✅ |
| 10 | `test_event_fallback_when_no_club` | interests match an event, no club | `kind=="event_fallback"`, message mentions "organiser" | matched | ✅ |
| 11 | `test_event_fallback_never_exposes_email` | event fallback with a named leader | no `@` in the message | none | ✅ |
| 12 | `test_irrelevant_event_not_surfaced` | event shares nothing with interests | falls to `kind=="popularity"` | did | ✅ |
| 13 | `test_popularity_when_nothing_matches` | interest `["knitting"]`, no match anywhere | `kind=="popularity"`, top item = highest activity_score | matched | ✅ |
| 14 | `test_valid_array` | `[{"club_id":1,"reason":"builds robots"}]` | parses through unchanged | unchanged | ✅ |
| 15 | `test_strips_code_fences` | JSON wrapped in ```` ```json ```` fences | fences stripped, parses | stripped | ✅ |
| 16 | `test_drops_hallucinated_id` | one real id (1) + one fake id (99) | only id 1 survives | `[1]` | ✅ |
| 17 | `test_malformed_raises` | `"Sure! here you go"` (not JSON) | raises an exception | raised | ✅ |
| 18 | `test_empty_array_ok` | `"[]"` | returns `[]` | `[]` | ✅ |
| 19 | `test_dedupes` | same club_id twice in the array | collapses to one entry | 1 entry | ✅ |
| 20 | `test_known_entity_resolved` | `"Try [[club:1]] today"`, allow-list has club 1 | `"Try Robotics Club today"`, no unknowns | matched | ✅ |
| 21 | `test_unknown_entity_not_surfaced` | `"Check [[club:77]]"`, 77 not in allow-list | `"77"` never appears; text says "that option"; unknown list records `("club",77)` | matched | ✅ |
| 22 | `test_plain_text_passthrough` | plain text, no tags | text unchanged, no unknowns | unchanged | ✅ |
| 23 | `test_email_scrubbed` | `"contact lead@knit.ac.in please"` | no `@` in output | none | ✅ |
| 24 | `test_call_finder_returns_json_for_every_candidate_in_prompt` | 2 candidate clubs in prompt | mock returns a reason for both ids {1,2} | matched | ✅ |
| 25 | `test_call_finder_is_cached_for_the_same_prompt_and_hash` | same prompt/hash called twice | identical output both calls (cache hit) | identical | ✅ |
| 26 | `test_call_chat_references_a_club_from_available_block` | 1 club in AVAILABLE block, user asks "robots?" | reply contains `[[club:1]]` | contained | ✅ |
| 27 | `test_call_chat_falls_back_gracefully_with_nothing_available` | AVAILABLE block says nothing exists | reply contains no `[[` tags at all | none | ✅ |

**What this suite does *not* cover:** it tests the deterministic scoring core
(`recommender.py`) and the mocked LLM client contract (`llm_client.py`) - both fully offline.
There is **no `test_agent_loop.py` and no `test_agent_tools.py`** in the repo - a design
document (`plans/project-campus-connect-team-kind-heron.md`) sketches those as a future Phase 5,
but they were never written. The single-call `run_agent_turn()` orchestration in `loop.py`
itself (the parallel `asyncio.gather`, the fallback branches, the budget/logging) has no direct
unit test today - it's only exercised indirectly through manual testing and the live server. If
"how well-tested is the AI module" needs a stronger answer for a viva, that orchestration layer
is the honest gap.

**Separately, this session's backend fix** (`declare_results` allowing a second call) was
verified against `backend/tests/integration/test_event.py`, which hits the real Neon DB rather
than a mock. That run currently errors before it even reaches my new/changed tests - a shared
fixture (`leader`) does `POST /clubs` against the live database and gets back a response with no
`id` key, which looks like unrelated integration-environment/test-data drift (confirmed
pre-existing: an untouched test, `test_declare_results_success`, fails on the exact same
fixture). This is not something this session's two edits caused, but it does mean the new test
(`test_declare_results_twice_swaps_winner`) is unverified by an actual DB run right now - only
by direct inspection and by manually querying event 18's live registration rows, which confirmed
the underlying data story matches what the fix assumes. Worth a follow-up session to fix the
`leader` fixture / integration DB state before trusting that suite's green light on anything.

---

## 5. Database schema changes this run

**None.** Every change in this session (§1) touched application code only -
`app/agent/*.py`, `app/services/event_registration.py`, and Vue components/CSS. No
`app/models/*.py` file was edited, and no migration was written or run.

Two things worth calling out on this specifically:

- The AI module's durable per-student memory (`backend/app/agent/memory.py`) is **not** a DB
  table. It's deliberately a small JSON file (`backend/var/student_memory.json`), capped at 10
  facts/student, written only from confirmed system events (never from the model). The
  module's own docstring says explicitly: *"If this outgrows a file, the shape below maps
  one-to-one onto an `ai_student_memory` table"* - i.e. schema growth was scoped and deferred on
  purpose, not accidentally skipped.
- The design plan on file (`plans/project-campus-connect-team-kind-heron.md`, Phase 2/3)
  proposes real schema-adjacent work that has **not** been done: replacing the mock discovery
  layer with real queries, and a genuine `ai_student_memory` table. None of that is in the
  current codebase - the AI module still runs against the live schema read-only, through the
  same service layer every other router uses, with zero new tables or columns.

So yes - additive-or-nothing is exactly what happened here, but "additive" undersells it: this
run added zero schema surface at all, matching the constraint (documented in the plan) that
schema changes should be minimal and justified, not proactive.

---

## 6. Why pages feel slow, and what's actually true about the tradeoff

**What's really going on:** every routed view fetches its own data inside Vue's `onMounted()`
hook. A grep of `frontend/src/views/` confirms this pattern in all 28 view files. Vue destroys
and rebuilds a component's local state every time you navigate away and back, so a plain
`onMounted` fetch reruns from scratch on every single visit - there's no "is this still fresh"
check by default.

Two mitigations already exist in the codebase, worth knowing about before assuming nothing's
been done:

- `clubsStore` / `eventsStore` (Pinia) guard with `if (this.loaded) return` - once loaded, they
  don't refetch on remount, only on an explicit `refreshClubs()` call or on logout
  (`auth.js`'s `logout()` resets both stores). So club/event data specifically is *not*
  reloading on every click already.
- `frontend/src/utils/apiCache.js` is a small in-memory cache with a 2-minute TTL
  (`cachedFetch(key, fetchFn, ttlMs)`), built specifically for views that fetch into a local ref
  instead of a store - its own comment says exactly this: "navigating away and back re-ran the
  request from scratch every single time... this gives those views the same property [as the
  stores] without turning each one into a Pinia store." Not every view uses it yet, though - it
  has to be adopted per-view.

**The honest tradeoff to tell the client:** Neon (serverless Postgres) trades raw latency for
zero-ops accuracy - every read is a live query against the same database every write goes to,
so nothing shown is ever stale by more than the time of one request, and there's no cache-
invalidation bug class to worry about. The cost is that a cold Neon connection (its serverless
compute can suspend when idle) plus FastAPI's per-request async DB round trip is measurably
slower than an app backed by an always-warm, provisioned instance or a read cache. That's a
real, defensible architecture choice for a project at this stage (no ops budget, correctness
matters more than shaving milliseconds off a demo click) - but it should be named as a tradeoff,
not implied to be free.

**What would actually make it feel faster**, in order of effort:

1. **Cheapest, no architecture change:** replace bare `onMounted(() => fetch())` in the views
   that don't already use a store, with `apiCache.js`'s `cachedFetch()` - it already exists and
   is already proven on some views. This alone stops "click into a page I was just on" from
   re-hitting the network.
2. **Lifecycle-hook change you specifically asked about:** this isn't really a "switch
   `onMounted` for a different hook" problem - Vue doesn't have a hook that means "only fetch if
   stale." The actual fix is the pattern above (a module-level cache/store the component reads
   from, with `onMounted` becoming "read from cache, fetch only if missing/stale") rather than a
   different lifecycle hook. `onMounted` itself is fine and correct; the bug is having no
   staleness check *at all* before firing the request inside it.
3. **A step further:** extend the `loaded`/TTL pattern to background-refresh - show cached data
   immediately on mount, then silently refetch after a few minutes and only update the view if
   the response actually differs (stale-while-revalidate). This gets "feels instant" without
   ever showing genuinely stale data for more than the refresh window - exactly the "refresh
   every 3-4 minutes" idea, just applied as a background revalidation instead of a blocking
   fetch on every click.
4. **Backend-side, if it's still not enough:** the 45-endpoint API layer could add
   short-TTL server-side caching for read-heavy, rarely-changing endpoints (club lists,
   directory pages), which would make the *first* load fast too, not just repeat visits - but
   that's a bigger change than anything above and should only be reached for if 1-3 aren't
   enough.

None of the above (1-3) requires touching the database or weakening correctness - they only
change when the frontend decides to ask again, never what it's allowed to show once it does.

---

## 7. Module map, with coupling and cohesion

The backend is layered top-to-bottom: `api` (routers) -> `services` (business rules) ->
`repository` (SQL) -> `models` (SQLAlchemy tables). The AI module sits beside that stack as its
own package (`app/agent/`) and only ever talks to the rest of the app through the same
`services` layer everything else uses - it has no repository or model of its own except the
JSON memory file.

"Cohesion" below means: how tightly do the responsibilities *inside* one module belong together.
"Coupling to the rest" means: how much does this module know about / depend on other modules'
internals (high coupling = fragile to change elsewhere; low coupling = can be modified or
replaced in isolation).

| Module | Backend files | Cohesion | Coupling to rest of app | Why |
|---|---|---|---|---|
| **Club module** | `api/club.py`, `services/club.py`, `repository/club.py`, `models/club.py` | High | Medium | Single clear responsibility (CRUD + directory + trending list). Coupled to Membership (approval counts) and Student (leader lookups) via joins, and to College for scoping - unavoidable, since a club without a college or a leader isn't a valid club. |
| **Event + registration module** | `api/event.py`, `services/event.py` + `services/event_registration.py`, `repository/event.py` + `repository/event_registration.py`, `models/event.py` + `models/event_registration.py` | Medium | Medium-High | Two closely related but distinct concerns (event lifecycle vs. per-student registration/attendance/results) live under one API surface. Reasonably cohesive as "everything about one event," but it reaches into Certificate (queues `issue_certificate_job` on result declaration) and Notification (posts on register/attend/result) - a leader declaring results fans out into two other modules' write paths. |
| **Membership module** | `services/membership.py`, `repository/membership.py`, `models/membership.py` | High | High | Small and focused (join/approve/leave a club), but it's the join table nearly everything else checks - Club (leader lookup), Event (is this student allowed to register), the AI module's `get_my_clubs`. Central and therefore high-coupling by necessity, not by accident. |
| **Certificate module** | `api/certificate.py`, `services/certificate.py`, `core/certificate.py` (PDF render), `models/certificate.py`, `repository/certificate.py` | High | Low-Medium | Self-contained: given a registration id it renders a PDF, stores it (S3 or Postgres fallback), and exposes public verify/download routes. Only reads from EventRegistration; nothing else reads from it except the public `/verify` flow. One of the cleaner-boundaried modules in the app. |
| **AI module (`app/agent/`)** | `tools.py`, `loop.py`, `recommender.py`, `llm_client.py`, `grounding.py`, `memory.py`, `budget.py`, `demo_data.py` | High | Low (by design) | Internally very cohesive - every file has one job (scoring, prompting, gating, memory, budget accounting) and `tools.py` is the single seam through which it reaches the rest of the app (via `Services`, a plain dataclass of already-instantiated service objects). It never imports a repository directly and never writes anything outside its own JSON memory file. This low coupling is deliberate and stated in the module's own docs - it's what lets the whole feature degrade to a canned deterministic response without the rest of the app knowing or caring. |
| **Announcement / Issue / Notification / Leaderboard modules** | one `api` + `service` + `repository` + `model` file each | High | Low | Each is a straightforward CRUD-shaped slice scoped to a club or student. Notification is reached *from* other modules (event, membership, certificate all call into it to post) but does not call back into any of them - a clean one-directional dependency, which is the right shape for a notification sink. |
| **Auth / User / Student / College modules** | `api/auth.py`, `api/student.py`, `api/college.py`, matching services/repos/models | Medium-High | High (unavoidable) | These are the identity/scoping backbone - `college_id` and `student_id` are threaded through nearly every other module's queries (multi-tenancy by college). High coupling here is structural, not a smell: it's the mechanism that keeps one college's data from leaking into another's, including inside the AI module's tool calls. |

**Frontend**, by the same read: `stores/` (Pinia, one per domain: clubs, events, announcements,
notifications, guidelines) are the cohesive, low-coupled units - each owns one slice of state
and is only coupled to its own `api/*.js` file. `views/` are the highly-coupled layer by nature
(a page necessarily pulls together whichever stores/composables/components it needs) - that's
expected and fine for a view layer, not a design flaw.

---

## 8. Directory structure and contents, in brief

### `backend/app/`

| Directory | Contents |
|---|---|
| `api/` | FastAPI routers - one file per domain (`club.py`, `event.py`, `auth.py`, `ai.py`, `certificate.py`, `student.py`, `college.py`, `issue.py`, `announcement.py`, `notification.py`, `leaderboard.py`). Thin: parses the request, calls a service, returns its result. No business logic lives here. |
| `services/` | Business rules - one file per domain, mirroring `api/`. This is where validation, ordering-of-operations, and cross-module calls (e.g. `event_registration.py` calling into notification and certificate) live. |
| `repository/` | Raw SQLAlchemy queries - one file per domain, mirroring `services/`. Nothing here decides *whether* an action is allowed, only how to read/write the rows for it. |
| `models/` | SQLAlchemy ORM table definitions - one file per table/domain. |
| `schemas/` | Pydantic request/response models - the API's public shape, decoupled from the ORM models. |
| `agent/` | The whole AI module, self-contained (see §7): `tools.py` (registry + `Services` dataclass), `loop.py` (turn orchestration - see §3), `recommender.py` (deterministic scoring core + grounding regexes), `llm_client.py` (the Anthropic call wrapper, with a deterministic mock mode for offline tests), `grounding.py` (allow-list + output gates), `memory.py` (the JSON-file durable memory, §5), `budget.py` / `voice_budget.py` (per-turn token/cost accounting for the report's cost math), `demo_data.py` (the offline-tier sample campus). |
| `core/` | Cross-cutting infrastructure: `config.py` (settings/env), `database.py` (async engine/session), `certificate.py` (PDF rendering), `storage.py` (S3 with local-Postgres fallback), `messages.py` (user-facing string constants). |
| `exceptions/` | One `AppException` subclass per domain error (e.g. `ResultsAlreadyDeclaredError`), each carrying its own HTTP status code - this is what lets services `raise` a domain error and have it turn into the right HTTP response without every router needing its own try/except. |
| `templates/` | Server-rendered assets (e.g. certificate PDF template inputs). |
| `utils/` | Small stateless helpers shared across the backend. |

### `frontend/src/`

| Directory | Contents |
|---|---|
| `views/` | 34 route-level page components (one per router entry) - `HomeView`, `ClubDirectoryView`, `EventDetailView`, `ResultsView`, `AdminApprovalsView`, etc. Each owns its own `onMounted` data-fetch and page-specific state (see §6 for why that matters). |
| `stores/` | Pinia stores - one per domain that needs state shared across views: `clubs.js`, `events.js`, `announcements.js`, `notifications.js`, `guidelines.js`, plus `auth.js` for session/role state. This is the layer that already avoids refetching on every navigation (the `loaded` guard, §6). |
| `api/` | One thin fetch-wrapper file per backend domain (`clubs.js`, `events.js`, `ai.js`, `certificates.js`, `auth.js`, `students.js`, `issues.js`, `leaderboard.js`, `announcements.js`, `notifications.js`) - each just shapes a request/response for its store or view, no business logic. |
| `composables/` | Reusable, framework-idiomatic scripts (Vue's `use*()` convention) that aren't tied to one view: `useChipFilter.js` (the filter-chip logic reused across directory/admin pages), `useFormValidation.js`, `usePasswordStrength.js`, `useAuthSession.js` (post-login session bootstrap), `useGoogleAuth.js`, `useLoadingBar.js` (the top progress bar on route change), `useNarrator.js` (browser `speechSynthesis` voice-over for the AI finder), `useToast.js`, `useScrollReveal.js`. Several ship their own colocated `*.test.js`. |
| `utils/` | Plain, non-Vue-specific helper modules: `apiCache.js` (the TTL cache from §6), `clubVisuals.js` (banner colour/icon/status-mapping helpers, used to keep club cards visually consistent across views), `markdown.js` (renders the AI assistant's Markdown replies), `recommender.js` (the unused legacy JS scorer from §2). |
| `components/` | Shared UI building blocks, split into `layout/` (sidebars, shells, nav) and `ui/` (cards, buttons, and other presentational pieces like `ClubCard.vue` reused across many views). |
| `router/` | `index.js` - route table (`publicRoutes` / `studentRoutes` / `leaderRoutes` / `adminRoutes`) plus `resolveGuardTarget()`, the role-based navigation guard that redirects based on `auth.role` / `auth.canManageClubs` before any route resolves. |
| `assets/` | `style.css` - the entire app's hand-written CSS, organised into ~72 numbered sections (see `STYLE-INDEX.md` at the project root for the section table) - no CSS framework, no scoped-per-component styles. |

Test files throughout both trees are colocated with the code they test (`*.test.js` next to its
module in `frontend/src`, `backend/tests/` mirroring `backend/app/`'s structure for integration
tests plus the two offline `test_llm_client.py` / `test_recommender.py` files at the top level)
rather than gathered into one separate tree.
