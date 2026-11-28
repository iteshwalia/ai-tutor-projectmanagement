# PM Mentor Development Log

This log records the distinct requests, implementation decisions, checks, and deployment follow-ups made while building PM Mentor. Repeated requests are grouped into the step they affected. Prompt descriptions are summarized from the project brief and follow-up instructions; they are not a verbatim transcript. No API credentials are recorded here.

A detailed, reader-friendly Word edition that preserves this timeline and includes representative prompt examples is available in [DEVELOPMENT_LOG_DETAILED.docx](DEVELOPMENT_LOG_DETAILED.docx). The earlier concise edition remains in [DEVELOPMENT_LOG.docx](DEVELOPMENT_LOG.docx).

## Representative prompts used during development

These are prompt examples documented in DEVELOPMENT.md. They capture the direction of the work; they are not a verbatim transcript of every user message.

- **Product and interface:** “Build a project-management tutor for working professionals, with a polished chat interface, topic navigation, learner profile, and clear study actions.”
- **Personalization:** “Let the learner enter a name, current level, focus topic, and preferred difficulty, and use that information in the welcome message and learning experience.”
- **Teaching style:** “Explain concepts simply, use workplace examples, give hints before answers, encourage retrying, adapt difficulty, and redirect unrelated questions to project management.”
- **Practice and assessment:** “Generate project-management questions dynamically. Ask a question, accept the learner's answer, mark it correct or incorrect, explain the result, and provide encouragement.”
- **Progress:** “Track attempts, correct answers, strong areas, weak areas, and the most useful next lesson.”
- **Technical delivery:** “Turn the interface into a proper Python application, add a Flask backend, use server-side API credentials, and provide deployment instructions.”

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
- Added feedback personalized to learner profile and topic accuracy, with an actionable best practice for each project-management topic after every answer.
- Added learner-specific topic, difficulty, and welcome-message behavior.
- Kept answer keys on the server rather than exposing them in question responses.

**Implementation note:** When an AI provider is configured, every question request asks the model to generate a fresh question matched to the learner's topic and difficulty. Without a provider key, the app selects from the authored question bank.

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
- Fixed the profile editor's missing `openModal` import, which the live browser reported as a `ReferenceError` and which prevented the difficulty control from opening.
- Restored focus to the button that opened a modal when it closes, avoiding focus remaining inside an `aria-hidden` profile dialog.
- Added a per-topic breakdown to the summary and a downloadable report with learner settings, attempts, accuracy, strengths, practice needs, and a next-lesson recommendation.

**Verification:** 22 automated tests passed; Ruff, Python compilation, and SVG XML validation passed. The live profile editor was tested by selecting Advanced and then restoring the original Intermediate setting.

### 13. Make profile-save feedback visible

**Issue reported:** The learner-profile dialog appeared not to close after changing difficulty and pressing Save.

**Investigation and work:**

- Reproduced a successful live save: the profile endpoint returned HTTP 200, the selected difficulty was applied, and the dialog closed.
- Found that a failed save left the dialog open but put its error message in the chat behind the dialog, making the failure easy to miss.
- Added a disabled “Saving…” button state while the profile request is in flight.
- Added an accessible in-dialog error message so a failed save is visible and the learner can retry without losing the form.

**Verification:** All 22 automated tests passed. A live browser save changed the difficulty and closed the dialog; the original preference was restored afterward. Failure-state feedback is covered by the updated dialog UI.

### 14. Add browser regression tests and a report

**Request:** Write Playwright tests and create a regression report for the major UI functionality.

**Work:**

- Added Python Playwright UI tests that launch the Flask app locally with temporary SQLite storage and force the built-in demo tutor, avoiding production data and model credentials.
- Covered initial UI and settings dialogs, profile save failure/retry/persistence, all four difficulty-aware mode prompts, chat input, quiz and practice answer feedback, progress metrics, report download, and session reset.
- Added Chromium installation to GitHub Actions and documented local setup and test commands.
- Created Markdown and PDF versions of the [regression test report](REGRESSION_TEST_REPORT.md) and the [full test report](TEST_REPORT.md), including test results and environment limitations.

**Verification:** The combined API and browser suite passed all 26 tests; Ruff and whitespace checks passed. The UI tests ran in Chromium against the temporary local application.

### 15. Export the reports as Word documents

**Request:** Provide the full and regression test reports in an editable document format.

**Work:** Generated [TEST_REPORT.docx](TEST_REPORT.docx) and [REGRESSION_TEST_REPORT.docx](REGRESSION_TEST_REPORT.docx) from the current Markdown reports, preserving headings, tables, lists, and report links. Added the Word versions to the README and report indexes.

