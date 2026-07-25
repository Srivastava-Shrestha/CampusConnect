# Bug Log

## 2026-07-25 — College onboarding accepts invalid domain format

**Endpoint:** POST /college/onboarding
**Test:** test_onboarding_malformed_email_suffix_fails
**Input:** email_suffix = "not_a_domain"
**Expected:** 400 or 422
**Actual:** 200 (college got created anyway)
