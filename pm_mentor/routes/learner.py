"""Learner profile, practice, and progress API routes."""

import random
import re
from datetime import datetime

from flask import Blueprint, current_app, jsonify, make_response
from flask import request as flask_request

from pm_mentor.learner_repository import get_learner_state, save_learner_state
from pm_mentor.learning_content import (
    LEVELS,
    QUESTION_BANK,
    TOPIC_BEST_PRACTICES,
    TOPICS,
)
from pm_mentor.services.tutor import generate_model_question, public_provider_status

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
    if public_provider_status()["api_configured"]:
        item, error, status = generate_model_question(
            profile,
            current_app.config["ENVIRONMENT"] == "production",
        )
        if error:
            return jsonify({"error": error, "source": "ai"}), status
    else:
        matching = [
            item
            for item in QUESTION_BANK
            if item["topic"] == profile["topic"]
            and item["difficulty"] == profile["difficulty"]
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
    correct = _answer_is_correct(normalized_answer, item)
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
    topic_attempted = area["attempted"]
    topic_accuracy = round(area["correct"] / topic_attempted * 100)
    profile = state["profile"]
    return jsonify(
        {
            "correct": correct,
            "correct_answer": item["answer"],
            "hint": item["hint"],
            "explanation": item["explanation"],
            "personalized_feedback": _personalized_feedback(
                profile,
                item["topic"],
                item["difficulty"],
                correct,
                topic_attempted,
                topic_accuracy,
            ),
            "best_practice": TOPIC_BEST_PRACTICES[item["topic"]],
            "progress": progress,
        }
    )


def _answer_is_correct(answer, item):
    accepted = {" ".join(value.casefold().split()) for value in item["accepted"]}
    if answer in accepted:
        return True

    match = re.fullmatch(r"(?:option\s*)?([a-d])\.?", answer)
    if not match:
        return False

    choice_index = ord(match.group(1)) - ord("a")
    choices = item["choices"]
    if choice_index >= len(choices):
        return False

    selected_choice = " ".join(choices[choice_index].casefold().split())
    correct_choice = " ".join(item["answer"].casefold().split())
    return selected_choice == correct_choice


def _personalized_feedback(profile, topic, difficulty, correct, topic_attempted, topic_accuracy):
    first_name = profile["name"].split()[0] or "Learner"
    if correct:
        progress_note = (
            f"This is your first result in {topic}."
            if topic_attempted == 1
            else (
                f"Your {topic} accuracy is now {topic_accuracy}% across "
                f"{topic_attempted} questions."
            )
        )
        next_step = (
            f"At {difficulty} level, deepen your reasoning by considering why the other options "
            "are less suitable."
        )
        opening = "Correct"
    else:
        progress_note = (
            f"This is your first question in {topic}."
            if topic_attempted == 1
            else (
                f"Your current {topic} accuracy is {topic_accuracy}% across "
                f"{topic_attempted} questions."
            )
        )
        next_steps = {
            "Beginner": "restate the core idea in your own words",
            "Intermediate": "compare each option against the scenario's constraints",
            "Advanced": "check the assumptions and downstream trade-offs before choosing",
        }
        next_step = f"At {difficulty} level, for another try, {next_steps[difficulty]}."
        opening = "Good attempt"

    return f"{opening}, {first_name}. {progress_note} {next_step}"


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
