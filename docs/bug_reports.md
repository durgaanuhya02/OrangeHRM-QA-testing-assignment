# Potential Bugs / Usability Issues — Login Page

**Application:** OrangeHRM Open Source Demo
**URL:** https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
**Reported By:** [Your Name]
**Date:** [Date]

> **Labeling convention used below:** every item is explicitly labeled either **"Potential Bug / Edge Case to Verify"** (behavior was observed once and is worth a second opinion or product-team judgment call before being treated as a defect) or **"Confirmed Behavior (Usability Concern)"** (the behavior was directly reproduced during testing, but is a design/UX judgment call rather than a functional defect). None of the three items below are claimed as confirmed *functional* bugs — the login form works correctly for its core purpose (accepting valid credentials, rejecting invalid ones). These are lower-severity observations a real QA pass would flag for product/UX review.

---

### BUG_001 — No client-side trimming of leading/trailing whitespace in the Username field

| Field | Details |
|---|---|
| **Bug Title** | Username field accepts and submits leading/trailing whitespace without trimming |
| **Description** | If a user accidentally types a leading or trailing space along with a correct username (e.g. `"  Admin  "`), the login is rejected with the same generic "Invalid credentials" message used for genuinely wrong credentials. Most modern login forms trim incidental whitespace before validating, since it's a common copy-paste/autofill artifact. |
| **Preconditions** | Login page loaded |
| **Steps to Reproduce** | 1. Enter `  Admin  ` (with leading/trailing spaces) in the Username field 2. Enter the correct password `admin123` 3. Click Login |
| **Expected Result** | Arguable either way — a strict app may reasonably treat this as invalid; a more forgiving one would trim it and log the user in. There is no universally "correct" expected result here, which is exactly why this is flagged for review rather than filed as a definite defect. |
| **Actual Result** | Login fails with "Invalid credentials" — confirmed and reproduced directly during testing (see TC_LOGIN_08) |
| **Severity** | Low |
| **Priority** | Low |
| **Environment** | Chrome (latest), Windows 11, `opensource-demo.orangehrmlive.com` |
| **Recommendation** | **Potential Bug / Edge Case to Verify.** Recommend confirming with the product owner whether whitespace-trimming is desired UX; if so, trim both fields client-side before submission. If intentional (e.g. for security-conscious exact-match behavior), no change is needed, but the generic error message means a user who fat-fingered a leading space gets no hint about *why* their otherwise-correct credentials failed. |

---

### BUG_002 — Generic "Invalid credentials" message does not distinguish failure reasons

| Field | Details |
|---|---|
| **Bug Title** | Login error message does not differentiate between "unknown username," "wrong password," or "malformed input" (e.g. accidental whitespace) |
| **Description** | Every rejected login — wrong username, wrong password, or both — shows the identical message "Invalid credentials." This is a deliberate and common security practice (it avoids telling an attacker which part of the credentials was wrong, i.e. it prevents username enumeration), so it is arguably correct behavior rather than a defect. It is flagged here purely as a usability trade-off worth documenting. |
| **Preconditions** | Login page loaded |
| **Steps to Reproduce** | 1. Try logging in with a wrong username + right password 2. Try logging in with right username + wrong password 3. Compare the two error messages |
| **Expected Result** | N/A — this is a security-vs-usability trade-off, not a clear-cut expected result |
| **Actual Result** | Both scenarios show the exact same "Invalid credentials" message — confirmed and reproduced during testing (TC_LOGIN_02, TC_LOGIN_03, TC_LOGIN_04) |
| **Severity** | Low |
| **Priority** | Low |
| **Environment** | Chrome (latest), Windows 11, `opensource-demo.orangehrmlive.com` |
| **Recommendation** | **Confirmed Behavior (Usability Concern), not recommended for change.** This is standard, defensible security practice (prevents username enumeration attacks). Documenting it here as a deliberate design decision rather than a bug, so it isn't mistakenly "fixed" in a way that would introduce a security regression. |

---

### BUG_003 — No visible account-lockout, rate-limiting, or CAPTCHA feedback after repeated failed attempts

| Field | Details |
|---|---|
| **Bug Title** | No observable protection or user feedback after multiple consecutive failed login attempts |
| **Description** | Brute-force protection (temporary lockout, increasing delay, or a CAPTCHA challenge after N failed attempts) is a standard login-security control. This was **not tested** against the shared public demo instance, because deliberately hammering the shared `Admin` account with failed logins could lock out or disrupt other people using the same public demo at the same time. This item is therefore based on the *absence of any visible client-side indication* (e.g. a CAPTCHA appearing, a "too many attempts" message) during normal testing — not on an actual lockout attempt. |
| **Preconditions** | Login page loaded |
| **Steps to Reproduce (NOT executed, documented for a controlled/isolated environment only)** | 1. In an isolated test environment (not the shared public demo), attempt login with an invalid password 10+ times in quick succession 2. Observe whether the account locks, a delay is introduced, or a CAPTCHA appears |
| **Expected Result** | Some form of rate-limiting, temporary lockout, or CAPTCHA should appear after a reasonable number of failed attempts, to mitigate brute-force credential-guessing attacks |
| **Actual Result** | Not executed — flagged as unverified rather than assumed. No lockout/CAPTCHA UI was observed during the limited number of failed-login tests performed (TC_LOGIN_02–04), but that is far too few attempts to draw a conclusion either way |
| **Severity** | Medium (if genuinely absent — unverified) |
| **Priority** | Medium |
| **Environment** | Chrome (latest), Windows 11, `opensource-demo.orangehrmlive.com` |
| **Recommendation** | **Potential Bug / Edge Case to Verify.** Recommend this be tested only in an isolated/sandboxed instance of OrangeHRM (never the shared public demo), by a tester or security reviewer authorized to do so. If no rate-limiting exists, recommend adding one as a standard security hardening measure. |

---

## Summary

| ID | Title | Classification | Severity |
|---|---|---|---|
| BUG_001 | Username whitespace not trimmed | Potential Bug / Edge Case to Verify | Low |
| BUG_002 | Generic error message for all invalid-credential cases | Confirmed Behavior (Usability Concern) — recommended to keep as-is | Low |
| BUG_003 | No visible brute-force protection feedback | Potential Bug / Edge Case to Verify (untested by design) | Medium |