**Verification:** Both DOCX files reopened successfully and their key test results and coverage sections were verified.

### 16. Document the user experience rationale and process

**Request:** Create a report covering user-experience thinking and the steps followed during development.

**Work:** Created Markdown, PDF, and Word versions of the [user experience and development process report](USER_EXPERIENCE_REPORT.md). It describes the intended learner, design goals, end-to-end journey, development sequence, validation evidence, constraints, and suggested next usability checks. The report distinguishes design rationale from formal user research, which has not been documented.

### 17. Generate fresh questions for practice and quiz

**Request:** Use the connected AI model to give learners new questions on every Practice and Quiz attempt.

**Work:**

- Connected each `/api/question` request to the configured Gemini or OpenAI-compatible provider.
- Prompted the model to create an original question matching the learner's saved topic and difficulty.
- Validated the returned question structure and kept answer keys on the server.
- Preserved the authored, topic- and difficulty-matched question bank when no model key is configured; provider failures are reported instead of silently switching sources.

**Verification:** Added tests confirming a separate model request on each question request, question validation, server-side answer handling, and explicit errors for invalid model output.

### 18. Personalize feedback and show topic best practices

**Request:** Add personalized feedback and Tips and Best Practices to Practice and Quiz.

**Work:**

- Added feedback that uses the learner's name, difficulty, topic, and topic-level accuracy to suggest a next reasoning step.
- Added practical best-practice guidance for each project-management topic after both correct and incorrect answers.
- Displayed the feedback and best practice in the shared answer-evaluation flow for Practice and Quiz.

**Verification:** Added API and browser assertions for personalized feedback, topic accuracy, best-practice guidance, and both answer outcomes.

### 19. Accept selected option letters

**Issue reported:** Correct multiple-choice answers were marked incorrect when the learner submitted only the option letter.

**Resolution and work:**

- Updated answer evaluation to map A–D to the corresponding displayed choices, case-insensitively and with an optional trailing period.
- Kept incorrect option letters incorrect and retained text-answer aliases.
- Updated the browser regression flow to submit a lowercase option letter with a period.

**Verification:** The full suite passed 30 tests: 26 API tests and four Playwright browser tests. Ruff and `git diff --check` passed.

### 20. Refresh reports and publish the update

**Work:**

- Regenerated the test, regression, user-experience, and visual reports as Markdown and Word documents; removed the previous PDF report files so only the requested formats remain.
- Committed the code, tests, and reports as `c8b152a` and pushed the commit to `main`.
- Confirmed GitHub Actions CI passed for the commit and the Render `/healthz` endpoint returned HTTP 200. The service is configured to auto-deploy on push.

**Deployment evidence limit:** The Render health endpoint does not expose a build SHA, so the exact commit serving the live site could not be independently confirmed.

### 21. Harden AI-generated question parsing

**Issue reported:** On the live application, Practice and Quiz returned an “AI provider returned an invalid question” error instead of showing a question.

**Work:**

- Tightened the generation prompt to request one plain JSON object without surrounding commentary.
- Made parsing tolerant of JSON wrapped in Markdown fences or short explanatory text.
- Normalized common model response variants, including letter-labeled choices, choice objects/maps, answer labels such as “B.”, and common aliases for prompt, answer, hint, and explanation fields.
- Kept final validation strict: the question still needs four distinct choices and an answer that maps to one of them.
- Logged the validation reason without logging the model response content.

**Verification:** Added regression coverage for fenced JSON, surrounding prose, labeled choices, a letter-labeled correct answer, and alternate field names. The full local suite passed 31 tests, Ruff passed, and `git diff --check` passed. A live model response was not available locally to reproduce byte-for-byte.

## Current state and known limits

- The live service reports Google Gemini when `GEMINI_API_KEY` is attached to the Render service through its environment configuration.
- The default no-key behavior remains the built-in demo tutor. The live OpenAI-compatible alternative has not been tested with a real credential.
- With a model key configured, each Practice or Quiz question request asks the model for a fresh topic- and difficulty-matched question. Without a key, the authored question bank remains available.
- Feedback is personalized to learner profile and topic accuracy; best practices are shown for every question topic. Multiple-choice letters A–D are accepted, including lowercase letters and an optional period.
- The latest local automated run passed 31 tests (27 API and four browser tests); Ruff and `git diff --check` passed.
- Render Free may sleep while idle and its local SQLite filesystem is ephemeral.
- Gemini free-tier use has limits and may use prompts to improve provider products. Do not send sensitive or confidential information.
- Current test, regression, user-experience, and visual reports are maintained as Markdown and Word documents; the previous PDF reports were removed.
