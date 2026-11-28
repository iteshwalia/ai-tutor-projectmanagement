import { state } from "./state.js";

function setActiveMode(mode) {
  document.querySelectorAll(".mode-button").forEach(button => {
    button.classList.toggle("active", button.dataset.mode === mode);
  });
}

export function bindModeEvents() {
  document.querySelectorAll(".mode-button").forEach(button => {
    button.addEventListener("click", () => {
      state.mode = button.dataset.mode;
      setActiveMode(state.mode);
      const difficultyGuidance = {
        Beginner: "Use plain language, define key terms, and give step-by-step hints.",
        Intermediate: "Use practical workplace examples and explain the main trade-offs.",
        Advanced: "Use complex situations, competing constraints, and fewer hints.",
      }[state.difficulty];
      const prompts = {
        learn: `Explain ${state.topic} at ${state.difficulty} level. ${difficultyGuidance}`,
        practice: `Give me a ${state.difficulty}-level practice question on ${state.topic}`,
        quiz: `Start a ${state.difficulty}-level PMP or PMI-ACP quiz on ${state.topic}`,
        challenge: `Give me a ${state.difficulty}-level challenge scenario on ${state.topic}`,
      };
      document.getElementById("messageInput").value = prompts[state.mode];
    });
  });
}
