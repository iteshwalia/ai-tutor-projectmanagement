"""Flask application factory and production configuration."""

import logging
import os
from os.path import join

from dotenv import load_dotenv
from flask import Flask

from backend.database import init_database
from backend.routes.health import health
from backend.routes.learner import learner
from backend.routes.pages import pages
from backend.routes.tutor import tutor

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))


def create_app(test_config=None):
    app = Flask(__name__)
    is_production = os.getenv("FLASK_ENV", "").lower() == "production"
    secret_key = os.getenv("FLASK_SECRET_KEY")
    if is_production and (
        not secret_key or secret_key == "local-development-only-change-me" or len(secret_key) < 32
    ):
        raise RuntimeError("FLASK_SECRET_KEY must be configured in production.")

    app.config.from_mapping(
        SECRET_KEY=secret_key or "local-development-only-change-me",
        DATABASE=os.getenv("DATABASE_PATH", join(app.instance_path, "pm_mentor.sqlite3")),
        ENVIRONMENT="production" if is_production else "development",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=is_production,
        MAX_CONTENT_LENGTH=16 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    init_database(app)
    register_security_headers(app)
    app.register_blueprint(pages)
    app.register_blueprint(health)
    app.register_blueprint(learner)
    app.register_blueprint(tutor)
    return app


def register_security_headers(app):
    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; script-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
        )
        if app.config["SESSION_COOKIE_SECURE"]:
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        return response


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )
