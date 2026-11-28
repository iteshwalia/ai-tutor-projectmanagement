"""Tutor response generation and model-provider integration."""

import json
import logging
import os
import re
from urllib import error, request
from urllib.parse import urlsplit

from . import __name__ as services_package

logger = logging.getLogger(services_package)
DIFFICULTY_INSTRUCTIONS = {
    "Beginner": (
        "Use everyday language, define project-management terms, explain one step at a time, "
        "and give a simple workplace example."
    ),
    "Intermediate": (
        "Use standard project-management terminology, practical workplace scenarios, and explain "
        "the main decision and trade-offs."
    ),
    "Advanced": (
        "Use complex PMP or PMI-ACP scenarios with competing constraints, explicit assumptions, "
        "and minimal scaffolding; compare important trade-offs."
    ),
}


def get_provider_config():
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    if gemini_key:
        key, key_name = gemini_key, "GEMINI_API_KEY"
        default_model = "gemini-3.5-flash-lite"
        default_url = (
            "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
        )
        model = os.getenv("GEMINI_MODEL", default_model)
        url = os.getenv("GEMINI_API_URL", default_url)
        provider = "Google Gemini"
    elif openai_key:
        key, key_name = openai_key, "OPENAI_API_KEY"
        default_model = "gpt-4o-mini"
        default_url = "https://api.openai.com/v1/chat/completions"
        model = os.getenv("OPENAI_MODEL", default_model)
        url = os.getenv("OPENAI_API_URL", default_url)
        provider = "OpenAI-compatible"
    else:
        return {
            "configured": False,
            "key": None,
            "key_name": "None",
            "model": "None",
            "url": "",
            "provider": "Demo knowledge",
        }

    return {
        "configured": True,
        "key": key,
        "key_name": key_name,
        "model": model,
        "url": url,
        "provider": provider,
    }


def public_provider_status():
    config = get_provider_config()
    return {
        "provider": config["provider"],
        "key_name": config["key_name"],
        "model": config["model"],
        "api_configured": config["configured"],
    }


