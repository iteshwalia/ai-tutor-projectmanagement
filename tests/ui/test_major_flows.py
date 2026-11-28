import re
from pathlib import Path

from playwright.sync_api import Page, expect

from pm_mentor.learning_content import QUESTION_BANK


def test_home_settings_and_profile_dialog_openers(page: Page) -> None:
    expect(page.get_by_role("heading", name="Welcome back, Itesh")).to_be_visible()
    expect(page.locator("#profileDifficulty")).to_have_text("Intermediate difficulty")
    expect(page.locator("#currentTopic")).to_have_text("Project Planning & Scheduling")

    page.locator("#topicSelector").click()
    profile_modal = page.locator("#profileModal")
    expect(profile_modal).to_have_class(re.compile(r"\bopen\b"))
    page.locator("#profileModal .modal-close").click()
    expect(profile_modal).not_to_have_class(re.compile(r"\bopen\b"))
    expect(page.locator("#topicSelector")).to_be_focused()

    page.locator("#settingsButton").click()
    settings_modal = page.locator("#settingsModal")
    expect(settings_modal).to_have_class(re.compile(r"\bopen\b"))
    expect(settings_modal).to_contain_text("GEMINI_API_KEY")
    page.locator("#saveSettings").click()
    expect(settings_modal).not_to_have_class(re.compile(r"\bopen\b"))


def test_profile_save_failure_and_difficulty_persistence(page: Page) -> None:
    def reject_profile_save(route) -> None:
        if route.request.method == "POST":
            route.fulfill(
                status=503,
                content_type="application/json",
                body='{"error":"test service unavailable"}',
            )
        else:
            route.continue_()

    page.locator("#editProfile").click()
    page.locator("#difficultyInput").select_option("Advanced")
    page.route("**/api/profile", reject_profile_save)
    page.locator("#profileForm button[type='submit']").click()

    status = page.locator("#profileSaveStatus")
    expect(status).to_be_visible()
    expect(status).to_have_text("Could not save your profile. Check your connection and try again.")
    expect(page.locator("#profileModal")).to_have_class(re.compile(r"\bopen\b"))
    expect(page.locator("#profileForm button[type='submit']")).to_be_enabled()

    page.unroute("**/api/profile")
    page.locator("#profileForm button[type='submit']").click()
    expect(page.locator("#profileModal")).not_to_have_class(re.compile(r"\bopen\b"))
    expect(page.locator("#profileDifficulty")).to_have_text("Advanced difficulty")
    expect(page.locator("#editProfile")).to_be_focused()

    page.reload(wait_until="domcontentloaded")
    expect(page.locator("#difficultyInput")).to_have_value("Advanced")
    expect(page.locator("#profileDifficulty")).to_have_text("Advanced difficulty")


def test_learning_modes_use_selected_topic_and_difficulty(page: Page) -> None:
    page.locator("#editProfile").click()
    page.locator("#difficultyInput").select_option("Advanced")
    page.locator("#topicInput").select_option(label="Agile Methodologies")
    page.locator("#profileForm button[type='submit']").click()
    expect(page.locator("#profileModal")).not_to_have_class(re.compile(r"\bopen\b"))

    input_box = page.locator("#messageInput")
    for mode in ("learn", "practice", "quiz", "challenge"):
        page.locator(f'[data-mode="{mode}"]').click()
        prompt = input_box.input_value()
        assert "Advanced" in prompt
        assert "Agile Methodologies" in prompt


def test_chat_practice_quiz_progress_download_and_reset(page: Page, app_url: str) -> None:
    input_box = page.locator("#messageInput")
    input_box.fill("Explain the critical path in simple terms")
    input_box.press("Enter")
    expect(page.locator("#chatContent")).to_contain_text("longest sequence")

    page.locator('[data-mode="quiz"]').click()
    quiz_prompt = input_box.input_value()
    assert "quiz" in quiz_prompt.lower()
    with page.expect_response(lambda response: response.url.endswith("/api/question")) as response:
        page.locator("#sendButton").click()
    quiz_question = response.value.json()
    expect(page.locator("#chatContent")).to_contain_text(
        f"Quiz question · {quiz_question['difficulty']} level"
    )
    page.locator("#messageInput").fill("__intentionally_wrong_answer__")
    with page.expect_response(lambda item: item.url.endswith("/api/evaluate")):
        page.locator("#sendButton").click()
    expect(page.locator("#chatContent")).to_contain_text("Not quite — good attempt.")
    expect(page.locator("#chatContent")).to_contain_text("Hint:")
    expect(page.locator("#chatContent")).to_contain_text("Personalized feedback:")
    expect(page.locator("#chatContent")).to_contain_text("Tip & best practice:")

    page.locator('[data-mode="practice"]').click()
    with page.expect_response(lambda response: response.url.endswith("/api/question")) as response:
        page.locator("#sendButton").click()
    practice_question = response.value.json()
    question_record = next(
        item
        for item in QUESTION_BANK
        if item["question"] == practice_question["question"]
        and item["topic"] == practice_question["topic"]
        and item["difficulty"] == practice_question["difficulty"]
    )
    answer_index = question_record["choices"].index(question_record["answer"])
    answer_letter = chr(ord("a") + answer_index)
    page.locator("#messageInput").fill(f"{answer_letter}.")
    with page.expect_response(lambda item: item.url.endswith("/api/evaluate")):
        page.locator("#sendButton").click()
    expect(page.locator("#chatContent")).to_contain_text("Correct — excellent work.")
    expect(page.locator("#chatContent")).to_contain_text("Personalized feedback:")
    expect(page.locator("#chatContent")).to_contain_text("Tip & best practice:")

    page.locator("#sessionSummary").click()
    summary = page.locator("#summaryModal")
    expect(summary).to_have_class(re.compile(r"\bopen\b"))
    expect(page.locator("#attemptedMetric")).to_have_text("2")
    expect(page.locator("#correctMetric")).to_have_text("1")
    expect(page.locator("#accuracyMetric")).to_have_text("50%")
    expect(page.locator("#topicBreakdown")).to_contain_text(
        "Project Planning & Scheduling"
    )

    with page.expect_download() as download_info:
        page.locator(".report-download").click()
    download = download_info.value
    assert download.suggested_filename == "pm-mentor-progress-report.txt"
    report_path = download.path()
    assert report_path is not None
    report = Path(report_path).read_text(encoding="utf-8")
    assert "Questions attempted: 2" in report
    assert "Correct answers: 1" in report
    assert "Accuracy: 50%" in report

    page.locator("#summaryModal .modal-close").click()
    page.locator("#resetButton").click()
    expect(page.locator("#weeklyCount")).to_have_text("0 / 5")
    expect(page.locator("#chatContent")).to_contain_text("Your session has been reset.")
    progress = page.request.get(f"{app_url}/api/progress").json()
    assert progress == {"attempted": 0, "correct": 0, "areas": {}}

    page.locator("#sessionSummary").click()
    expect(page.locator("#attemptedMetric")).to_have_text("0")
    expect(page.locator("#correctMetric")).to_have_text("0")
    expect(page.locator("#accuracyMetric")).to_have_text("0%")
