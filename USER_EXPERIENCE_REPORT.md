# PM Mentor User Experience and Development Process Report

**Prepared:** 22 November 2026
**Project:** PM Mentor — AI Project Management Tutor

## Executive summary

PM Mentor is designed as a focused learning companion for working professionals who are preparing for project-management responsibilities or strengthening skills they use at work. Its core learning loop is:

**Choose a topic and difficulty → learn or practice → receive feedback → review progress → continue with a recommendation.**

The experience is intended to feel more like guided professional learning than a general-purpose chatbot. The interface offers Learn, Practice, Quiz, and Challenge modes; a learner profile; topic- and difficulty-matched content; answer feedback; and a progress summary with a downloadable report.

The design decisions in this report come from the project brief, product implementation, and recorded browser regression checks. They are not a substitute for formal learner interviews or a usability study; no such study is documented.

## Intended learner and learning context

| Design consideration | Product response |
|---|---|
| Learner | Working professionals preparing for project-manager responsibilities or looking to improve project-management knowledge |
| Learning context | Short, self-paced sessions that can begin with a question or a selected learning mode |
| Subject scope | Project planning and scheduling, Agile, stakeholders, risk, leadership, and AI project management |
| Learner starting point | A profile for name, current level, focus topic, and preferred difficulty |
| Desired result | Understand a concept, apply it to a scenario, learn from mistakes, and identify a useful next step |

## Experience goals and design rationale

### 1. Keep the tutor focused

The product is intentionally scoped to project management instead of presenting itself as an all-purpose assistant. A clear topic selector, project-management suggestions, and domain-specific examples set expectations and help learners start with relevant material.

### 2. Let learners choose how to study

Four modes support different intentions:

- **Learn** provides a concept explanation.
- **Practice** gives a question to build confidence.
- **Quiz** frames questions as a knowledge check.
- **Challenge** offers a more applied scenario.

Learners can also use the chat composer directly, so the modes guide rather than replace self-directed questions.

### 3. Make personalization affect the lesson

The learner can select a topic and a Beginner, Intermediate, or Advanced difficulty. Difficulty is not just a profile label: it changes mode prompts and selects a question variant for the chosen topic. The profile and practice question show the selected difficulty so the adaptation is visible.

### 4. Make mistakes useful

Answer evaluation distinguishes correct and incorrect answers. Incorrect responses provide a hint, the correct answer, an explanation, and encouragement. This is intended to support another learning attempt rather than stop at a score.

### 5. Show progress and a next step

The learning summary presents attempts, correct answers, accuracy, topic results, strong areas, topics needing practice, and a recommended next lesson. A downloadable report lets the learner retain or review the session summary.

### 6. Keep interactions understandable and recoverable

The profile dialog displays a saving state while a request is pending. If a save fails, an accessible error appears inside the dialog and the learner can retry without losing the selections. Closing a dialog returns focus to the control that opened it.

### 7. Make the AI connection transparent

Provider status appears in the application, while model credentials remain on the server and are not exposed in browser code. When no model key is configured, the built-in demo tutor keeps core learning interactions available. Settings also explain the provider configuration and warn learners not to submit sensitive information to a free-tier model.

## Learner journey

1. **Orient:** The learner sees the PM Mentor workspace, the current focus topic, suggested learning actions, and the four modes.
2. **Personalize:** The learner opens the profile to set a name, current level, topic, and preferred difficulty.
3. **Choose an activity:** The learner selects Learn, Practice, Quiz, or Challenge, or asks a question in the composer.
4. **Engage:** The tutor explains a concept or presents a topic- and difficulty-matched practice question.
5. **Reflect:** The learner submits an answer and receives corrective feedback, hints, explanations, and encouragement.
6. **Review:** Progress is summarized by overall metrics and topic areas, with a recommended next lesson.
7. **Continue:** The learner can download the summary and use the recommendation to guide the next session.

## Development steps followed

