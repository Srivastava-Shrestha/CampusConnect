# Bug Log

2026-07-25
[BUG] Invalid email_suffix domain format validation
- Endpoint: POST /college/onboarding
- Found during onboarding validation tests.
- API accepts malformed domains in the email_suffix field.
- Reproduced with email_suffix =
  - not_a_domain
  - .knit.edu.in
  - knit.edu.in.
  - knit..edu.in
  - admin@knit.edu.in
- Expected: 400/422
- Observed: 200
---
2026-07-26
[BUG] Case-sensitive email domain lookup
- Endpoint: POST /auth/signup, POST /auth/login
- Found during signup/login flow testing.
- Signing up with an uppercase email fails to log in with the lowercase version.
- Reproduced with email =
  - Signup: Pawan.Kumar@knit.edu.in
  - Login: pawan.kumar@knit.edu.in
- Expected: 200
- Observed: 401
---
2026-07-26
[BUG] Whitespace-only strings pass validation
- Endpoint: POST /auth/signup, POST /college/onboarding
- Found during signup and college onboarding validation tests.
- Fields accept strings made entirely of spaces; email_suffix isn't stripped before use.
- Reproduced with:
  - full_name = "     " (signup)
  - name = "     " (onboarding)
  - description = "     " (onboarding)
  - email_suffix = " knit.edu.in " → slug returned as " knit" instead of "knit"
- Expected: 422 for whitespace-only fields; slug without leading space
- Observed: 200 in all cases; slug retains leading space