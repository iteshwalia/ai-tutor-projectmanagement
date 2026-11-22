"""SQLite persistence for learner profiles, questions, and progress."""

import json
import secrets
import sqlite3
from pathlib import Path

from flask import current_app, g, session


def init_database(app):
    database_path = app.config["DATABASE"]
    if database_path != ":memory:":
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS learner_sessions (
                session_id TEXT PRIMARY KEY,
                profile_json TEXT NOT NULL,
                progress_json TEXT NOT NULL,
                active_question_json TEXT,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    finally:
        connection.close()

    app.teardown_appcontext(close_database)


def close_database(_error=None):
    connection = g.pop("database", None)
    if connection is not None:
        connection.close()


def get_database():
    if "database" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"], timeout=5)
        connection.row_factory = sqlite3.Row
        g.database = connection
    return g.database


def get_learner_state():
    session_id = session.get("learner_id")
    if not isinstance(session_id, str):
        session.clear()
        session_id = secrets.token_urlsafe(32)
        session["learner_id"] = session_id

    row = (
        get_database()
        .execute(
            "SELECT profile_json, progress_json, active_question_json "
            "FROM learner_sessions WHERE session_id = ?",
            (session_id,),
        )
        .fetchone()
    )
    if row is None:
        state = {
            "profile": {
                "name": "Alex Morgan",
                "level": "Intermediate",
                "difficulty": "Intermediate",
                "topic": "Project Planning & Scheduling",
            },
            "progress": {"attempted": 0, "correct": 0, "areas": {}},
            "active_question": None,
        }
        save_learner_state(state)
        return state
    return {
        "profile": json.loads(row["profile_json"]),
        "progress": json.loads(row["progress_json"]),
        "active_question": (
            json.loads(row["active_question_json"]) if row["active_question_json"] else None
        ),
    }


def save_learner_state(state):
    get_database().execute(
        """
        INSERT INTO learner_sessions (
            session_id, profile_json, progress_json, active_question_json, updated_at
        )
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(session_id) DO UPDATE SET
            profile_json = excluded.profile_json,
            progress_json = excluded.progress_json,
            active_question_json = excluded.active_question_json,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            session["learner_id"],
            json.dumps(state["profile"]),
            json.dumps(state["progress"]),
            json.dumps(state["active_question"]) if state["active_question"] else None,
        ),
    )
    get_database().commit()