| Step | Work completed | User-experience outcome |
|---|---|---|
| 1. Define the learning problem | Focused the project on project management for working professionals | Clear audience and subject scope |
| 2. Establish the teaching style | Specified plain language, workplace examples, hints, constructive evaluation, and encouragement | Consistent tutoring intent across modes |
| 3. Build the first workspace | Created the chat, composer, suggested actions, profile, and mode navigation | A usable starting point for the learner |
| 4. Add learning activities | Connected Learn, Practice, Quiz, and Challenge flows to the tutor and question bank | More than a generic chat interaction |
| 5. Add personalization | Added name, level, topic, and difficulty controls | Learner context informs tutor behavior |
| 6. Add evaluation and progress | Added answer checking, feedback, session metrics, topic results, and recommendations | Learners can see what to improve and what to do next |
| 7. Add a model provider safely | Added optional Gemini service-side calls and a demo fallback | AI responses are available without putting credentials in the browser; the app remains usable without a key |
| 8. Refine the information architecture | Organized the frontend and backend into feature- and domain-oriented modules | Related behavior is easier to locate and maintain |
| 9. Close interaction gaps | Fixed profile-dialog wiring, restored focus on close, and made save progress/errors visible | Profile changes are more understandable and recoverable |
| 10. Add regression coverage | Added Playwright checks for major browser flows and generated test reports | Key interactions can be rechecked consistently |
| 11. Deploy and verify | Published the app to Render and checked health/provider status and browser behavior | The tutor is accessible online; free-tier operational limits are documented |

The chronological development record is in [DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md), and the prompt and implementation story is in [DEVELOPMENT.md](DEVELOPMENT.md).

## Validation evidence

The current regression suite passed **26 tests**: 22 API/backend tests and four Playwright browser tests. The browser cases cover:

- Home, settings, and profile dialogs, including focus restoration
- Profile save failure, retry, successful difficulty change, and persistence after reload
- Topic and difficulty guidance in all four learning modes
- Chat by keyboard, quiz/practice questions, correct and incorrect feedback, progress metrics, report download, and reset

The browser suite uses Chromium and an isolated local Flask app with a temporary SQLite database and demo responses. It does not use learner data or credentials from Render. See the [regression test report](REGRESSION_TEST_REPORT.md) for results and limitations.

## Constraints and evidence boundaries

- **No formal usability study is documented.** The current rationale is based on the project brief, implementation choices, and functional regression tests. Learner interviews and observed usability sessions remain future validation work.
- **Question generation is not model-driven.** Practice questions are selected from the authored question bank and matched to topic and difficulty; Gemini is used for tutor chat, not to generate each practice question.
- **Automated browser coverage is Chromium-only.** It does not include Firefox/WebKit, screenshot-based visual comparison, or a full assistive-technology audit.
- **The automated suite uses the demo tutor.** A live Gemini response was verified separately; automated tests do not depend on external model calls.
- **Render Free has operational limits.** The service can sleep while idle and local SQLite data may not persist through restarts or redeployments.
- **The Gemini free tier has privacy and usage limits.** Learners should not submit sensitive or confidential information.

## Recommended next UX validation

1. Ask working professionals to complete representative tasks: change difficulty, start practice, recover from an incorrect answer, and find their next lesson.
2. Observe where learners hesitate or misinterpret labels, feedback, and progress metrics before changing the interface.
3. Check keyboard-only and screen-reader journeys for profile editing, mode selection, answer feedback, and report download.
4. Test slow or interrupted network conditions, including a Render cold start, and confirm the saving state and recovery guidance are clear.
5. Evaluate whether topic recommendations help learners choose a next lesson; collect any usage data only with appropriate notice and consent.

## Related project artifacts

- [Architecture and sequence diagrams](architecture.md)
- [Full test report](TEST_REPORT.md) ([PDF](TEST_REPORT.pdf), [Word](TEST_REPORT.docx))
- [Playwright regression report](REGRESSION_TEST_REPORT.md) ([PDF](REGRESSION_TEST_REPORT.pdf), [Word](REGRESSION_TEST_REPORT.docx))
