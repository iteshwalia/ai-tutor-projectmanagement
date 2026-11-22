"""Learner profile, practice, and progress API routes."""

import random

from flask import Blueprint, jsonify
from flask import request as flask_request

from backend.content import LEVELS, QUESTION_BANK, TOPICS
from backend.database import get_learner_state, save_learner_state

learner = Blueprint("learner", __name__, url_prefix="/api")


@learner.get("/profile")
def get_profile():
    return jsonify(get_learner_state()["profile"])


@learner.post("/profile")
def update_profile():
    data = flask_request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A JSON profile is required."}), 400

    state = get_learner_state()
    profile = state["profile"]
    name = data.get("name")
    if isinstance(name, str) and name.strip():
        profile["name"] = name.strip()[:80]
    if isinstance(data.get("level"), str) and data["level"] in LEVELS:
        profile["level"] = data["level"]
    if isinstance(data.get("difficulty"), str) and data["difficulty"] in LEVELS:
        profile["difficulty"] = data["difficulty"]
    if isinstance(data.get("topic"), str) and data["topic"] in TOPICS:
        profile["topic"] = data["topic"]
    state["profile"] = profile
    save_learner_state(state)
    return jsonify(profile)


@learner.get("/question")
def question():
    state = get_learner_state()
    profile = state["profile"]
    matching = [item for item in QUESTION_BANK if item["topic"] == profile["topic"]]
    item = random.choice(matching or QUESTION_BANK)
    state["active_question"] = item
    save_learner_state(state)
    return jsonify(
        {
            "topic": item["topic"],
            "question": item["question"],
            "choices": item["choices"],
            "hint": item["hint"],
        }
    )


@learner.post("/evaluate")
def evaluate():
    data = flask_request.get_json(silent=True)
    answer = data.get("answer") if isinstance(data, dict) else None
    answer = answer.strip().casefold() if isinstance(answer, str) else ""
    if not answer:
        return jsonify({"error": "A non-empty answer is required."}), 400
    if len(answer) > 1000:
        return jsonify({"error": "Answers must be 1,000 characters or fewer."}), 400

    state = get_learner_state()
    item = state["active_question"]
    if not item:
        return jsonify({"error": "No active question."}), 400

    normalized_answer = " ".join(answer.split())
    accepted = {" ".join(value.casefold().split()) for value in item["accepted"]}
    correct = normalized_answer in accepted
    progress = state["progress"]
    progress["attempted"] += 1
    if correct:
        progress["correct"] += 1
    area = progress["areas"].setdefault(item["topic"], {"attempted": 0, "correct": 0})
    area["attempted"] += 1
    if correct:
        area["correct"] += 1
    state["progress"] = progress
    state["active_question"] = None
    save_learner_state(state)
    return jsonify(
        {
            "correct": correct,
            "correct_answer": item["answer"],
            "hint": item["hint"],
            "explanation": item["explanation"],
            "progress": progress,
        }
    )


@learner.get("/progress")
def progress():
    return jsonify(get_learner_state()["progress"])


@learner.post("/reset")
def reset():
    state = get_learner_state()
    state["progress"] = {"attempted": 0, "correct": 0, "areas": {}}
    state["active_question"] = None
    save_learner_state(state)
    return jsonify(state["progress"])
