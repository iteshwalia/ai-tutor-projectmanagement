# Development Story of PM Mentor

## 1. What we set out to build

PM Mentor was created to help working professionals learn project management in a practical, interactive way. Instead of building a general chatbot, we narrowed the focus to concepts that professionals encounter in real projects, including planning, Agile delivery, stakeholders, risk, leadership, PERT scheduling, and CPMAI.

The aim was simple: a learner should be able to choose a topic, receive an explanation suited to their level, answer a question, see useful feedback, and understand what to practice next.

For the chronological record of requests, implementation choices, tests, releases, and follow-up fixes, see the [Development Log](DEVELOPMENT_LOG.md).

## 2. Prompts used during development

Development began with the project brief, which described the audience, tutor behavior, learning modes, personalization, question generation, progress tracking, and deployment needs. We translated that brief into a series of practical prompts.

### Initial interface prompt

> “Build a project-management tutor for working professionals, with a polished chat interface, topic navigation, learner profile, and clear study actions.”

This became the first visual prototype. It established the learning workspace, sidebar, chat area, profile card, and four learning modes.

### Personalization prompt

> “Let the learner enter a name, current level, focus topic, and preferred difficulty, and use that information in the welcome message and learning experience.”

This helped us make the app feel specific to the learner rather than presenting the same generic advice to everyone.

### Teaching behavior prompt

> “Explain concepts simply, use workplace examples, give hints before answers, encourage retrying, adapt difficulty, and redirect unrelated questions to project management.”

We used this as the teaching philosophy for both the demo responses and the optional AI provider.

### Practice and assessment prompt

> “Generate project-management questions dynamically. Ask a question, accept the learner's answer, mark it correct or incorrect, explain the result, and provide encouragement.”

This prompted the PERT, stakeholder, Agile, risk, and CPMAI question flow.

### Progress prompt

> “Track attempts, correct answers, strong areas, weak areas, and the most useful next lesson.”

This led to the performance summary and the weekly goal display.

### Technical packaging prompt

> “Turn the interface into a proper Python application, add a Flask backend, use server-side API credentials, and provide deployment instructions.”

The answer to this prompt was the final Flask structure, JSON APIs, Dockerfile, and architecture diagrams.

## 3. Development iterations

### Iteration 1: Creating the first working prototype

We started with HTML, CSS, and JavaScript. The first version focused on the visual experience: a professional sidebar, conversation panel, learner profile, suggested prompts, and progress summary.

At this stage, all interactions were handled in the browser. The application was usable, but it had no Python backend or persistent server-side session behavior.

### Iteration 2: Adding personalization

We added profile controls for:

- Learner name
- Current level
- Preferred difficulty
- Study topic

The profile modal also became the place to select a different topic. The interface began updating names, avatars, topics, and welcome text from the learner's choices.

### Iteration 3: Improving the learning modes

Learn mode was initially a free chat. Practice, Quiz, and Challenge modes were then connected to question prompts. This made the modes behave differently in the interface and gave learners a clear way to move between explanation and assessment.

We also added:

- Multiple-choice project-management questions
- A hint before revealing a difficult answer
- Explicit correct and incorrect feedback
- Short explanations after evaluation
- Encouraging retry language

Practice questions are selected randomly from the authored, topic-matched question bank. The current Practice API does not ask Gemini to invent a new question on each request.

### Iteration 4: Adding progress and recommendations

We introduced session progress metrics, including attempted questions and correct answers. Results began updating topic areas so the summary could identify both strengths and weak areas.

The summary modal was enhanced to show:

- Total attempted questions
- Correct answers
- Accuracy percentage
- Strong areas
- Areas needing practice
- A recommended next lesson

### Iteration 5: Moving to a Flask application

The static files were reorganized into:

```text
app.py
templates/index.html
static/app.js
static/styles.css
requirements.txt
Dockerfile
```

The HTML, JavaScript, and CSS remained the user-facing application, while Flask became the server responsible for routes, sessions, and optional AI calls.

### Iteration 6: Securing AI integration

The original browser-side settings modal was changed so it no longer collected API keys. The first server-side provider configuration used:

- `OPENAI_API_KEY`
- `OPENAI_API_URL`
- `OPENAI_MODEL`

