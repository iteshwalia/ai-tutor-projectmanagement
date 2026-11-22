import { learnerAPI } from "./api.js";
import { addMessage, escapeHTML, openModal } from "./dom.js";
import { state } from "./state.js";

export function updateWeekly() {
  const count = Math.min(state.attempted, 5);
  document.getElementById("weeklyCount").textContent = `${count} / 5`;
  document.getElementById("weeklyProgress").style.width = `${count * 20}%`;
}

export async function loadProgress() {
  Object.assign(state, await learnerAPI.getProgress());
  updateWeekly();
}

export function updateSummary() {
  document.getElementById("attemptedMetric").textContent = state.attempted;
  document.getElementById("correctMetric").textContent = state.correct;
  const accuracy = state.attempted ? Math.round((state.correct / state.attempted) * 100) : 0;
  document.getElementById("accuracyMetric").textContent = `${accuracy}%`;

  const strong = [];
  const weak = [];
  Object.entries(state.areas).forEach(([area, result]) => {
    if (result.attempted && result.correct / result.attempted >= 0.7) strong.push(area);
    if (result.attempted && result.correct / result.attempted < 0.7) weak.push(area);
  });
  document.getElementById("strongAreas").innerHTML = strong.length
    ? strong.map(area => `<span>${escapeHTML(area)}</span>`).join("")
    : "<span>Keep practicing to build insights</span>";
  document.getElementById("weakAreas").innerHTML = weak.length
    ? weak.map(area => `<span>${escapeHTML(area)}</span>`).join("")
    : "<span>Complete a practice question</span>";
  const topicResults = Object.entries(state.areas)
    .sort(([first], [second]) => first.localeCompare(second))
    .map(([topic, result]) => {
      const topicAccuracy = result.attempted
        ? Math.round((result.correct / result.attempted) * 100)
        : 0;
      return `<div class="topic-result"><span>${escapeHTML(topic)}</span>` +
        `<strong>${result.correct}/${result.attempted} · ${topicAccuracy}%</strong></div>`;
    });
  document.getElementById("topicBreakdown").innerHTML = topicResults.length
    ? topicResults.join("")
    : "<span>Complete a practice question to see topic results</span>";
  document.getElementById("recommendationText").textContent = weak[0]
    ? `${weak[0]} fundamentals and a guided scenario`
    : `${state.topic} fundamentals and an applied challenge`;
}

export async function resetProgress() {
  try {
    Object.assign(state, await learnerAPI.reset());
  } catch {
    addMessage("assistant", "<p>I couldn’t reset your progress. Please retry.</p>");
    return;
  }
  state.awaitingAnswer = null;
  updateWeekly();
  const messages = document.querySelectorAll("#chatContent .message");
  messages.forEach((message, index) => {
    if (index > 1) message.remove();
  });
  addMessage("assistant", "<p>Your session has been reset. Choose a learning mode or ask me what you would like to study.</p>");
}

export function bindProgressEvents() {
  document.getElementById("sessionSummary").addEventListener("click", () => {
    updateSummary();
    openModal("summaryModal");
  });
  document.getElementById("resetButton").addEventListener("click", resetProgress);
}
