"""Project-management learning content used by practice and demo modes."""

TOPICS = {
    "Project Planning & Scheduling",
    "Agile Methodologies",
    "Stakeholder Management",
    "Risk Management",
    "Leadership & Team Performance",
    "CPMAI - AI Project Management",
}
LEVELS = {"Beginner", "Intermediate", "Advanced"}
DEFAULT_LEARNER_NAME = "Itesh"

TOPIC_BEST_PRACTICES = {
    "Project Planning & Scheduling": (
        "Confirm scope and dependencies before estimating, and update the schedule when "
        "assumptions change."
    ),
    "Agile Methodologies": (
        "Keep the backlog ordered by value and refine upcoming work with the delivery team."
    ),
    "Stakeholder Management": (
        "Tailor communication to each stakeholder's influence and information needs, then "
        "revisit engagement as conditions change."
    ),
    "Risk Management": (
        "Give each significant risk an owner, a trigger, a response, and a regular review date."
    ),
    "Leadership & Team Performance": (
        "Clarify outcomes and decision rights, and make it safe for the team to raise blockers "
        "early."
    ),
    "CPMAI - AI Project Management": (
        "Check data quality, representativeness, and readiness before modeling, and retain human "
        "oversight after deployment."
    ),
}

QUESTION_BANK = [
    {
        "topic": "Project Planning & Scheduling",
        "difficulty": "Intermediate",
        "question": (
            "A task has an optimistic estimate of 3 days, a most likely estimate of 5 days, "
            "and a pessimistic estimate of 13 days. What is the PERT expected duration?"
        ),
        "answer": "6 days",
        "accepted": ["6", "6 days", "six"],
        "choices": ["5 days", "6 days", "7 days", "8 days"],
        "hint": "Use the PERT formula and give the most likely estimate four times the weight.",
        "explanation": "PERT expected duration = (3 + 20 + 13) / 6 = 6 days.",
    },
    {
        "topic": "Stakeholder Management",
        "difficulty": "Intermediate",
        "question": (
            "A stakeholder has high interest and high influence. Which engagement strategy "
            "is most appropriate?"
        ),
        "answer": "Manage closely",
        "accepted": ["manage closely", "closely", "keep satisfied and involved"],
        "choices": ["Monitor", "Keep informed", "Keep satisfied", "Manage closely"],
        "hint": "Consider the stakeholder's influence as well as their interest.",
        "explanation": (
            "High-power, high-interest stakeholders are a priority and should be managed closely."
        ),
    },
    {
        "topic": "Agile Methodologies",
        "difficulty": "Beginner",
        "question": (
            "Who owns the Product Backlog and is accountable for maximizing product value in Scrum?"
        ),
        "answer": "Product Owner",
        "accepted": ["product owner", "the product owner"],
        "choices": ["Scrum Master", "Project Manager", "Product Owner", "Development Team"],
        "hint": "Separate responsibility for product value from facilitation of the Scrum process.",
        "explanation": (
            "The Product Owner owns the Product Backlog and is accountable for maximizing value."
        ),
    },
    {
        "topic": "Risk Management",
        "difficulty": "Intermediate",
        "question": (
            "A team identifies a future risk and agrees to add an extra test cycle only if "
            "the risk occurs. What strategy is this?"
        ),
        "answer": "Contingency response",
        "accepted": ["contingency", "contingency response", "contingency plan"],
        "choices": ["Mitigation", "Avoidance", "Contingency response", "Transfer"],
        "hint": "The response is prepared before the event, but activated only if it occurs.",
        "explanation": (
            "A contingency response is prepared in advance and triggered only when a defined "
            "risk event occurs."
        ),
    },
    {
        "topic": "Project Planning & Scheduling",
        "difficulty": "Beginner",
        "question": (
            "Which planning artifact decomposes the total project scope into manageable "
            "deliverables and work packages?"
        ),
        "answer": "Work Breakdown Structure (WBS)",
        "accepted": ["work breakdown structure", "wbs"],
        "choices": [
            "Stakeholder register",
            "Work Breakdown Structure (WBS)",
            "Risk report",
            "Issue log",
        ],
        "hint": "Look for the hierarchical breakdown of all approved project work.",
        "explanation": (
            "The WBS organizes the approved scope into deliverables and smaller work packages "
            "that can be estimated and managed."
        ),
    },
    {
        "topic": "Project Planning & Scheduling",
        "difficulty": "Advanced",
        "question": (
            "A critical-path activity slips by two days and no recovery action is taken. "
            "What is the direct effect on the schedule?"
        ),
        "answer": "The project completion date is delayed by two days",
        "accepted": [
            "the project completion date is delayed by two days",
            "the finish date is delayed by two days",
            "project completion is delayed by two days",
        ],
        "choices": [
            "The project completion date is delayed by two days",
            "The project budget is reduced",
            "The activity gains two days of float",
            "The scope is automatically reduced",
        ],
        "hint": "Critical-path activities have no total float to absorb a delay.",
        "explanation": (
            "With zero float and no schedule recovery, a two-day delay to a critical-path "
            "activity moves the project's finish date by two days."
        ),
    },
    {
        "topic": "Project Planning & Scheduling",
        "difficulty": "Intermediate",
        "question": "A project's Cost Performance Index (CPI) is 0.80. What does this indicate?",
        "answer": "The project is over budget",
        "accepted": ["the project is over budget", "over budget", "cost overrun"],
        "choices": [
            "The project is under budget",
            "The project is over budget",
            "The project is ahead of schedule",
            "The project has no cost variance",
        ],
        "hint": "CPI compares earned value with actual cost; a value below 1.0 is unfavorable.",
        "explanation": (
            "A CPI of 0.80 means the project is earning 80 cents of value for each dollar "
            "spent, which indicates cost inefficiency and an over-budget trend."
        ),
    },
    {
        "topic": "Stakeholder Management",
        "difficulty": "Beginner",
        "question": (
            "A stakeholder has low power but high interest in the project. "
            "What engagement approach is usually appropriate?"
        ),
        "answer": "Keep informed",
        "accepted": ["keep informed", "inform", "keep them informed"],
        "choices": ["Monitor", "Keep informed", "Keep satisfied", "Manage closely"],
        "hint": "Use both power and interest to identify the stakeholder's quadrant.",
        "explanation": (
            "Stakeholders with high interest and lower power should generally receive timely "
            "information and opportunities to provide input."
        ),
    },
    {
        "topic": "Stakeholder Management",
        "difficulty": "Advanced",
        "question": (
            "Which tool compares stakeholders' current and desired engagement levels "
            "to identify communication or involvement gaps?"
        ),
        "answer": "Stakeholder engagement assessment matrix",
        "accepted": [
            "stakeholder engagement assessment matrix",
            "engagement assessment matrix",
        ],
        "choices": [
            "Responsibility assignment matrix",
            "Stakeholder engagement assessment matrix",
            "Probability and impact matrix",
            "Schedule network diagram",
        ],
        "hint": "It records current and desired engagement for each stakeholder.",
        "explanation": (
            "The stakeholder engagement assessment matrix helps the team compare current "
            "engagement with the desired state and plan actions to close gaps."
        ),
    },
    {
        "topic": "Agile Methodologies",
        "difficulty": "Beginner",
        "question": (
            "In Scrum, which event lets stakeholders inspect the increment and provide "
            "feedback on the product?"
        ),
        "answer": "Sprint Review",
        "accepted": ["sprint review", "the sprint review"],
        "choices": ["Sprint Planning", "Daily Scrum", "Sprint Review", "Sprint Retrospective"],
        "hint": "This event happens near the end of a sprint and focuses on the product.",
        "explanation": (
            "The Sprint Review is an opportunity to inspect the increment, discuss progress "
            "toward the product goal, and adapt future work based on feedback."
        ),
    },
    {
        "topic": "Agile Methodologies",
        "difficulty": "Intermediate",
        "question": (
            "What is the main purpose of the Daily Scrum for the developers?"
        ),
        "answer": "Inspect progress toward the Sprint Goal and adapt the plan",
        "accepted": [
            "inspect progress toward the sprint goal and adapt the plan",
            "inspect progress and adapt the plan",
            "adapt the plan toward the sprint goal",
        ],
        "choices": [
            "Report individual hours to the project manager",
            "Inspect progress toward the Sprint Goal and adapt the plan",
            "Approve the product release",
            "Re-estimate the entire product backlog",
        ],
        "hint": "It is a short planning event for the people doing the work.",
        "explanation": (
            "Developers use the Daily Scrum to inspect progress toward the Sprint Goal and "
            "adjust their plan for the next day."
        ),
    },
    {
        "topic": "Risk Management",
        "difficulty": "Beginner",
        "question": (
            "Which document records identified risks, their owners, analysis, and planned "
            "responses?"
        ),
        "answer": "Risk register",
        "accepted": ["risk register", "the risk register"],
        "choices": ["Issue log", "Risk register", "Assumption log", "Change log"],
        "hint": "This is the central record maintained during risk management.",
        "explanation": (
            "The risk register records individual risks and supporting details such as "
            "owners, analysis, triggers, and response plans."
        ),
    },
    {
        "topic": "Risk Management",
        "difficulty": "Intermediate",
        "question": (
            "A team adds a prototype test to reduce the chance that a technical risk will "
            "occur. Which threat response strategy is this?"
        ),
        "answer": "Mitigate",
        "accepted": ["mitigate", "mitigation", "risk mitigation"],
        "choices": ["Avoid", "Mitigate", "Transfer", "Accept"],
        "hint": "The response reduces the probability or impact rather than eliminating all risk.",
        "explanation": (
            "Mitigation takes action to reduce a threat's probability or impact to an "
            "acceptable level."
        ),
    },
    {
        "topic": "Risk Management",
        "difficulty": "Intermediate",
        "question": (
            "A project purchases insurance so a third party bears the financial impact "
            "of a particular threat. Which response strategy is this?"
        ),
        "answer": "Transfer",
        "accepted": ["transfer", "risk transfer", "transferring the risk"],
        "choices": ["Avoid", "Mitigate", "Transfer", "Accept"],
        "hint": "The response shifts ownership of the financial impact to another party.",
        "explanation": (
            "Risk transfer allocates responsibility for the threat's impact to a third party, "
            "often through insurance or contractual terms."
        ),
    },
    {
        "topic": "Leadership & Team Performance",
        "difficulty": "Beginner",
        "question": (
            "A servant leader notices the team is blocked by a dependency and works to "
            "remove it. What leadership behavior is being demonstrated?"
        ),
        "answer": "Removing impediments",
        "accepted": [
            "removing impediments",
            "remove impediments",
            "clearing blockers",
            "remove blockers",
        ],
        "choices": [
            "Centralizing every decision",
            "Removing impediments",
            "Increasing work in progress",
            "Avoiding team feedback",
        ],
        "hint": "The leader helps the team make progress rather than directing every task.",
        "explanation": (
            "Servant leaders support the team's effectiveness by helping resolve blockers "
            "and enabling people to do their work."
        ),
    },
    {
        "topic": "CPMAI - AI Project Management",
        "difficulty": "Beginner",
        "question": (
            "Before building an AI model, why should a project team assess data readiness?"
        ),
        "answer": "To verify that suitable, sufficient, and usable data is available",
        "accepted": [
            "to verify that suitable, sufficient, and usable data is available",
            "to verify that suitable sufficient and usable data is available",
            "to assess data quality availability and suitability",
            "check data quality and availability",
        ],
        "choices": [
            "To select a project logo",
            "To verify that suitable, sufficient, and usable data is available",
            "To skip stakeholder validation",
            "To guarantee a model will never make errors",
        ],
        "hint": "AI project outcomes depend on the relevance and quality of the data.",
        "explanation": (
            "Data readiness checks whether relevant data exists, is accessible, and is "
            "sufficiently usable and representative for the intended AI outcome."
        ),
    },
    {
        "topic": "Agile Methodologies",
        "difficulty": "Advanced",
        "question": (
            "Halfway through a Sprint, a high-value request arrives. The Sprint Goal is still "
            "achievable, but the new work would displace committed scope. "
            "What is the best next step?"
        ),
        "answer": "Renegotiate scope while protecting the Sprint Goal",
        "accepted": [
            "renegotiate scope while protecting the sprint goal",
            "protect the sprint goal while negotiating scope",
            "discuss scope with the product owner while protecting the sprint goal",
        ],
        "choices": [
            "Add the new work immediately and extend the Sprint",
            "Cancel the Sprint because a stakeholder requested a change",
            "Renegotiate scope while protecting the Sprint Goal",
            "Accept the change without discussing its impact",
        ],
        "hint": "Keep the Sprint Goal stable while considering whether scope can be adjusted.",
        "explanation": (
            "The Product Owner and Developers can renegotiate scope as they learn more, "
            "provided the Sprint Goal is not endangered."
        ),
    },
    {
        "topic": "Risk Management",
        "difficulty": "Advanced",
        "question": (
            "A threat occurs despite mitigation, and the trigger for its approved contingency "
            "response is met. What should the project manager do next?"
        ),
        "answer": "Execute the approved contingency response and update the risk record",
        "accepted": [
            "execute the approved contingency response and update the risk record",
            "execute the contingency response",
            "implement the planned contingency response",
        ],
        "choices": [
            "Ignore the event because mitigation was already attempted",
            "Execute the approved contingency response and update the risk record",
            "Close the risk without assessing the impact",
            "Replace the response with an unapproved workaround",
        ],
        "hint": "The agreed trigger has been met, so use the response planned for that event.",
        "explanation": (
            "When the trigger occurs, implement the approved contingency response, assess "
            "the resulting impact, and update the risk record."
        ),
    },
    {
        "topic": "Leadership & Team Performance",
        "difficulty": "Intermediate",
        "question": (
            "Two experienced team members disagree about a design approach. Which action best "
            "supports servant leadership?"
        ),
        "answer": "Facilitate a discussion so the team can decide using shared criteria",
        "accepted": [
            "facilitate a discussion so the team can decide using shared criteria",
            "facilitate a team decision using shared criteria",
            "help the team compare options and reach a decision",
        ],
        "choices": [
            "Choose the design yourself to end the disagreement",
            "Facilitate a discussion so the team can decide using shared criteria",
            "Ask the sponsor to choose without the team's input",
            "Avoid the issue and let the disagreement continue",
        ],
        "hint": "Enable the team's decision-making rather than taking ownership away from them.",
        "explanation": (
            "A servant leader facilitates collaboration and helps the team make an informed "
            "decision instead of imposing a solution."
        ),
    },
    {
        "topic": "Leadership & Team Performance",
        "difficulty": "Advanced",
        "question": (
            "Several departments repeatedly redirect team members, causing missed Sprint "
            "Goals. What should the project leader do first?"
        ),
        "answer": "Resolve priority conflicts with sponsors and protect team focus",
        "accepted": [
            "resolve priority conflicts with sponsors and protect team focus",
            "resolve conflicting priorities with sponsors and protect team focus",
            "negotiate priorities and protect the team's focus",
        ],
        "choices": [
            "Increase individual workload targets",
            "Remove team members who raise the conflict",
            "Resolve priority conflicts with sponsors and protect team focus",
            "Continue planning as if team capacity were unchanged",
        ],
        "hint": "Address the organizational cause of the interruptions and align decision-makers.",
        "explanation": (
            "The leader should make the competing priorities visible, work with sponsors and "
            "functional leaders to resolve them, and protect the team's ability to deliver."
        ),
    },
    {
        "topic": "CPMAI - AI Project Management",
        "difficulty": "Intermediate",
        "question": (
            "An AI pilot produces accurate results, but users distrust them because teams use "
            "different definitions for the input labels. What should the project team do next?"
        ),
        "answer": "Validate data definitions and labels with domain experts and users",
        "accepted": [
            "validate data definitions and labels with domain experts and users",
            "align data definitions with domain experts and users",
            "standardize and validate the labels with users",
        ],
        "choices": [
            "Increase model complexity immediately",
            "Validate data definitions and labels with domain experts and users",
            "Ignore user feedback because accuracy is high",
            "Deploy the model to more users without review",
        ],
        "hint": "Reliable AI depends on shared, meaningful labels as well as model accuracy.",
        "explanation": (
            "Domain experts and users should validate shared definitions and label quality "
            "before the team treats the pilot's results as trustworthy."
        ),
    },
    {
        "topic": "CPMAI - AI Project Management",
        "difficulty": "Advanced",
        "question": (
            "After deployment, the data patterns shift and model performance declines. What "
            "is the best governance response?"
        ),
        "answer": "Use monitoring thresholds and an approved human-reviewed retraining process",
        "accepted": [
            "use monitoring thresholds and an approved human-reviewed retraining process",
            "monitor for drift and retrain through an approved process with human review",
            "use defined monitoring and controlled retraining with human oversight",
        ],
        "choices": [
            "Retrain automatically on all new data without review",
            "Ignore the decline if the model once passed testing",
            "Use monitoring thresholds and an approved human-reviewed retraining process",
            "Delete the model without assessing operational impact",
        ],
        "hint": "Manage model drift with defined monitoring, decision thresholds, and oversight.",
        "explanation": (
            "The team should monitor performance against agreed thresholds and use a "
            "controlled, human-reviewed process to decide whether retraining is appropriate."
        ),
    },
]

