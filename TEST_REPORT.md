# PM Mentor Test Report

**Test date:** 22 November 2026  
**Release commit:** `7ef2f07419cb69acb9a8415fb4d2b0ba6df28884`  
**Deployment:** [https://pm-mentor.onrender.com](https://pm-mentor.onrender.com/)

The live deployment evidence in this report is for the release commit above. Follow-up source validation is recorded separately and has not yet been deployed.

## Result

**Pass, with an AI-provider limitation.** The release's automated suite, lint, and Python compilation passed. The scrolling fix was deployed and verified in the live browser. The deployed app uses its built-in demo tutor because no model API key is configured.

## Automated checks

| Check | Result |
|---|---|
| `.\.venv\Scripts\python.exe -m pytest` (release commit) | Passed: 14 tests |
| `.\.venv\Scripts\python.exe -m ruff check .` | Passed: no lint issues |
| `.\.venv\Scripts\python.exe -m compileall -q app.py backend tests` | Passed |
| GitHub Actions CI for the release commit | Passed: [workflow run 2](https://github.com/iteshwalia/ai-tutor-projectmanagement/actions/runs/45027726219) |

The automated tests cover page and health endpoints, frontend module serving, demo chat responses, input validation, question generation and evaluation, progress updates and reset, profile validation and persistence, model-request forwarding with a mocked provider, HTTPS endpoint restrictions, secret-safe status output, production configuration, session-cookie contents, and security headers.

## Follow-up source validation

The current working source adds Gemini configuration, expands the question and demo-knowledge base, and changes the default learner name to Itesh. Local verification passed **19 tests**, Ruff, Python compilation, and `git diff --check`. Tests cover Gemini request defaults and secret-safe status, expanded CPMAI content, and migration of the legacy placeholder profile. The Gemini request is mocked; no real API key has been used. These changes still require a Render deployment before the live checks below apply to them.

## Live deployment checks

- Render built the Docker image and reported the service live for the release commit.
- `GET /healthz` returned `{"status":"ok"}`.
- The deployed homepage loaded in the browser.
- After four sequential chat exchanges, waiting for each reply to finish, the chat container measured 240 px high with 1,166 px of message content. Its scroll position was 925.6 px of a 926 px maximum (0.4 px from the bottom), confirming it remained scrollable and followed the latest reply.

## Limitations and follow-up

- The real external-model request was **not** tested with a live credential. The current source supports Google Gemini with `GEMINI_API_KEY` and other OpenAI-compatible providers with `OPENAI_API_KEY`; automated provider forwarding uses mocked HTTP responses.
- Gemini's free tier has usage limits, and Google may use free-tier prompts to improve its products. Do not send sensitive, confidential, or personally identifying information; check Google's current [Gemini API terms](https://ai.google.dev/gemini-api/terms).
- The Render Free service can sleep while idle, and its local SQLite storage is ephemeral. Cold starts and loss of learner progress after restarts or redeploys are expected on this tier.
- The repository is deployed from a public-repository URL. New commits may require a manual Render deploy unless the repository is connected through Render's Git provider integration.
