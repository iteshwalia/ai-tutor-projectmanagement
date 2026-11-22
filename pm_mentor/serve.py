"""Production Waitress entry point for platforms that provide a PORT."""

import os

from waitress import serve

from pm_mentor.application import create_app

if __name__ == "__main__":
    serve(create_app(), host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
