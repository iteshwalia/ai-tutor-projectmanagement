"""Health-check endpoint."""

from flask import Blueprint, jsonify

health = Blueprint("health", __name__)


@health.get("/healthz")
def health_check():
    return jsonify({"status": "ok"})
