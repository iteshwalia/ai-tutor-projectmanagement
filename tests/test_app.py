import json
import os
import sqlite3
import tempfile
import unittest
from contextlib import closing
from http.cookies import SimpleCookie
from unittest.mock import MagicMock, patch

from flask.sessions import SecureCookieSessionInterface

from app import create_app


class TutorApplicationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "DATABASE": os.path.join(self.temp_dir.name, "test.sqlite3"),
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def get_pert_question(self):
        with patch(
            "backend.routes.learner.random.choice",
            side_effect=lambda choices: next(
                item for item in choices if item["answer"] == "6 days"
            ),
        ):
            return self.client.get("/api/question")

    def test_home_and_health_endpoints(self):
        home = self.client.get("/")
        self.assertEqual(home.status_code, 200)
        self.assertIn(b'type="module" src="/static/js/app.js"', home.data)
        entrypoint = self.client.get("/static/js/app.js")
        self.assertEqual(entrypoint.status_code, 200)
        self.assertIn("javascript", entrypoint.content_type)
        chat_module = self.client.get("/static/js/chat.js")
        self.assertEqual(chat_module.status_code, 200)
        self.assertIn(b"tutorAPI", chat_module.data)
        self.assertEqual(self.client.get("/healthz").json, {"status": "ok"})

    def test_chat_uses_demo_without_provider_key(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post("/api/chat", json={"message": "Explain the critical path"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["source"], "demo")
        self.assertIn("longest sequence", response.json["reply"])

    def test_chat_rejects_empty_or_non_string_message(self):
        self.assertEqual(self.client.post("/api/chat", json={}).status_code, 400)
        self.assertEqual(
            self.client.post("/api/chat", json={"message": ["not", "text"]}).status_code,
            400,
        )

    def test_question_and_answer_update_progress(self):
        question = self.get_pert_question()
        self.assertEqual(question.status_code, 200)
        self.assertNotIn("answer", question.json)
        self.assertNotIn("accepted", question.json)
        answer = self.client.post("/api/evaluate", json={"answer": "6 days"})
        self.assertEqual(answer.status_code, 200)
        self.assertTrue(answer.json["correct"])
        self.assertEqual(answer.json["progress"]["attempted"], 1)
        self.assertEqual(answer.json["progress"]["correct"], 1)

    def test_answer_matching_does_not_accept_substrings(self):
        self.get_pert_question()
        answer = self.client.post("/api/evaluate", json={"answer": "not 6"})
        self.assertEqual(answer.status_code, 200)
        self.assertFalse(answer.json["correct"])

    def test_evaluation_requires_active_question_and_answer(self):
        self.assertEqual(self.client.post("/api/evaluate", json={"answer": "6"}).status_code, 400)
        self.client.get("/api/question")
        self.assertEqual(self.client.post("/api/evaluate", json={"answer": ""}).status_code, 400)

    def test_profile_only_accepts_known_options(self):
        response = self.client.post(
            "/api/profile",
            json={
                "name": "  Sam  ",
                "level": "Root",
                "difficulty": "Advanced",
                "topic": ["invalid"],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Sam")
        self.assertEqual(response.json["level"], "Intermediate")
        self.assertEqual(response.json["difficulty"], "Advanced")
        self.assertEqual(response.json["topic"], "Project Planning & Scheduling")
        persisted_profile = self.client.get("/api/profile")
        self.assertEqual(persisted_profile.json["name"], "Sam")

    def test_default_profile_uses_itesh_and_migrates_legacy_placeholder(self):
        self.assertEqual(self.client.get("/api/profile").json["name"], "Itesh")
        with self.client.session_transaction() as browser_session:
            browser_session["learner_id"] = "legacy-profile"
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            connection.execute(
                """
                INSERT INTO learner_sessions (
                    session_id, profile_json, progress_json, active_question_json
                ) VALUES (?, ?, ?, NULL)
                """,
                (
                    "legacy-profile",
                    json.dumps(
                        {
                            "name": "Alex Morgan",
                            "level": "Intermediate",
                            "difficulty": "Intermediate",
                            "topic": "Project Planning & Scheduling",
                        }
                    ),
                    json.dumps({"attempted": 0, "correct": 0, "areas": {}}),
                ),
            )
            connection.commit()
        response = self.client.get("/api/profile")
        self.assertEqual(response.json["name"], "Itesh")
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            migrated_profile = json.loads(
                connection.execute(
                    "SELECT profile_json FROM learner_sessions WHERE session_id = ?",
                    ("legacy-profile",),
                ).fetchone()[0]
            )
        self.assertEqual(migrated_profile["name"], "Itesh")

    def test_expanded_cpmai_question_accepts_natural_answer(self):
        self.client.post(
            "/api/profile",
            json={"topic": "CPMAI - AI Project Management"},
        )
        question = self.client.get("/api/question")
        self.assertEqual(question.json["topic"], "CPMAI - AI Project Management")
        self.assertIn("data readiness", question.json["question"].lower())
        answer = self.client.post(
            "/api/evaluate",
            json={
                "answer": (
                    "To verify that suitable, sufficient, and usable data is available"
                )
            },
        )
        self.assertTrue(answer.json["correct"])

    def test_demo_knowledge_includes_data_readiness(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post("/api/chat", json={"message": "What is data readiness?"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("available, relevant", response.json["reply"])

    def test_reset_clears_session_progress(self):
        self.client.get("/api/question")
        self.client.post("/api/evaluate", json={"answer": "6"})
        response = self.client.post("/api/reset")
        self.assertEqual(response.json, {"attempted": 0, "correct": 0, "areas": {}})

    def test_status_reports_configured_model_provider_without_secret(self):
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "test-secret-token",
                "OPENAI_MODEL": "test-model",
            },
            clear=True,
        ):
            response = self.client.get("/api/status")
        self.assertEqual(response.json["provider"], "OpenAI-compatible")
        self.assertEqual(response.json["model"], "test-model")
        self.assertNotIn("test-secret-token", json.dumps(response.json))

    def test_status_reports_gemini_provider_without_secret(self):
        with patch.dict(
            os.environ,
            {
                "GEMINI_API_KEY": "test-gemini-secret",
                "OPENAI_API_KEY": "test-openai-secret",
            },
            clear=True,
        ):
            response = self.client.get("/api/status")
        self.assertEqual(response.json["provider"], "Google Gemini")
        self.assertEqual(response.json["key_name"], "GEMINI_API_KEY")
        self.assertEqual(response.json["model"], "gemini-3.5-flash-lite")
        self.assertNotIn("test-gemini-secret", json.dumps(response.json))
        self.assertNotIn("test-openai-secret", json.dumps(response.json))

    def test_chat_forwards_message_to_configured_model(self):
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "A model-generated explanation."}}]}
        ).encode()
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-token"}, clear=True),
            patch("backend.services.tutor.request.urlopen", return_value=mock_response) as urlopen,
        ):
            response = self.client.post("/api/chat", json={"message": "Explain the critical path"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["source"], "ai")
        self.assertEqual(response.json["reply"], "A model-generated explanation.")
        forwarded_request = urlopen.call_args.args[0]
        self.assertEqual(forwarded_request.headers["Authorization"], "Bearer test-token")
        self.assertEqual(
            json.loads(forwarded_request.data)["messages"][-1]["content"],
            "Explain the critical path",
        )

    def test_chat_uses_gemini_defaults_without_sending_learner_name(self):
        mock_response = MagicMock()
        mock_response.__enter__.return_value.read.return_value = json.dumps(
            {"choices": [{"message": {"content": "Gemini tutor reply."}}]}
        ).encode()
        with (
            patch.dict(os.environ, {"GEMINI_API_KEY": "test-gemini-token"}, clear=True),
            patch("backend.services.tutor.request.urlopen", return_value=mock_response) as urlopen,
        ):
            response = self.client.post("/api/chat", json={"message": "Explain project scope"})

        self.assertEqual(response.status_code, 200)
        forwarded_request = urlopen.call_args.args[0]
        payload = json.loads(forwarded_request.data)
        self.assertEqual(
            forwarded_request.full_url,
            "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        )
        self.assertEqual(payload["model"], "gemini-3.5-flash-lite")
        self.assertNotIn("Itesh", payload["messages"][0]["content"])

    def test_chat_rejects_non_https_provider_urls(self):
        with (
            patch.dict(
                os.environ,
                {
                    "OPENAI_API_KEY": "test-token",
                    "OPENAI_API_URL": "http://example.test/chat",
                },
                clear=True,
            ),
            patch("backend.services.tutor.request.urlopen") as urlopen,
        ):
            response = self.client.post("/api/chat", json={"message": "Explain the critical path"})
        self.assertEqual(response.status_code, 503)
        urlopen.assert_not_called()

    def test_secure_cookie_and_security_headers(self):
        app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret",
                "DATABASE": os.path.join(self.temp_dir.name, "secure.sqlite3"),
                "SESSION_COOKIE_SECURE": True,
            }
        )
        response = app.test_client().get("/api/progress")
        self.assertIn("Secure", response.headers["Set-Cookie"])
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertIn("Strict-Transport-Security", response.headers)

    def test_cookie_contains_only_opaque_session_id(self):
        response = self.client.get("/api/question")
        cookie = SimpleCookie()
        cookie.load(response.headers["Set-Cookie"])
        session_cookie = cookie["session"].value
        serializer = SecureCookieSessionInterface().get_signing_serializer(self.app)
        decoded_session = serializer.loads(session_cookie)
        self.assertEqual(set(decoded_session), {"learner_id"})
        self.assertNotIn("answer", response.get_data(as_text=True))

    def test_production_requires_secret_key(self):
        with patch.dict(os.environ, {"FLASK_ENV": "production"}, clear=True):
            with self.assertRaises(RuntimeError):
                create_app()


if __name__ == "__main__":
    unittest.main()
