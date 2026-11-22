"""Tutor chat and provider-status API routes."""

from flask import Blueprint, current_app, jsonify
from flask import request as flask_request

from backend.database import get_learner_state
from backend.services.tutor import (
    generate_demo_response,
    generate_model_response,
    public_provider_status,
)

tutor = Blueprint("tutor", __name__, url_prefix="/api")


@tutor.post("/chat")
def chat():
    data = flask_request.get_json(silent=True)
    message = data.get("message") if isinstance(data, dict) else None
    message = message.strip() if isinstance(message, str) else ""
    if not message:
        return jsonify({"error": "A non-empty message is required."}), 400
    if len(message) > 4000:
        return jsonify({"error": "Messages must be 4,000 characters or fewer."}), 400

    profile = get_learner_state()["profile"]
    provider = public_provider_status()
    if provider["api_configured"]:
        response, error, status = generate_model_response(
            message,
            profile,
            current_app.config["ENVIRONMENT"] == "production",
        )
        if error:
            return jsonify({"error": error, "source": "ai"}), status
        return jsonify({"reply": response, "source": "ai"})
    return jsonify({"reply": generate_demo_response(message, profile), "source": "demo"})


@tutor.get("/status")
def status():
    return jsonify(public_provider_status())