This was an important improvement because credentials should not be embedded in browser code or shared with other users. When no provider was configured, the app continued to work using a built-in demo knowledge layer. The later Gemini addition is documented in Iteration 10.

### Iteration 7: Deployment and documentation

The project now includes:

- Flask local-server instructions
- Docker build and run instructions
- Mermaid system architecture and interaction-sequence documentation
- A downloadable-style SVG architecture diagram
- This development story

### Iteration 8: Preparing the repository for development and deployment

After moving the project into its dedicated VS Code workspace, we added:

- A standard `.vscode` setup with a launch profile, tasks, and extension recommendations
- `.gitignore`, `.gitattributes`, `.dockerignore`, and a GitHub Actions workflow
- A pinned production requirements file and a separate developer-tools file
- A `.env.example` template that contains no real credentials
- Waitress as the production WSGI server and a non-root Docker user
- A required production secret key, secure cookies, security headers, and request-size limits
- SQLite-backed learner state; the browser cookie now carries only an opaque signed session ID
- API answer-key privacy and exact answer matching
- Automated tests for API behavior, session isolation, model forwarding, and production configuration

We also removed duplicate, unused browser-side tutor logic so the Flask backend is the source of truth for questions, answers, and progress.

### Iteration 9: Separating frontend and backend responsibilities

The final refactor replaced the single browser script and crowded Flask module with small, named components:

- The frontend entry point now loads ES modules from `static/js/`.
- `api.js` owns HTTP requests; `chat.js`, `modes.js`, `profile.js`, and `progress.js` own their UI behavior.
- `app.py` is the small local entry point; `pm_mentor/application.py` builds the Flask app and registers routes.
- `pm_mentor/routes/` contains separate page, health, learner, and tutor endpoints.
- `pm_mentor/services/tutor.py` owns model-provider calls and the demo response path.
- `pm_mentor/learner_repository.py` owns SQLite connections and learner state.
- `pm_mentor/learning_content.py` holds quiz and demo learning content.

This makes it easier to find a feature, test it in isolation, and add new behavior without growing a single application file indefinitely.

### Iteration 10: Expanding practice content and enabling a free-tier model option

We broadened the built-in practice bank with original PMP-style items covering WBS, critical-path delays, cost performance, stakeholder engagement, Scrum events, risk responses, servant leadership, and AI data readiness. The demo tutor also gained concise explanations for these concepts, so the app remains useful without a model credential.

The previous GitHub Models instructions were replaced with a first-class Google Gemini option. The backend now uses `GEMINI_API_KEY` and the Gemini OpenAI-compatible endpoint by default, while preserving support for other OpenAI-compatible providers. The settings and setup docs warn that Gemini free-tier use is limited and prompts may be used to improve Google's products. The learner's name is no longer included in the model system prompt.

The default learner is now Itesh. Existing records that still contain the original seeded placeholder name are updated when that learner profile is next loaded; learner-chosen names are unchanged.

### Iteration 11: Giving the codebase a domain-first layout

The generic `backend/` package was renamed to `pm_mentor/`, so the import path now names the product rather than only its technical layer. Generic module names were clarified as `learning_content.py` and `learner_repository.py`. The Flask factory moved to `pm_mentor/application.py`, while the root `app.py` remains a small, familiar development entry point. Production starts through `pm_mentor/serve.py`.

The architecture diagram was also rewritten in plain language around the learner's journey, while keeping the route and storage details in the architecture guide.

### Iteration 12: Making difficulty adaptive and adding a progress report

The selected difficulty now determines which authored question is returned for the learner's topic. The question bank includes beginner, intermediate, and advanced coverage for every topic. Each learning mode also sends difficulty-specific instructions, the model prompt differentiates explanation depth and hints, and the built-in tutor varies its guidance when no model key is configured. The learner profile and practice question both display the selected level.

The progress summary now includes a per-topic breakdown and a downloadable text report with learner settings, attempts, accuracy, strong areas, needs-practice topics, and a recommended next lesson.

## 4. Testing performed

We tested the application at both browser-facing and API levels.

### Concept and chat tests

