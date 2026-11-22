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

QUESTION_BANK = [
    {
        "topic": "Project Planning & Scheduling",
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
]

FALLBACK_KNOWLEDGE = {
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
