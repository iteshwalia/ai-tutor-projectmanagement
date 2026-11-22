import os
import threading
from collections.abc import Iterator
from unittest.mock import patch

import pytest
from playwright.sync_api import Browser, Page, sync_playwright
from werkzeug.serving import make_server

from app import create_app


@pytest.fixture(scope="session")
def app_url(tmp_path_factory: pytest.TempPathFactory) -> Iterator[str]:
    environment = patch.dict(os.environ, {"GEMINI_API_KEY": "", "OPENAI_API_KEY": ""})
    environment.start()
    server = None
    thread = None
    try:
        database = tmp_path_factory.mktemp("pm-mentor-ui") / "learners.sqlite3"
        app = create_app(
            {
                "SECRET_KEY": "playwright-test-secret",
                "DATABASE": str(database),
            }
        )
        server = make_server("127.0.0.1", 0, app, threaded=True)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        if server:
            server.shutdown()
        if thread:
            thread.join(timeout=5)
        environment.stop()


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser, app_url: str) -> Iterator[Page]:
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    page.route("https://**/*", lambda route: route.abort())
    page.goto(app_url, wait_until="networkidle")
    yield page
    context.close()