FALLBACK_KNOWLEDGE = {
    "work breakdown structure": (
        "A Work Breakdown Structure (WBS) organizes the approved project scope into "
        "deliverables and manageable work packages."
    ),
    "wbs": (
        "A WBS is a hierarchical breakdown of the approved project scope into deliverables "
        "and work packages that can be estimated and managed."
    ),
    "scope creep": (
        "Scope creep is the gradual growth of project work without the required review, "
        "approval, and adjustment of time, cost, or resources."
    ),
    "project charter": (
        "A project charter formally authorizes a project and gives the project manager "
        "authority to use organizational resources."
    ),
    "change control": (
        "Change control evaluates a requested change, its impact, and the required approval "
        "before updating project baselines or plans."
    ),
    "cost performance index": (
        "The Cost Performance Index (CPI) is earned value divided by actual cost. "
        "A value below 1.0 signals that cost efficiency is worse than planned."
    ),
    "cpi": (
        "CPI is earned value divided by actual cost. A CPI below 1.0 means the project "
        "is earning less value per dollar than planned."
    ),
    "earned value": (
        "Earned value management compares planned value, earned value, and actual cost "
        "to assess schedule and cost performance."
    ),
    "power-interest": (
        "A power-interest grid groups stakeholders by influence and interest to guide "
        "how often and how closely to engage them."
    ),
    "stakeholder engagement assessment matrix": (
        "This matrix compares each stakeholder's current and desired engagement level "
        "so the team can plan steps to close the gap."
    ),
    "sprint review": (
        "A Sprint Review is where the Scrum Team and stakeholders inspect the increment, "
        "discuss outcomes, and adapt future work."
    ),
    "daily scrum": (
        "The Daily Scrum is a short event for developers to inspect progress toward the "
        "Sprint Goal and adapt their plan."
    ),
    "definition of done": (
        "The Definition of Done is a shared description of the quality and completion "
        "checks an increment must meet."
    ),
    "product owner": (
        "The Product Owner is accountable for maximizing product value and managing "
        "the Product Backlog."
    ),
    "risk register": (
        "A risk register tracks identified risks, owners, analysis, triggers, and planned "
        "response strategies."
    ),
    "risk mitigation": (
        "Risk mitigation reduces the probability or impact of a threat through planned "
        "preventive or impact-limiting actions."
    ),
    "risk transfer": (
        "Risk transfer shifts responsibility for some or all of a threat's financial impact "
        "to another party, such as through insurance."
    ),
    "servant leadership": (
        "Servant leadership focuses on enabling the team, listening, removing impediments, "
        "and supporting shared ownership."
    ),
    "data readiness": (
        "Data readiness checks whether data is available, relevant, sufficiently complete, "
        "and suitable for the intended AI use case."
    ),
    "acceptance criteria": (
        "Acceptance criteria are specific conditions a deliverable must satisfy to be "
        "accepted by its customer or product owner."
    ),
    "critical path": (
        "The critical path is the longest sequence of dependent activities that determines "
        "the shortest possible project duration."
    ),
    "stakeholder": (
        "Use a power-interest grid to decide whether to monitor, inform, satisfy, or manage "
        "stakeholders closely."
    ),
    "agile": (
        "Agile delivers value in small increments and adapts plans based on frequent feedback."
    ),
    "risk": (
        "Risk management identifies uncertain events, assesses probability and impact, and "
        "assigns a response strategy."
    ),
    "scrum": (
        "Scrum uses short iterations called sprints. The Product Owner owns value priorities "
        "and the Scrum Master supports the process."
    ),
}
