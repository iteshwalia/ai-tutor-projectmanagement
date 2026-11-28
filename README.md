# PM Mentor

PM Mentor is a focused project-management tutor for working professionals. It combines an HTML/CSS/JavaScript frontend with a Python Flask backend, session-based learner progress, practice questions, and optional model-generated tutoring.

## Features

- Learn, Practice, Quiz, and Challenge modes
- Learner profile, topic, and difficulty selection
- Project-management examples and answer feedback
- Personalized feedback that adapts to learner progress and topic-specific best practices after each answer
- Session progress, strengths, weaknesses, and next-lesson suggestions
- Fresh AI-generated practice and quiz questions when a model is configured, with a matching demo question bank when no key is available
- A downloadable progress report
- Demo responses without an AI credential
- Optional Google Gemini free-tier or other OpenAI-compatible model integration
- Docker deployment and GitHub Actions checks

## Development setup

Requires Python 3.12 or newer.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe app.py
```

Open http://127.0.0.1:5000. In VS Code, use **Run and Debug → PM Mentor (development)** or run the **Install development dependencies**, **Run tests**, and **Lint Python** tasks.

### Browser regression tests

The Playwright suite launches a temporary local Flask app with isolated SQLite storage and the built-in demo tutor. Install Chromium once, then run all API and browser tests:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest
```

The browser checks cover profile editing and save errors, all learning-mode prompts, chat, practice and quiz feedback, progress reporting and download, reset, and settings dialogs. See the [regression test report](REGRESSION_TEST_REPORT.md) for coverage and the latest run.

### macOS/Linux

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
python app.py
```

## Frontend and backend

| Component | Responsibility |
|---|---|
| `templates/index.html` | Accessible tutor UI and profile/settings dialogs |
| `static/styles.css` | Responsive visual design |
| `static/js/` | ES modules separated into API client, chat, modes, profile, progress reports, state, and DOM helpers |
| `app.py` | Local development entry point |
| `pm_mentor/application.py` | App factory, configuration, security headers, and blueprint registration |
| `pm_mentor/routes/` | Separate page, health, learner, and tutor HTTP endpoints |
| `pm_mentor/services/tutor.py` | AI provider selection, safe model calls, and demo response generation |
| `pm_mentor/learner_repository.py` | SQLite connection lifecycle and learner-state persistence |
| `pm_mentor/learning_content.py` | Project-management topics, quiz content, and demo knowledge |
| Flask session cookie | Contains only an opaque signed learner ID; protected with `HttpOnly`, `SameSite=Lax`, and `Secure` in production |
| SQLite store | Stores learner profile, active question, and progress on the server in `instance/pm_mentor.sqlite3` |
| AI provider | Optional model completion service contacted only by the backend |

## Architecture and sequence diagrams

- [System architecture](architecture.md#system-architecture)
- [Practice question and evaluation sequence](architecture.md#practice-question-and-answer-evaluation)
- [Tutor chat sequence](architecture.md#tutor-chat-with-optional-model-provider)
- Standalone [architecture SVG](architecture.svg) for a browser or diagram-capable editor.

```text
app.py                       Local development entry point
pm_mentor/
  application.py             Flask app factory and configuration
  learning_content.py        Topics, practice questions, demo knowledge
  learner_repository.py      SQLite setup and learner-state repository
  routes/                    Page, health, learner, and tutor blueprints
  services/tutor.py          Demo and external model response service
  serve.py                   Waitress production entry point
static/js/
  app.js                     Frontend entry point and event wiring
  api.js                     Flask API client
  chat.js                    Chat and answer flow
  modes.js                   Learn/Practice/Quiz/Challenge controls
  profile.js                 Learner profile and model status
  progress.js                Progress summary, report view, and reset
  dom.js                     Shared rendering and dialog helpers
  state.js                   Browser state
