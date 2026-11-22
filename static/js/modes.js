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
      const prompts = {
        learn: `Explain ${state.topic} in simple terms and use a professional workplace example`,
        practice: `Give me a practice question on ${state.topic}`,
        quiz: "Start a short PMP-style quiz",
        challenge: `Give me a ${state.difficulty}-level challenge scenario on ${state.topic}`,
      };
      document.getElementById("messageInput").value = prompts[state.mode];
    });
  });
}
