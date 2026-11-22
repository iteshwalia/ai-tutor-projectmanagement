# PM Mentor Test Report

**Test date:** 22 November 2026  
- **Previously deployed release:** `7ef2f07419cb69acb9a8415fb4d2b0ba6df28884`
- **Current deployment:** `6b41578a8ccffeb1dc77a876530f08f69997342e`
- **Deployment:** [https://pm-mentor.onrender.com](https://pm-mentor.onrender.com/)

The historical scroll-test evidence below is for the previous release. Follow-up source validation and current deployment evidence are recorded separately.

## Result

**Pass.** Automated tests, lint, and Python compilation passed. The current source is deployed; a fresh browser check confirmed the Itesh profile and Gemini configuration. A live Gemini response was also verified.

## Automated checks

| Check | Result |
|---|---|
| `.\.venv\Scripts\python.exe -m pytest` (release commit) | Passed: 14 tests |
| `.\.venv\Scripts\python.exe -m ruff check .` | Passed: no lint issues |
| `.\.venv\Scripts\python.exe -m compileall -q app.py backend tests` | Passed |
| GitHub Actions CI for the release commit | Passed: [workflow run 2](https://github.com/iteshwalia/ai-tutor-projectmanagement/actions/runs/45027726219) |

The automated tests cover page and health endpoints, frontend module serving, demo chat responses, input validation, question generation and evaluation, progress updates and reset, profile validation and persistence, model-request forwarding with a mocked provider, HTTPS endpoint restrictions, secret-safe status output, production configuration, session-cookie contents, and security headers.

## Follow-up source validation

The current source adds Gemini configuration, expands the question and demo-knowledge base, and changes the default learner name to Itesh. Local verification passed **19 tests**, Ruff, Python compilation, and `git diff --check`. Tests cover Gemini request defaults and secret-safe status, expanded CPMAI content, and migration of the legacy placeholder profile. Automated provider forwarding is mocked; a separate live check confirmed the configured Gemini provider.

- Render manually deployed commit `6b41578` successfully and reports it Live.
- A fresh page load showed the learner name as **Itesh** and the updated Gemini setup instructions.
- The already-open browser tab still displayed the older cached page until refreshed or reopened.
- After the Gemini environment group was connected, `GET /api/status` reported `api_configured: true`, `key_name: GEMINI_API_KEY`, provider `Google Gemini`, and model `gemini-3.5-flash-lite`.
- A harmless live chat prompt (“Explain the critical path in one sentence.”) returned a project-management explanation, and the UI identified the source as Google Gemini.

## Live deployment checks

- Render built the Docker image and reported the service live for the release commit.
- `GET /healthz` returned `{"status":"ok"}`.
- The deployed homepage loaded in the browser.
- After four sequential chat exchanges, waiting for each reply to finish, the chat container measured 240 px high with 1,166 px of message content. Its scroll position was 925.6 px of a 926 px maximum (0.4 px from the bottom), confirming it remained scrollable and followed the latest reply.

## Limitations and follow-up

- A live Gemini request was verified. The OpenAI-compatible alternative has not been tested with a live credential; automated provider-forwarding tests use mocked HTTP responses.
- Gemini's free tier has usage limits, and Google may use free-tier prompts to improve its products. Do not send sensitive, confidential, or personally identifying information; check Google's current [Gemini API terms](https://ai.google.dev/gemini-api/terms).
- The Render Free service can sleep while idle, and its local SQLite storage is ephemeral. Cold starts and loss of learner progress after restarts or redeploys are expected on this tier.
- The repository is deployed from a public-repository URL. New commits may require a manual Render deploy unless the repository is connected through Render's Git provider integration.
