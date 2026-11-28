import { tutorAPI } from "./api.js";
import { addMessage, escapeHTML, removeElement, showTyping } from "./dom.js";
import { state } from "./state.js";
import { updateSummary, updateWeekly } from "./progress.js";

const MAX_QUIZ_QUESTIONS = 20;

export async function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  input.style.height = "38px";
  document.getElementById("suggestions")?.remove();
  addMessage("user", escapeHTML(message));

  if (state.awaitingQuizCount) {
    const count = parseQuizQuestionCount(message);
    if (count === null) {
      addMessage(
        "assistant",
        `<p>Please enter a whole number from 1 to ${MAX_QUIZ_QUESTIONS}.</p>`,
      );
      return;
    }
    state.awaitingQuizCount = false;
    state.activeQuiz = { total: count, answered: 0, correct: 0 };
    await requestQuestion();
    return;
  }

  if (state.awaitingAnswer) {
    await submitAnswer(message);
    return;
  }

  if (state.activeQuiz) {
    await requestQuestion();
    return;
  }

  const typing = showTyping();
  try {
    if (/practice|quiz|challenge|question|scenario/i.test(message)) {
      state.mode = /quiz|test me/i.test(message)
        ? "quiz"
        : /challenge/i.test(message)
          ? "challenge"
          : "practice";
      removeElement(typing);
      if (state.mode === "quiz") {
        state.awaitingQuizCount = true;
        addMessage(
          "assistant",
          `<p>How many questions would you like in this quiz? Enter a number from 1 to ${MAX_QUIZ_QUESTIONS}.</p>`,
        );
        return;
      }
      await requestQuestion();
      return;
    }
    const result = await tutorAPI.chat(message);
    removeElement(typing);
    addMessage("assistant", escapeHTML(result.reply).replace(/\n/g, "<br>"));
  } catch (error) {
    removeElement(typing);
    addMessage("assistant", `<p>I couldn’t reach the tutor service. ${escapeHTML(error.message)} Please try again.</p>`);
  }
}

function parseQuizQuestionCount(value) {
  const match = value.match(/^\s*(\d+)(?:\s+questions?)?\s*$/i);
  const count = match ? Number(match[1]) : NaN;
  return Number.isInteger(count) && count >= 1 && count <= MAX_QUIZ_QUESTIONS
    ? count
    : null;
}

async function requestQuestion() {
  const typing = showTyping();
  try {
    const question = await tutorAPI.question();
    removeElement(typing);
    state.awaitingAnswer = question;
    const quizNumber = state.activeQuiz
      ? ` ${state.activeQuiz.answered + 1} of ${state.activeQuiz.total}`
      : "";
    const modeLabel = state.activeQuiz || state.mode === "quiz" ? "Quiz" : "Practice";
    const choices = question.choices.map((choice, index) =>
      `<li><strong>${String.fromCharCode(65 + index)}.</strong> ${escapeHTML(choice)}</li>`
    ).join("");
    addMessage(
      "assistant",
      `<p><strong>${modeLabel} question${quizNumber} · ` +
      `${escapeHTML(question.difficulty)} level</strong></p>` +
      `<p>${escapeHTML(question.question)}</p><ul>${choices}</ul>` +
      "<p><small>Reply with your answer.</small></p>",
    );
  } catch (error) {
    removeElement(typing);
    addMessage(
      "assistant",
      `<p>I couldn’t load the question. ${escapeHTML(error.message)} Please try again.</p>`,
    );
  }
}

async function submitAnswer(answer) {
  const typing = showTyping();
  try {
    const result = await tutorAPI.evaluate(answer);
    removeElement(typing);
    const feedback = result.correct
      ? `<div class="feedback correct"><p><strong>Correct — excellent work.</strong></p><p>${escapeHTML(result.explanation)}</p></div>`
      : `<div class="feedback incorrect"><p><strong>Not quite — good attempt.</strong></p>` +
        `<p><strong>Hint:</strong> ${escapeHTML(result.hint)}</p>` +
        `<p><strong>Correct answer:</strong> ${escapeHTML(result.correct_answer)}</p>` +
        `<p>${escapeHTML(result.explanation)}</p><p>Keep going; you can try another practice question.</p></div>`;
    const feedbackWithGuidance = feedback.replace(
      "</div>",
      `<p><strong>Personalized feedback:</strong> ${escapeHTML(result.personalized_feedback)}</p>` +
      `<p><strong>Tip &amp; best practice:</strong> ${escapeHTML(result.best_practice)}</p></div>`,
    );
    addMessage("assistant", feedbackWithGuidance);
    Object.assign(state, result.progress);
    const quiz = state.activeQuiz;
    if (quiz) {
      quiz.answered += 1;
      if (result.correct) quiz.correct += 1;
    }
    state.awaitingAnswer = null;
    updateSummary();
    updateWeekly();
    if (quiz && quiz.answered === quiz.total) {
      const percentage = Math.round((quiz.correct / quiz.total) * 100);
      addMessage(
        "assistant",
        `<div class="quiz-score-report" role="status">` +
        "<h3>Quiz score report</h3>" +
        `<p>Questions answered: ${quiz.total}</p>` +
        `<p>Correct answers: ${quiz.correct} of ${quiz.total}</p>` +
        `<p>Score: ${percentage}%</p></div>`,
      );
      state.activeQuiz = null;
      return;
    }
    if (quiz) await requestQuestion();
  } catch (error) {
    removeElement(typing);
    addMessage("assistant", `<p>I couldn’t evaluate that answer. ${escapeHTML(error.message)}</p>`);
  }
}

export function bindChatEvents() {
  const input = document.getElementById("messageInput");
  document.getElementById("sendButton").addEventListener("click", sendMessage);
  input.addEventListener("keydown", event => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });
  input.addEventListener("input", event => {
    event.target.style.height = "38px";
    event.target.style.height = `${Math.min(event.target.scrollHeight, 100)}px`;
  });
  document.querySelectorAll(".suggestion-card").forEach(card => {
    card.addEventListener("click", () => {
      input.value = card.dataset.prompt;
      sendMessage();
    });
  });
}
