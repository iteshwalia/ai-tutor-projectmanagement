# PM Mentor Development Log

This log records the distinct requests, implementation decisions, checks, and deployment follow-ups made while building PM Mentor. Repeated requests are grouped into the step they affected. Prompt descriptions are summarized from the project brief and follow-up instructions; they are not a verbatim transcript. No API credentials are recorded here.

## Development timeline

### 1. Define the learning problem and audience

**Request:** Build a personalized AI tutor focused on Project Management for working professionals, rather than a general-purpose chatbot.

**Decisions and work:**

- Focus the learning area on project planning, Agile, stakeholders, risk, leadership, and AI project management.
- Shape the teaching approach around accessible explanations, workplace examples, hints, practice, constructive feedback, and next-step recommendations.
- Plan four modes: Learn, Practice, Quiz, and Challenge.

**Result:** A clear product scope for both the interface and tutor behavior. The behavioral prompt examples are collected in [DEVELOPMENT.md](DEVELOPMENT.md).

### 2. Build the first learning interface

**Request:** Create a simple but complete tutor interface with a chat area, message input, suggested actions, learner profile, and progress summary.

**Work:**

- Built the initial HTML, CSS, and JavaScript learning workspace.
- Added profile fields for learner name, level, topic, and preferred difficulty.
- Added navigation for the learning modes and an initial progress summary.

**Result:** The project moved from a concept into a usable browser prototype. The initial repository commit is `5ec9d0e` (21 November 2026).

### 3. Add practice, feedback, and personalization

**Request:** Make practice interactive: show questions, accept answers, explain results, and use learner progress to suggest what to study next.

**Work:**

- Added project-management questions with choices, hints, accepted answers, and explanations.
- Added answer evaluation and progress tracking for attempted and correct questions, organized by topic.
- Added learner-specific topic, difficulty, and welcome-message behavior.
- Kept answer keys on the server rather than exposing them in question responses.

**Implementation note:** Practice questions are selected randomly from the authored question bank for the learner's topic. The Practice API does not currently ask Gemini to generate a new question for every request.

### 4. Turn the prototype into a Python web application

**Request:** Package the project as a proper HTML and Python application, make the frontend/backend boundary clear, and prepare it for Git and production.

**Work:**

- Added a Flask application factory, API routes, SQLite learner-state storage, and a production WSGI server.
- Once Python was installed locally, created the project virtual environment and installed the development dependencies.
- Split backend page, learner, health, and tutor endpoints into route modules.
- Split browser behavior into ES modules for API calls, chat, learning modes, profile, progress, state, and DOM helpers.
- Added Docker and VS Code development configuration, dependency manifests, GitHub Actions checks, and environment-variable examples.
- Added secure-cookie settings, request validation, security headers, production-secret validation, and server-side provider calls.

**Result:** The app gained an independently deployable backend while retaining the browser UI. The production-ready application work is recorded in commit `812de59` (22 November 2026).

### 5. Deploy the application and correct the chat scrolling issue

**Request:** Make the app accessible online while the learner's laptop is off, and fix the chat panel when conversation history grows.

**Work:**

- Configured the Render web service and verified its health endpoint.
- Adjusted the chat layout so the message panel can shrink and scroll within the application viewport.
- Manually deployed the scroll fix in commit `7ef2f07`.

**Verification:** After four sequential chat exchanges, the chat area was 240 px high with 1,166 px of message content. The scroll position reached 925.6 px of a 926 px maximum, confirming it could reach the latest message.

**Operational note:** Render Free can sleep when idle and uses ephemeral local storage. A cold start is possible, and SQLite learner progress is not guaranteed to survive service restarts or redeploys.

### 6. Document testing and provide a visual report

**Request:** Create a test report and a visual test report.

**Work:**

- Recorded the initial automated, browser, and deployment checks in [TEST_REPORT.md](TEST_REPORT.md).
- Created the two-page visual test report PDF.
- Added links to the reports from the project documentation.

**Verification:** The initial release suite had 14 passing tests, clean Ruff checks, and successful Python compilation. The report identifies which live checks were performed and which still required a real model credential.

**Commits:** `2f35036` (test report) and `26b1dfa` (visual report), 22 November 2026.

### 7. Expand learning content and add Gemini support

**Request:** Change the default learner name to Itesh, broaden the question-and-answer base, and identify an affordable model option.

**Decisions and work:**

- Added 12 original practice questions across planning, stakeholder management, Agile, risk, leadership, and AI project management, plus related built-in demo explanations.
- Changed the default profile to Itesh and added a one-time-on-read migration for existing seeded profiles named “Alex Morgan”; learner-selected names are preserved.
- Added Google Gemini through its OpenAI-compatible chat-completions endpoint. `GEMINI_API_KEY` takes precedence over `OPENAI_API_KEY`; the default model is `gemini-3.5-flash-lite`.
- Kept credentials server-side and removed the learner's name from the model prompt.
- Replaced the retired GitHub Models instructions with Gemini setup guidance and a free-tier privacy warning.