| Input or action | Expected result | Outcome |
|---|---|---|
| Open the home page | The interface should load with navigation and chat | Passed |
| "Hello" | A friendly project-management response should appear | Basic chat response path |
| "Explain the critical path" | A clear explanation and workplace example | Passed |
| "What is Scrum?" | A simple Agile explanation | Demo fallback path |
| "Give me a practice question" | A question from the selected topic should appear | Passed |
| "What is today's weather?" | The tutor should redirect briefly to project management | Model prompt directs this; demo response remains on topic |

### Answer evaluation tests

We tested the PERT question:

> “A task has an optimistic estimate of 3 days, a most likely estimate of 5 days, and a pessimistic estimate of 13 days. What is the PERT expected duration?”

An answer of **“6 days”** was evaluated as correct. The server returned the correct answer, a PERT formula explanation, and updated progress of one attempt and one correct result.

An incorrect answer should receive:

- A constructive “not quite” message
- A hint
- The correct answer
- A short explanation
- Encouragement to continue

### Automated and API verification

The automated suite (`py -m pytest -q`) covers:

- Home and health endpoints
- Difficulty-matched practice questions for every topic and level
- Learner progress report metrics, topic breakdown, and download headers
- Demo response and configured model request forwarding
- Input validation for chat, profile, and answer endpoints
- Correct and incorrect question evaluation, including rejecting substring matches
- Session progress update and reset
- Question-answer privacy and opaque cookie contents
- Secure-cookie and security-header behavior
- Production secret-key validation

The original prototype was also smoke-tested through the browser-facing home page and chat, question, progress, and evaluation endpoints. On 22 November 2026, the deployed Gemini status and one generic model-generated chat response were verified in the browser. A live call to an alternative OpenAI-compatible provider has not been tested.

The earlier release-candidate checks completed with **14 passing tests**, clean Ruff checks, and successful Python compilation. The follow-up source changes passed **19 tests**, Ruff, Python compilation, and `git diff --check`. Automated Gemini request tests use a mocked provider response; the separate live browser check confirmed a real Gemini reply. A Waitress production-mode smoke test returned HTTP 200 from `/healthz` and verified secure session-cookie and HSTS headers. Docker image building was not performed because Docker is not installed in the environment.

## 5. System prompt used for the AI tutor

The following prompt defines the intended AI behavior:

```text
You are PM Mentor, a tutor for working professionals studying project management.
Adapt your explanation to the learner's current level and difficulty preference.

Explain concepts in simple, practical language and use workplace examples.
Give hints before revealing an answer during practice.
Ask the learner a focused question after explaining a concept.
Evaluate answers constructively and explain why an answer is correct or incorrect.
If the answer is wrong, provide a hint, the correct answer, an explanation, and encouragement.
Adapt follow-up questions to the learner's performance.
Generate original PMP- or PMI-ACP-style questions rather than repeating a fixed question bank.
For unrelated questions, briefly redirect the learner to project management.
End with a useful next step or learning recommendation.
```

This is the teaching specification used during design, not a verbatim copy of the compact prompt sent on every chat request. The runtime prompt is assembled in `pm_mentor/services/tutor.py` and includes the learner's topic and difficulty. Practice questions are served by the authored question bank rather than generated by the model.

## 6. Key improvements

During development, the project changed in several important ways:

1. The app became a complete web application rather than a collection of static mockups.
2. Learners can personalize their name, level, topic, and difficulty.
3. Learning content now fits Learn, Practice, Quiz, and Challenge modes.
4. Answer evaluation includes hints, explanations, and encouragement.
5. SQLite-backed learner records track attempts and correct answers.
6. The summary recommends practice based on weak areas.
7. API credentials were moved away from browser JavaScript.
8. The app now includes a demo mode that works without an AI key.
9. Docker packaging allows repeatable deployment.
10. Architecture and development documentation support the final presentation.

## 7. Presentation demonstration

For a short live demonstration:

1. Open `http://127.0.0.1:5000`.
2. Introduce the target audience: working professionals preparing for or improving project-manager responsibilities.
3. Open the learner profile and explain how name, level, topic, and difficulty affect the experience.
4. Select Learn and ask for an explanation of the critical path.
5. Select Practice and answer a PERT question correctly or incorrectly.
6. Open Today's Performance to show attempts, accuracy, weak areas, strong areas, and the next lesson.
7. Explain how Flask serves the interface and protects optional AI credentials.
8. Present the architecture diagram and Docker deployment options.
