import { tutorAPI } from "./api.js";
import { addMessage, escapeHTML, removeElement, showTyping } from "./dom.js";
import { state } from "./state.js";
import { updateSummary, updateWeekly } from "./progress.js";

export async function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;
  input.value = "";
  input.style.height = "38px";
  document.getElementById("suggestions")?.remove();
  addMessage("user", escapeHTML(message));

  if (state.awaitingAnswer) {
    await submitAnswer(message);
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
      const question = await tutorAPI.question();
      removeElement(typing);
      state.awaitingAnswer = question;
      const choices = question.choices.map((choice, index) =>
        `<li><strong>${String.fromCharCode(65 + index)}.</strong> ${escapeHTML(choice)}</li>`
      ).join("");
      addMessage(
        "assistant",
        `<p><strong>${state.mode === "quiz" ? "Quiz" : "Practice"} question</strong></p>` +
        `<p>${escapeHTML(question.question)}</p><ul>${choices}</ul>` +
        "<p><small>Reply with your answer.</small></p>",
      );
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
    addMessage("assistant", feedback);
    Object.assign(state, result.progress);
    state.awaitingAnswer = null;
    updateSummary();
    updateWeekly();
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
