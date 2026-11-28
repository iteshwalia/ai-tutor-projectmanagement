# PM Mentor Regression Test Report

**Report date:** 28 November 2026
**Result:** **PASS — 31 tests**

Word edition: [REGRESSION_TEST_REPORT.docx](REGRESSION_TEST_REPORT.docx)

## Test setup

The automated browser suite runs the application locally with a temporary SQLite database and the demo tutor. It does not use learner data or credentials from the deployed service. API tests mock external model calls where model behavior is under test.

## Regression matrix

| Case | Coverage | Result |
|---|---|---|
| API — Profile and session | Profile validation, persistence, default profile migration, cookie contents, reset | Pass |
| API — Questions and evaluation | Topic/difficulty matching, fresh model question per request, wrapped JSON and labeled-choice parsing, answer text and option-letter matching, malformed model response | Pass |
| API — Feedback and progress | Correct/incorrect scoring, personalized feedback using learner and topic progress, topic best practices, progress report | Pass |
| API — Tutor and configuration | Demo chat, model request forwarding, Gemini defaults, provider status, HTTPS enforcement, production secret requirement | Pass |
| UI-01 — Home and dialogs | Welcome/profile/topic display, profile dialog, settings dialog, focus restoration | Pass |
| UI-02 — Profile recovery | Simulated save failure, visible retry guidance, successful save, reload persistence | Pass |
| UI-03 — Learning modes | Learn, Practice, Quiz, and Challenge prompts include selected topic and difficulty | Pass |
| UI-04 — Practice and quiz flow | Quiz length validation (1–20), sequential questions, final score report, lowercase option-letter submission, incorrect and correct feedback, personalized feedback, best-practice tips, metrics, report download, reset | Pass |

## Validation results

| Command | Result |
|---|---|
| `python -m pytest -q` | **31 passed** (27 API, 4 browser) |
| Ruff checks on changed Python and JavaScript paths | Passed |
| `git diff --check` | Passed |

## Scope and limitations

- Automated browser coverage uses Chromium and an isolated local app.
- The browser suite uses demo mode. Provider request behavior is verified with mocked responses, not live credentials.
- This is functional regression coverage; it does not include screenshot-based pixel comparison or a full assistive-technology audit.
- Manual responsive visual observations and the option-letter fix are documented in [VISUAL_TEST_REPORT.md](VISUAL_TEST_REPORT.md).
- No live Render deployment check was performed for this report.
