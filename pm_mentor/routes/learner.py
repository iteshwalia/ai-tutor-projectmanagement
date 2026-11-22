"""Learner profile, practice, and progress API routes."""

import random
from datetime import datetime

from flask import Blueprint, jsonify, make_response
from flask import request as flask_request

from pm_mentor.learner_repository import get_learner_state, save_learner_state
from pm_mentor.learning_content import LEVELS, QUESTION_BANK, TOPICS

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
    matching = [
        item
        for item in QUESTION_BANK
        if item["topic"] == profile["topic"] and item["difficulty"] == profile["difficulty"]
    ]
    item = random.choice(matching)
    state["active_question"] = item
    save_learner_state(state)
    return jsonify(
        {
            "topic": item["topic"],
            "difficulty": item["difficulty"],
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


@learner.get("/progress/report")
def progress_report():
    state = get_learner_state()
    profile = state["profile"]
    progress = state["progress"]
    attempted = progress["attempted"]
    correct = progress["correct"]
    accuracy = round(correct / attempted * 100) if attempted else 0
    areas = sorted(progress["areas"].items())
    strong = []
    weak = []
    topic_lines = []

    for topic, result in areas:
        topic_attempted = result["attempted"]
        topic_correct = result["correct"]
        topic_accuracy = round(topic_correct / topic_attempted * 100) if topic_attempted else 0
        topic_lines.append(
            f"- {topic}: {topic_correct}/{topic_attempted} correct ({topic_accuracy}%)"
        )
        if topic_attempted and topic_correct / topic_attempted >= 0.7:
            strong.append(topic)
        elif topic_attempted:
            weak.append(topic)

    recommendation = (
        f"{weak[0]} fundamentals and a guided scenario"
        if weak
        else f"{profile['topic']} fundamentals and an applied challenge"
    )
    strong_lines = [f"- {topic}" for topic in strong] or [
        "- Keep practicing to build insights."
    ]
    weak_lines = [f"- {topic}" for topic in weak] or [
        "- No priority areas identified yet."
    ]
    report_lines = [
        "PM Mentor - Learning Progress Report",
        f"Generated: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
        f"Learner: {' '.join(profile['name'].split())}",
        f"Focus topic: {profile['topic']}",
        f"Selected difficulty: {profile['difficulty']}",
        "",
        "Overall performance",
        f"Questions attempted: {attempted}",
        f"Correct answers: {correct}",
        f"Accuracy: {accuracy}%",
        "",
        "Topic breakdown",
        *(topic_lines or ["- No practice questions completed yet."]),
        "",
        "Strong areas",
        *strong_lines,
        "",
        "Needs practice",
        *weak_lines,
        "",
        f"Recommended next lesson: {recommendation}",
    ]
    response = make_response("\n".join(report_lines) + "\n")
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    response.headers["Content-Disposition"] = (
        'attachment; filename="pm-mentor-progress-report.txt"'
    )
    response.headers["Cache-Control"] = "no-store"
    return response


@learner.post("/reset")
def reset():
    state = get_learner_state()
    state["progress"] = {"attempted": 0, "correct": 0, "areas": {}}
    state["active_question"] = None
    save_learner_state(state)
    return jsonify(state["progress"])
