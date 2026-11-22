# PM Mentor

PM Mentor is a focused project-management tutor for working professionals. It combines an HTML/CSS/JavaScript frontend with a Python Flask backend, session-based learner progress, practice questions, and optional model-generated tutoring.

## Features

- Learn, Practice, Quiz, and Challenge modes
- Learner profile, topic, and difficulty selection
- Project-management examples and answer feedback
- Session progress, strengths, weaknesses, and next-lesson suggestions
- Demo responses without an AI credential
- Optional OpenAI-compatible or GitHub Models integration
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

### macOS/Linux

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python app.py
```

## Frontend and backend

| Component | Responsibility |
|---|---|
| `templates/index.html` | Accessible tutor UI and profile/settings dialogs |
| `static/styles.css` | Responsive visual design |
| `static/js/` | ES modules separated into API client, chat, modes, profile, progress, state, and DOM helpers |
| `app.py` | App factory, configuration, security headers, and blueprint registration |
| `backend/routes/` | Separate page, health, learner, and tutor HTTP endpoints |
| `backend/services/tutor.py` | AI provider selection, safe model calls, and demo response generation |
| `backend/database.py` | SQLite connection lifecycle and learner-state persistence |
| `backend/content.py` | Project-management topics, quiz content, and demo knowledge |
| Flask session cookie | Contains only an opaque signed learner ID; protected with `HttpOnly`, `SameSite=Lax`, and `Secure` in production |
| SQLite store | Stores learner profile, active question, and progress on the server in `instance/pm_mentor.sqlite3` |
| AI provider | Optional model completion service contacted only by the backend |

```text
app.py                       Application factory and configuration
backend/
  content.py                 Topics, practice questions, demo knowledge
  database.py                SQLite setup and learner-state repository
  routes/                    Page, health, learner, and tutor blueprints
  services/tutor.py          Demo and external model response service
static/js/
  app.js                     Frontend entry point and event wiring
  api.js                     Flask API client
  chat.js                    Chat and answer flow
  modes.js                   Learn/Practice/Quiz/Challenge controls
  profile.js                 Learner profile and model status
  progress.js                Progress summary and reset
  dom.js                     Shared rendering and dialog helpers
  state.js                   Browser state
```

Important endpoints: `GET /healthz`, `GET /api/status`, `POST /api/chat`, `GET/POST /api/profile`, `GET /api/question`, `POST /api/evaluate`, `GET /api/progress`, and `POST /api/reset`.

## Model responses and API credentials

The backend checks `OPENAI_API_KEY` first. If it is absent, it checks `GITHUB_TOKEN`. These credentials are never sent to or stored in the browser.

| Environment variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | Bearer key for the OpenAI API or a compatible service |
| `GITHUB_TOKEN` | Bearer token for GitHub Models if `OPENAI_API_KEY` is not set |
| `OPENAI_API_URL` | Optional chat-completions endpoint override |
| `OPENAI_MODEL` | Optional model ID; defaults to `gpt-4o-mini` for OpenAI and `openai/gpt-4.1-mini` for GitHub Models |
| `FLASK_SECRET_KEY` | Required signing key for production Flask sessions |
| `FLASK_ENV` | Set to `production` to enable secure-cookie production behavior |

Without a model key, `/api/chat` replies from built-in demo knowledge; it does not call an AI model. The `/api/status` endpoint and Settings panel show which response source is active, without revealing the key.

Non-local model endpoints must use HTTPS. HTTP is allowed only for loopback development endpoints.

For local development, copy `.env.example` to `.env` and set your chosen provider key. `python-dotenv` loads it automatically, and `.env` is ignored by Git. Never paste a real token into source code, screenshots, or issue reports. GitHub Models access and available model identifiers depend on your account and the selected endpoint.

## Production deployment

Do not use Flask's development server in production. The included Docker image runs Waitress as a non-root user.

### Deploy publicly on Render

The included [render.yaml](render.yaml) Blueprint configures a Free web service, HTTPS, a generated Flask session secret, and a `/healthz` health check. Render Free services can sleep when idle and their local filesystem is ephemeral. The service remains hosted independently of your laptop, but allow for a cold start and do not rely on SQLite progress surviving restarts or redeploys. Choose a paid persistent disk or managed database if progress must be durable.

1. Push this project to a GitHub repository (see [Prepare a Git repository](#prepare-a-git-repository)).
2. Sign in at [Render](https://render.com), select **New → Blueprint**, and connect the GitHub repository.
3. Review the `pm-mentor` Free service details, then apply the Blueprint.
4. Wait for the deploy and health check to pass. Render assigns a public `https://...onrender.com` address; open it while your laptop is off to confirm it is hosted independently. The first request after idle may take time while the service wakes.
5. To enable model-generated replies, add `OPENAI_API_KEY` or `GITHUB_TOKEN` under the service's **Environment** settings. Optionally add `OPENAI_MODEL` and `OPENAI_API_URL`, then redeploy.

The service works without a model key using demo responses. Do not put credentials in the Blueprint or commit them to Git; set them in Render's secret environment-variable settings.

1. Generate a unique session key:

   ```powershell
   py -c "import secrets; print(secrets.token_hex(32))"
   ```

2. Set `FLASK_SECRET_KEY`, `OPENAI_API_KEY` or `GITHUB_TOKEN`, and any model options in your hosting provider's secret manager.
3. Build and run the image behind a TLS-terminating reverse proxy:

   ```powershell
   docker build -t pm-mentor .
   docker run --rm -p 5000:5000 `
     -v pm-mentor-data:/app/instance `
     -e FLASK_SECRET_KEY=$env:FLASK_SECRET_KEY `
     -e OPENAI_API_KEY=$env:OPENAI_API_KEY `
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
- [Latest test report and deployment verification](TEST_REPORT.md)
- [Visual test report (PDF)](VISUAL_TEST_REPORT.pdf)
- [Architecture diagram and component responsibilities](architecture.md)
- [Architecture SVG](architecture.svg)