**Verification:** The suite passed 19 tests, Ruff, Python compilation, and `git diff --check`. Automated provider forwarding uses mocked responses. Commit `6b41578` contains these application changes.

### 8. Deploy the learner-name and Gemini changes

**Issue found:** The website initially still displayed Alex because Render was serving the older release; pushing to GitHub had not triggered a deployment.

**Work and verification:**

- Manually deployed commit `6b41578` to Render.
- Confirmed Render reported the deployment Live.
- Opened a fresh app page and verified the welcome screen and profile showed Itesh.
- Updated the test report with the new deployment evidence.

**Commits:** `64fcb0c` recorded deployment verification; the runtime application remains at commit `6b41578`.

### 9. Create architecture and interaction diagrams

**Request:** Create a proper architecture diagram and sequence diagram.

**Work:**

- Replaced the early, simplified diagram with a component-level architecture showing the browser, Render/Waitress/Flask layers, API services, SQLite, local learning content, and optional model providers.
- Added Mermaid sequence diagrams for practice/evaluation and tutor chat, including the Gemini, compatible-provider, and demo fallback paths.
- Linked the diagrams from the README and updated the SVG diagram.

**Verification:** The SVG parsed as valid XML, the Markdown contained the architecture diagram and both sequence diagrams, and `git diff --check` passed.

**Commit:** `86a218f` (22 November 2026).

### 10. Connect the Render Environment Group and verify live Gemini

**Issue found:** The app still reported Demo knowledge even though a Gemini key had been added to an Environment Group. The group's variable was not yet available to the running service.

**Resolution and verification:**

- Connected the Environment Group to the `pm-mentor` Render service.
- Confirmed a fresh `GET /api/status` response reported `api_configured: true`, `key_name: GEMINI_API_KEY`, provider `Google Gemini`, and model `gemini-3.5-flash-lite`.
- Sent one non-sensitive project-management question through the live chat UI and received a model-generated answer. The UI identified Google Gemini as the source.
- Added a test proving Gemini takes precedence if both Gemini and OpenAI-compatible keys are set.
- Recorded the live verification in [TEST_REPORT.md](TEST_REPORT.md).

**Commits:** `2cdece2` added the provider-precedence test; `45b6dbe` recorded the live Gemini check. No key value is included in source, reports, or this log.

### 11. Clarify the application structure and architecture diagram

**Request:** Restructure the application with more descriptive, developer-friendly file and folder names, and make the architecture diagram easier to understand.

**Work:**

- Renamed the generic `backend/` package to `pm_mentor/`.
- Renamed `content.py` and `database.py` to `learning_content.py` and `learner_repository.py`.
- Moved the Flask application factory to `pm_mentor/application.py`; kept the root `app.py` as a small local entry point and moved production startup to `pm_mentor/serve.py`.
- Updated Docker, tests, imports, and current file maps to use the new package paths.
- Reworked the architecture guide and SVG to explain the learner experience in plain language, while preserving the details of practice questions, progress storage, and optional Gemini integration.

**Verification:** All 19 automated tests passed; Ruff, Python compilation, `git diff --check`, and SVG XML validation passed.

### 12. Make difficulty selection adaptive and add a learner progress report

**Request:** Fix difficulty selection so it meaningfully changes the learning experience, and add a basic learner progress summary report.

**Work:**

- Added beginner, intermediate, and advanced question variants for every topic; practice and quiz requests now select a question matching both the saved topic and difficulty.
- Made Learn, Practice, Quiz, and Challenge prompts explicitly reflect the selected difficulty. The AI tutor prompt and built-in responses now give distinct guidance for each level.
- Displayed selected difficulty in the learner profile and on practice questions.
- Added a per-topic breakdown to the summary and a downloadable report with learner settings, attempts, accuracy, strengths, practice needs, and a next-lesson recommendation.

**Verification:** 22 automated tests passed; Ruff, Python compilation, and SVG XML validation passed.

## Current state and known limits

- The live service reports Google Gemini when `GEMINI_API_KEY` is attached to the Render service through its environment configuration.
- The default no-key behavior remains the built-in demo tutor. The live OpenAI-compatible alternative has not been tested with a real credential.
- Practice questions are authored and randomly selected by topic and difficulty; model-generated questions on demand remain a possible future improvement.
- Render Free may sleep while idle and its local SQLite filesystem is ephemeral.
- Gemini free-tier use has limits and may use prompts to improve provider products. Do not send sensitive or confidential information.
