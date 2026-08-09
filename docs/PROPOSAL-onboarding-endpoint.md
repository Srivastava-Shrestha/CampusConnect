# Proposal: `POST /auth/onboarding`

**Raised from:** issue #46, item 3 ("Onboarding flow screens are not available")
**For:** backend owner
**Status:** frontend is already built and calling this route; backend route does not exist

---

## The problem

`frontend/src/views/OnboardView.vue` collects a student's profile across three
steps and submits it via `saveOnboarding()` in `frontend/src/api/auth.js`:

```js
export async function saveOnboarding(profile) {
  return apiRequest("/auth/onboarding", { method: "POST", body: JSON.stringify(profile) })
}
```

Against the deployed backend that route returns **404**:

```
POST https://campusconnect.itshrestha.dev/auth/onboarding   ->  404
POST https://campusconnect.itshrestha.dev/auth/login        ->  422   (control - route exists)
```

Live OpenAPI currently exposes only `/auth/login`, `/auth/signup`, and
`/college/onboarding` (the last is campus-admin college setup, a different
thing). So every student who completes onboarding silently loses their answers.

Worth noting: migration `138b941be66b_added_a_interest_column_in_student_table.py`
already added `students.interests`. **The column is there and waiting - only the
write path is missing.**

---

## What the frontend sends today

```json
{
  "dept": "cse",
  "year": "2",
  "interests": ["coding", "robotics"],
  "goal": "discover"
}
```

| Field | Type | Values |
|---|---|---|
| `dept` | string | a slug from the department grid, or free text when "Other" is picked |
| `year` | string | `"1"`, `"2"`, `"3"`, `"4"`, `"pg"`, `"diploma"` |
| `interests` | string[] | slugs from a fixed list of 12 (`coding`, `robotics`, `music`, `art`, `sports`, `literature`, `debate`, `entrepreneurship`, `science`, `gaming`, `photography`, `social`) |
| `goal` | string | `"discover"`, `"events"`, `"lead"` |

---

## Mismatches against the `students` table

This is the part worth agreeing on before anyone writes code.

| Frontend field | `students` column | Problem |
|---|---|---|
| `dept` | `branch` | **Naming only.** Map `dept -> branch`, or rename one side. |
| `year` | `year` (int) | **Type conflict.** Frontend can send `"pg"` and `"diploma"`, which are not integers. |
| `interests` | `interests` (`ARRAY(Text)`) | Fine, already matches. |
| `goal` | *(none)* | No column exists. |
| *(none)* | `roll_no` | Column exists; onboarding never asks for it. |

### On `year`

`Student.year` is `Mapped[int | None]`. `"pg"` and `"diploma"` cannot be stored
there. Three ways out, in order of preference:

1. **Widen the column to `String(16)`** (small migration). Keeps "PG" and
   "Diploma" as first-class values and needs no frontend change. Recommended.
2. Split into `year: int | None` + `program: str | None`.
3. Frontend maps `pg`/`diploma` to sentinel integers. Cheapest, but the
   sentinels leak into every future query - not recommended.

### On `goal`

Not stored anywhere today. Either add `goal String(32)` to `students`, or drop it
from the payload. Mild argument for keeping it: it is a useful signal for the AI
club recommender, which already scores on interest text.

---

## Suggested contract

```
POST /auth/onboarding
Authorization: Bearer <token>
```

**Request**

```json
{
  "branch": "cse",
  "year": "2",
  "interests": ["coding", "robotics"],
  "goal": "discover"
}
```

**Rules**

- Auth required; the student is taken from the token, never from the body.
- `branch` optional, max 64 chars.
- `year` optional, one of `1`, `2`, `3`, `4`, `pg`, `diploma`.
- `interests` optional, 0-12 entries, each from the fixed slug list, deduplicated.
- `goal` optional, one of `discover`, `events`, `lead`.
- Idempotent: re-running onboarding overwrites the previous answers rather than
  appending, so a student can redo it safely.

**Response `200`**

```json
{
  "branch": "cse",
  "year": "2",
  "interests": ["coding", "robotics"],
  "goal": "discover",
  "message": "Profile saved."
}
```

**Errors**

| Code | When |
|---|---|
| `401` | missing or invalid token |
| `403` | caller is not a student (e.g. a campus admin) |
| `422` | value outside the allowed sets above |

---

## Frontend changes needed once this lands

Small, and we will handle them:

1. Rename `dept` to `branch` in `OnboardView.vue`'s payload (or the backend
   accepts `dept` - either is fine, we just need to agree which).
2. Handle a failed save. `finishOnboarding()` currently `await`s with no
   `try/catch`, so a rejected request leaves the student on a dead step with no
   message. That is worth fixing regardless of this endpoint.

---

## Open questions

1. Widen `year` to string, or split it into `year` + `program`?
2. Add a `goal` column, or drop `goal` from the payload?
3. Should onboarding also capture `roll_no`, given the column already exists?
