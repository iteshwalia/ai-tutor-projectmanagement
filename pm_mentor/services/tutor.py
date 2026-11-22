"""Tutor response generation and model-provider integration."""

import json
import logging
import os
from urllib import error, request
from urllib.parse import urlsplit

from . import __name__ as services_package

logger = logging.getLogger(services_package)


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

    system_prompt = (
        f"You are PM Mentor, a {profile['difficulty']} tutor for working professionals. "
        f"The learner is studying {profile['topic']}. "
        "Explain simply with workplace examples, give hints before answers, encourage retrying, "
        "evaluate answers constructively, and redirect unrelated questions to project management."
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


def generate_demo_response(message, profile):
    text = message.lower()
    for keyword, answer in _fallback_knowledge().items():
        if keyword in text:
            return (
                f"{answer} For a {profile['difficulty'].lower()}-level learner, apply this "
                "to a real project team and identify the decision, constraint, "
                "and expected outcome."
            )
    return (
        f"For {profile['topic']}, begin by identifying the project goal, constraints, "
        "and stakeholders. I can explain a concept, give a practice question, "
        "or start a short quiz."
    )


def _fallback_knowledge():
    from pm_mentor.learning_content import FALLBACK_KNOWLEDGE

    return FALLBACK_KNOWLEDGE
