# PM Mentor technical architecture

PM Mentor is a browser-based learning application backed by a Flask service. The browser manages the interactive quiz flow; the server protects provider credentials, generates questions, evaluates answers, and persists learner progress.

## System architecture

![PM Mentor technical architecture](architecture.svg)

```mermaid
flowchart LR
    learner["Learner"] --> ui

    subgraph browser["Browser"]
        ui["HTML, CSS, JavaScript modules"]
        quiz["Quiz state<br/>Question count · position · score"]
        client["JSON API client"]
        ui --> quiz
        ui --> client
    end

    subgraph service["Render Docker service"]
        waitress["Waitress WSGI server"]
        flask["Flask app factory<br/>Pages · static assets · security headers"]
        routes["API routes<br/>Learner · tutor · health"]
        learning["Question and evaluation flow<br/>Validate questions · grade answers · update progress"]
        tutor["Tutor service<br/>Provider calls · demo responses"]
        waitress --> flask --> routes
        routes --> learning
        routes --> tutor
    end

    subgraph data["Data and external services"]
        sqlite[("SQLite<br/>Profile · active question · progress")]
        content["Built-in question bank<br/>Topics · best practices · demo knowledge"]
        provider["Gemini or OpenAI-compatible provider"]
        env["Server environment<br/>API credentials"]
    end

    client <-->|"HTTPS JSON"| routes
    learning --> sqlite
    learning --> content
    env -.-> learning
    env -.-> tutor
    learning -->|"When configured: fresh question"| provider
    tutor -->|"When configured"| provider
    tutor -->|"Without a provider key"| content

    subgraph delivery["Build and deployment"]
        github["GitHub repository"] --> actions["GitHub Actions<br/>Ruff · pytest · Playwright"]
        github --> render["Render<br/>Docker · Waitress"]
    end

    actions -.-> render
```

### Component responsibilities

| Component | Responsibility |
|---|---|
| Browser UI (`templates/`, `static/js/`) | Renders the tutor, profile, learning modes, feedback, and progress. Quiz count, current position, and in-progress score live in browser memory. |
| Flask application (`pm_mentor/application.py`) | Serves pages and static files, initializes persistence, registers API routes, and applies security settings. |
| Learner routes (`pm_mentor/routes/learner.py`) | Handles profiles, question requests, answer evaluation, progress, report download, and reset. |
| Tutor routes (`pm_mentor/routes/tutor.py`) | Handles tutor chat and public provider status. |
| Tutor service (`pm_mentor/services/tutor.py`) | Calls configured model providers, parses and validates generated questions, and supplies demo responses when no key is configured. |
| SQLite repository (`pm_mentor/learner_repository.py`) | Stores the learner profile, active question and cumulative progress by signed session identifier. |
| Learning content (`pm_mentor/learning_content.py`) | Supplies the no-key question bank, topic content, and best-practice guidance. |
| Render service | Runs the Dockerized Flask application with Waitress. Render Free local storage may be ephemeral. |
| GitHub Actions | Runs Ruff and the API/browser test suite on pushes. |

### API surface

| Endpoint | Purpose |
|---|---|
| `GET /healthz` | Service health check |
| `GET /api/status` | Public model-provider configuration status; never returns credentials |
| `GET` / `POST /api/profile` | Read or update the learner profile |
| `GET /api/question` | Generate a fresh model question when configured, otherwise select from the built-in bank |
| `POST /api/evaluate` | Grade the active question, save progress, and return feedback |
| `GET /api/progress` | Read cumulative learner progress |
| `GET /api/progress/report` | Download a text progress report |
| `POST /api/reset` | Reset cumulative progress and the active question |
| `POST /api/chat` | Send a tutoring request to the configured provider or built-in demo tutor |

## Quiz and answer flow

```mermaid
sequenceDiagram
    actor Learner
    participant Browser as Browser UI
    participant API as Flask learner API
    participant Service as Question and evaluation service
    participant Provider as Configured model provider
    participant Bank as Built-in question bank
    participant DB as SQLite

    Learner->>Browser: Start Quiz
    Browser->>Learner: Ask for 1–20 questions
    Learner->>Browser: Choose quiz length
    loop Each question
        Browser->>API: GET /api/question
        API->>Service: Generate a question for profile topic and difficulty
        alt Provider key configured
            Service->>Provider: Request a fresh question
            Provider-->>Service: Return question content
            Service->>Service: Parse and validate question and answer
        else No provider key
            Service->>Bank: Select matching authored question
            Bank-->>Service: Return question and answer
        end
        Service->>DB: Save active question and answer key
        API-->>Browser: Return question and choices (no answer key)
        Browser-->>Learner: Show numbered question
        Learner->>Browser: Submit answer
        Browser->>API: POST /api/evaluate
        API->>Service: Evaluate answer and prepare feedback
        Service->>DB: Update cumulative and topic progress
        API-->>Browser: Correctness, explanation, personalized feedback, tip
        Browser-->>Learner: Show feedback
    end
    Browser-->>Learner: Show final correct count and percentage
```

The quiz's requested length and running score are held in browser memory, while the active answer key and cumulative learning progress remain on the server. Reloading the page does not resume an in-progress quiz.

When a provider is configured, every `/api/question` request asks the model for a new question. The server validates the response before exposing the choices; the answer key remains server-side. Invalid model output is returned as an error rather than silently replaced with a bank question. Without a provider key, question requests use the topic- and difficulty-matched bank.

## Tutor chat flow

```mermaid
sequenceDiagram
    actor Learner
    participant Browser as Browser UI
    participant API as Flask tutor API
    participant Service as Tutor service
    participant Provider as Gemini or compatible provider
    participant Demo as Built-in demo knowledge

    Learner->>Browser: Ask about project management
    Browser->>API: POST /api/chat
    API->>Service: Pass message and learner profile
    alt Provider key configured
        Service->>Provider: Send prompt using server-side credentials
        Provider-->>Service: Return tutor response
    else No provider key
        Service->>Demo: Find topic guidance
        Demo-->>Service: Return demo response
    end
    Service-->>API: Tutor response
    API-->>Browser: JSON reply
    Browser-->>Learner: Display response
```

Provider credentials are read from server environment variables and are never sent to the browser. The service supports Google Gemini and OpenAI-compatible chat-completion endpoints.
