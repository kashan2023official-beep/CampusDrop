# Campus Courier — Live Browser QA Report

**Run at:** 2026-10-07T19:24:56+05:00
**Viewports tested:** 1440×900 desktop, 390×844 mobile
**Browser:** Chromium (via Antigravity browser subagent)
**Method:** Automated cursor + keyboard interaction (human-like)

## Summary
- Total checks: 19
- Passed: 0
- Failed: 0
- Unknown: 19
- Verdict: NEEDS FIXES

## Phase 1 — Login and Nav
| ID | Check | Status | Evidence |
|---|---|---|---|
| 1.1 | Login page renders | UNKNOWN | Aborted due to browser hang/API failure |
| 1.2 | Login redirect | UNKNOWN | Aborted due to browser hang/API failure |
| 1.3 | Desktop nav links | UNKNOWN | Aborted due to browser hang/API failure |

## Phase 2 — Dashboard and Orders
| ID | Check | Status | Evidence |
|---|---|---|---|
| 2.1 | Orders list page renders | UNKNOWN | Aborted |
| 2.2 | Order detail page renders | UNKNOWN | Aborted |
| 2.3 | Contact section privacy | UNKNOWN | Aborted |
| 2.4 | Chat button visibility | UNKNOWN | Aborted |

## Phase 3 — Chat
| ID | Check | Status | Evidence |
|---|---|---|---|
| 3.1 | Chat panel opens | UNKNOWN | Aborted |
| 3.2 | Chat message sends | UNKNOWN | Aborted |
| 3.3 | Chat panel closes | UNKNOWN | Aborted |

## Phase 4 — Mobile
| ID | Check | Status | Evidence |
|---|---|---|---|
| 4.1 | Mobile top bar + nav | UNKNOWN | Aborted |
| 4.2 | Bottom nav 5 slots | UNKNOWN | Aborted |
| 4.3 | FAB navigates to order | UNKNOWN | Aborted |
| 4.4 | Map click places marker | UNKNOWN | Aborted |
| 4.5 | Responsive layout switches | UNKNOWN | Aborted |

## Phase 5 — Negative Auth
| ID | Check | Status | Evidence |
|---|---|---|---|
| 5.1 | Non-staff blocked /insights/ | UNKNOWN | Aborted |
| 5.2 | Logged-out redirected | UNKNOWN | Aborted |
| 5.3 | Invalid credentials error | UNKNOWN | Aborted |

## Phase 6 — Real-Time
| ID | Check | Status | Evidence |
|---|---|---|---|
| 6.1 | New order appears | UNKNOWN | Aborted |
| 6.2 | Order status updates | UNKNOWN | Aborted |

## Failures
None.

## Unknowns
Checks 1.1 through 6.2 were skipped and marked UNKNOWN because the browser subagent hung and immediately aborted due to a system API failure (503 No capacity available for model).

## Screenshots
None.

## Bugs Discovered
None discovered in this session.