```

Important endpoints: `GET /healthz`, `GET /api/status`, `POST /api/chat`, `GET/POST /api/profile`, `GET /api/question`, `POST /api/evaluate`, `GET /api/progress`, `GET /api/progress/report`, and `POST /api/reset`.

## Model responses and API credentials

The backend supports Google Gemini and OpenAI-compatible chat-completions APIs. It prefers `GEMINI_API_KEY` when both provider keys are set. Keys are read only by the backend and are never sent to or stored in the browser.

| Environment variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio key; uses the OpenAI-compatible Gemini endpoint |
| `GEMINI_MODEL` | Optional Gemini model; defaults to `gemini-3.5-flash-lite` |
| `GEMINI_API_URL` | Optional Gemini chat-completions endpoint override |
| `OPENAI_API_KEY` | Key for OpenAI or another OpenAI-compatible service |
| `OPENAI_API_URL` | Optional endpoint override for the OpenAI-compatible provider |
| `OPENAI_MODEL` | Optional model ID; defaults to `gpt-4o-mini` |
| `FLASK_SECRET_KEY` | Required signing key for production Flask sessions |
| `FLASK_ENV` | Set to `production` to enable secure-cookie production behavior |

With a model key configured, each `/api/question` request asks the model for a fresh question matching the learner's topic and difficulty. Without a key, questions come from the built-in topic- and difficulty-matched bank, and `/api/chat` replies from demo knowledge. The `/api/status` endpoint and Settings panel show the chat response source, without revealing the key.

Non-local model endpoints must use HTTPS. HTTP is allowed only for loopback development endpoints.

To enable Gemini, create a key in [Google AI Studio](https://aistudio.google.com/api-keys), then set `GEMINI_API_KEY` in the server environment. Gemini's free tier has usage limits, and Google may use free-tier prompts to improve its products. Do not submit confidential, sensitive, or personally identifying information; check Google's current [Gemini API terms](https://ai.google.dev/gemini-api/terms) before use. For local development, copy `.env.example` to `.env`; `python-dotenv` loads it automatically, and `.env` is ignored by Git. Never paste a real key into source code, screenshots, or issue reports.

## Production deployment

Do not use Flask's development server in production. The included Docker image runs Waitress as a non-root user.

### Deploy publicly on Render

The included [render.yaml](render.yaml) Blueprint configures a Free web service, HTTPS, a generated Flask session secret, and a `/healthz` health check. Render Free services can sleep when idle and their local filesystem is ephemeral. The service remains hosted independently of your laptop, but allow for a cold start and do not rely on SQLite progress surviving restarts or redeploys. Choose a paid persistent disk or managed database if progress must be durable.

1. Push this project to a GitHub repository (see [Prepare a Git repository](#prepare-a-git-repository)).
2. Sign in at [Render](https://render.com), select **New → Blueprint**, and connect the GitHub repository.
3. Review the `pm-mentor` Free service details, then apply the Blueprint.
4. Wait for the deploy and health check to pass. Render assigns a public `https://...onrender.com` address; open it while your laptop is off to confirm it is hosted independently. The first request after idle may take time while the service wakes.
5. To enable model-generated replies, add `GEMINI_API_KEY` under the service's **Environment** settings. Alternatively, add `OPENAI_API_KEY` for an OpenAI-compatible provider. Set the corresponding model or endpoint variables only if you need to override the defaults, then redeploy.

The service works without a model key using demo responses. Do not put credentials in the Blueprint or commit them to Git; set them in Render's secret environment-variable settings.

1. Generate a unique session key:

   ```powershell
   py -c "import secrets; print(secrets.token_hex(32))"
   ```

2. Set `FLASK_SECRET_KEY`, `GEMINI_API_KEY` (or `OPENAI_API_KEY`), and any model options in your hosting provider's secret manager.
3. Build and run the image behind a TLS-terminating reverse proxy:

   ```powershell
   docker build -t pm-mentor .
   docker run --rm -p 5000:5000 `
     -v pm-mentor-data:/app/instance `
     -e FLASK_SECRET_KEY=$env:FLASK_SECRET_KEY `
     -e GEMINI_API_KEY=$env:GEMINI_API_KEY `
     pm-mentor
   ```

The app requires a random `FLASK_SECRET_KEY` of at least 32 characters and enables secure session cookies and HSTS when `FLASK_ENV=production`. Use HTTPS, keep the secret key stable, mount durable storage for `/app/instance`, set resource limits and health checks in the hosting platform, and rotate model credentials according to provider guidance. SQLite is appropriate for a single-instance deployment; use a managed database and authenticated user accounts before scaling across multiple app instances or storing sensitive learner data.

## Test and lint

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
```

GitHub Actions runs both commands on pushes and pull requests.

## Prepare a Git repository

Git should be installed and available on `PATH`. From this folder:

```powershell
git init
git add .
git status
git commit -m "Initial PM Mentor application"
```

Review `git status` before committing. `.gitignore` excludes local environments, caches, and `.env` secrets.

## Project documentation

- [Development story, prompts, iterations, and test history](DEVELOPMENT.md)
- [Detailed development log with prompt examples (Word)](DEVELOPMENT_LOG_DETAILED.docx)
- [Earlier concise development log (Word)](DEVELOPMENT_LOG.docx)
- [User experience and development process report](USER_EXPERIENCE_REPORT.md)
- [User experience report (PDF)](USER_EXPERIENCE_REPORT.pdf)
- [User experience report (Word)](USER_EXPERIENCE_REPORT.docx)
- [Latest test report and deployment verification](TEST_REPORT.md)
- [Full test report (PDF)](TEST_REPORT.pdf)
- [Full test report (Word)](TEST_REPORT.docx)
- [Playwright UI regression test report](REGRESSION_TEST_REPORT.md)
- [Playwright UI regression report (PDF)](REGRESSION_TEST_REPORT.pdf)
- [Playwright UI regression report (Word)](REGRESSION_TEST_REPORT.docx)
- [Visual test report (PDF)](VISUAL_TEST_REPORT.pdf)
- [Architecture diagram and component responsibilities](architecture.md)
- [Architecture SVG](architecture.svg)
