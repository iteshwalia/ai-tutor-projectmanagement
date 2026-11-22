# PM Mentor UI Regression Test Report

**Test date:** 22 November 2026
**Application baseline:** `262aeaa`
**Result:** **PASS — 26 tests**

PDF version: [REGRESSION_TEST_REPORT.pdf](REGRESSION_TEST_REPORT.pdf)

## Test setup

The browser suite starts a local Flask app with a temporary SQLite database, fresh browser contexts, and the built-in demo tutor. It does not use learner data or credentials from the deployed Render service. Browser checks run in Playwright Chromium.

## Regression matrix

| Case | Coverage | Result |
|---|---|---|
| UI-01 — Home and dialogs | Welcome/profile/topic display, topic-selector profile dialog, focus restoration, settings dialog open/close | Pass |
| UI-02 — Learner profile | Simulated HTTP 503, visible retry error, enabled retry button, successful Advanced save, dialog close, persistence after reload | Pass |
| UI-03 — Learning modes | Learn, Practice, Quiz, and Challenge prompts include the selected topic and difficulty | Pass |
| UI-04 — Learning and progress | Chat submission by Enter, quiz question and incorrect feedback, practice question and correct feedback, progress metrics, report download contents, session reset | Pass |
| API — Existing backend suite | Profile and question APIs, answer evaluation, progress, provider handling, security/configuration checks | Pass |

## Validation results

| Command | Result |
|---|---|
| `.\.venv\Scripts\python.exe -m pytest -q` | **26 passed** |
| `.\.venv\Scripts\ruff.exe check .` | Passed |
| `git diff --check` | Passed |
| `.\.venv\Scripts\python.exe -m playwright install chromium` | Passed |

GitHub Actions now installs Playwright Chromium before running Ruff and the complete pytest suite.

## Scope and limitations

- The browser suite uses Chromium only; Firefox and WebKit are not included.
- Model credentials are intentionally disabled; chat coverage exercises the demo tutor, not a live Gemini call.
- The suite runs against an isolated local app, not the deployed Render instance. Previous live deployment checks remain in [TEST_REPORT.md](TEST_REPORT.md).
- These are functional browser checks, not screenshot-based visual-diff or accessibility-audit tests.