def generate_model_response(message, profile, app_is_production):
    config = get_provider_config()
    parsed_url = urlsplit(config["url"])
    is_local_http = (
        not app_is_production
        and parsed_url.scheme == "http"
        and parsed_url.hostname in {"localhost", "127.0.0.1", "::1"}
    )
    if parsed_url.scheme != "https" and not is_local_http:
        logger.error("AI provider URL must use HTTPS outside local development.")
        return None, "The AI provider endpoint must use HTTPS.", 503

    difficulty = profile["difficulty"]
    system_prompt = (
        f"You are PM Mentor, a {difficulty} tutor for working professionals. "
        f"The learner is studying {profile['topic']}. "
        f"{DIFFICULTY_INSTRUCTIONS[difficulty]} "
        "Give hints before answers, encourage retrying, evaluate answers constructively, "
        "and redirect unrelated questions to project management."
    )
    payload = json.dumps(
        {
            "model": config["model"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            "temperature": 0.7,
        }
    ).encode("utf-8")
    provider_request = request.Request(
        config["url"],
        data=payload,
        headers={
            "Authorization": f"Bearer {config['key']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(provider_request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        content = result["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise ValueError("The model returned an empty response.")
        return content, None, None
    except (error.URLError, KeyError, json.JSONDecodeError, ValueError):
        logger.exception("AI provider request failed")
        return None, "The AI provider could not complete the request.", 502


def generate_model_question(profile, app_is_production):
    prompt = (
        "Create one original multiple-choice project-management question. "
        f"Use the topic {json.dumps(profile['topic'])} and difficulty "
        f"{json.dumps(profile['difficulty'])}. Do not repeat a generic definition question. "
        "Return a single plain JSON object without Markdown fences or surrounding commentary. "
        "Use these fields: question (string), answer (string matching one choice or its A-D "
        "letter), accepted (array of other valid answer strings), choices (array of exactly four "
        "distinct strings), hint (string that does not reveal the answer), and explanation "
        "(string explaining why the answer is correct)."
    )
    content, error_message, status = generate_model_response(
        prompt,
        profile,
        app_is_production,
    )
    if error_message:
        return None, error_message, status

    try:
        question = _parse_model_json(content)
        if not isinstance(question, dict):
            raise ValueError("The model response must be a JSON object.")

        question_text = question.get("question") or question.get("prompt")
        answer_value = (
            question.get("answer")
            or question.get("correct_answer")
            or question.get("correctAnswer")
        )
        hint = question.get("hint") or question.get("tip")
        explanation = question.get("explanation") or question.get("rationale")
        choices = question.get("choices") or question.get("options")
        accepted = question.get("accepted", question.get("accepted_answers", []))

        if isinstance(choices, dict):
            labeled_choices = {str(key).strip().casefold(): value for key, value in choices.items()}
            choices = [
                labeled_choices.get(letter, labeled_choices.get(f"option {letter}"))
                for letter in "abcd"
            ]
        elif isinstance(choices, list):
            choices = [
                choice.get("text", choice.get("label", choice.get("value")))
                if isinstance(choice, dict)
                else choice
                for choice in choices
            ]

        text_fields = ("question", "answer", "hint", "explanation")
        question_fields = {
            "question": question_text,
            "answer": answer_value,
            "hint": hint,
            "explanation": explanation,
        }
        if any(
            not isinstance(question_fields[field], str)
            or not question_fields[field].strip()
            or len(question_fields[field]) > 1200
            for field in text_fields
        ):
            raise ValueError("The model response contains an invalid question field.")

        if (
            not isinstance(choices, list)
            or len(choices) != 4
            or any(not isinstance(choice, str) or not choice.strip() for choice in choices)
        ):
            raise ValueError("The model response must contain four distinct choices.")

        choices = [_strip_model_choice_label(choice) for choice in choices]
        choice_keys = [" ".join(choice.casefold().split()) for choice in choices]
        if len(set(choice_keys)) != 4:
            raise ValueError("The model response must contain four distinct choices.")

        answer = _canonical_model_answer(answer_value, choices)
        answer_key = " ".join(answer.casefold().split())

        if accepted is None:
            accepted = []
        elif isinstance(accepted, str):
            accepted = [accepted]
        if not isinstance(accepted, list) or any(not isinstance(value, str) for value in accepted):
            raise ValueError("The model response contains invalid accepted answers.")
        accepted = [value for value in accepted if value.strip()]
        accepted_answers = {
            " ".join(value.strip().casefold().split()): value.strip()
            for value in [answer, *accepted]
        }
        answer_index = choice_keys.index(answer_key)
        answer_letter = chr(ord("A") + answer_index)
        accepted_answers[answer_letter.casefold()] = answer_letter
        accepted_answers[f"{answer_letter.casefold()}."] = f"{answer_letter}."

        return (
            {
                "topic": profile["topic"],
                "difficulty": profile["difficulty"],
                "question": question_text.strip(),
                "answer": answer,
                "accepted": list(accepted_answers.values()),
                "choices": choices,
                "hint": hint.strip(),
                "explanation": explanation.strip(),
            },
            None,
            None,
        )
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        logger.warning("AI provider returned an invalid practice question: %s", exc)
        return None, "The AI provider returned an invalid question. Please try again.", 502


def _parse_model_json(content):
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start < 0 or end <= start:
            raise
        return json.loads(content[start : end + 1])


def _strip_model_choice_label(choice):
    match = re.fullmatch(r"\s*[a-d][.)]\s*(.+?)\s*", choice, re.IGNORECASE)
    return match.group(1).strip() if match else choice.strip()


def _canonical_model_answer(answer, choices):
    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("The model response contains an invalid answer.")

    answer = answer.strip()
    choice_match = re.fullmatch(r"(?:option\s*)?([a-d])\.?", answer, re.IGNORECASE)
    if choice_match:
        return choices[ord(choice_match.group(1).lower()) - ord("a")]

    prefixed_answer = re.fullmatch(
        r"(?:option\s*)?([a-d])[.):]\s*(.+)",
        answer,
        re.IGNORECASE,
    )
    if prefixed_answer:
        choice = choices[ord(prefixed_answer.group(1).lower()) - ord("a")]
        if " ".join(prefixed_answer.group(2).casefold().split()) != " ".join(
            choice.casefold().split()
        ):
            raise ValueError("The model response answer label does not match its choice.")
        return choice

    answer_key = " ".join(answer.casefold().split())
    for choice in choices:
        if answer_key == " ".join(choice.casefold().split()):
            return choice.strip()
    raise ValueError("The model response answer must match one of its choices.")


def generate_demo_response(message, profile):
    text = message.lower()
    for keyword, answer in _fallback_knowledge().items():
        if keyword in text:
            return f"{answer} {_demo_difficulty_guidance(profile['difficulty'])}"
    return (
        f"For {profile['topic']}, begin by identifying the project goal, constraints, "
        f"and stakeholders. {_demo_difficulty_guidance(profile['difficulty'])} "
        "I can explain a concept, give a practice question, or start a short quiz."
    )


def _demo_difficulty_guidance(difficulty):
    guidance = {
        "Beginner": (
            "In simple terms, define the key idea and try one small next step on a project."
        ),
        "Intermediate": (
            "Apply the idea to a workplace scenario and identify the key decision and trade-off."
        ),
        "Advanced": (
            "Compare this approach with an alternative, including assumptions, constraints, "
            "and likely consequences."
        ),
    }
    return guidance[difficulty]


def _fallback_knowledge():
    from pm_mentor.learning_content import FALLBACK_KNOWLEDGE

    return FALLBACK_KNOWLEDGE
