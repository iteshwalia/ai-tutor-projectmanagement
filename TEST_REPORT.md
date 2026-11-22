# PM Mentor Test Report

**Test date:** 22 November 2026  
**Release commit:** `7ef2f07419cb69acb9a8415fb4d2b0ba6df28884`  
**Deployment:** [https://pm-mentor.onrender.com](https://pm-mentor.onrender.com/)

## Result

**Pass, with an AI-provider limitation.** The automated suite, lint, and Python compilation passed. The scrolling fix was deployed and verified in the live browser. The app currently uses its built-in demo tutor because no model API key is configured.

## Automated checks

| Check | Result |
|---|---|
| `.\.venv\Scripts\python.exe -m pytest` | Passed: 14 tests |
| `.\.venv\Scripts\python.exe -m ruff check .` | Passed: no lint issues |
| `.\.venv\Scripts\python.exe -m compileall -q app.py backend tests` | Passed |
| GitHub Actions CI for the release commit | Passed: [workflow run 2](https://github.com/iteshwalia/ai-tutor-projectmanagement/actions/runs/45027726219) |

The automated tests cover page and health endpoints, frontend module serving, demo chat responses, input validation, question generation and evaluation, progress updates and reset, profile validation and persistence, model-request forwarding with a mocked provider, HTTPS endpoint restrictions, secret-safe status output, production configuration, session-cookie contents, and security headers.

## Live deployment checks

- Render built the Docker image and reported the service live for the release commit.
- `GET /healthz` returned `{"status":"ok"}`.
- The deployed homepage loaded in the browser.
- After four sequential chat exchanges, waiting for each reply to finish, the chat container measured 240 px high with 1,166 px of message content. Its scroll position was 925.6 px of a 926 px maximum (0.4 px from the bottom), confirming it remained scrollable and followed the latest reply.

## Limitations and follow-up

- The real external-model request was **not** tested with a live credential. Automated provider forwarding is tested using a mocked HTTP response; production currently reports `Demo knowledge`.
- GitHub Models was retired on 30 July 2026, so a `GITHUB_TOKEN` for that service cannot enable model responses. See [GitHub's notice](https://docs.github.com/en/github-models). The available OpenAI-compatible integration needs an `OPENAI_API_KEY` added as a secret in Render; do not commit or share the key.
- The Render Free service can sleep while idle, and its local SQLite storage is ephemeral. Cold starts and loss of learner progress after restarts or redeploys are expected on this tier.
- The repository is deployed from a public-repository URL. New commits may require a manual Render deploy unless the repository is connected through Render's Git provider integration.
