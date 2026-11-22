import { addMessage, bindModalEvents, closeModal, openModal } from "./dom.js";
import { bindChatEvents } from "./chat.js";
import { bindModeEvents } from "./modes.js";
import { bindProfileEvents, loadAIStatus, loadProfile, updateProfileUI } from "./profile.js";
import { bindProgressEvents, loadProgress, updateWeekly } from "./progress.js";

function bindSettingsEvents() {
  document.getElementById("settingsButton").addEventListener("click", () => {
    openModal("settingsModal");
  });
  document.getElementById("saveSettings").addEventListener("click", () => {
    closeModal("settingsModal");
    addMessage("assistant", "<p>The tutor is ready. Server-side API settings are used automatically when configured.</p>");
  });
}

function showLoadError(message) {
  addMessage("assistant", `<p>${message}</p>`);
}

bindChatEvents();
bindModeEvents();
bindProfileEvents();
bindProgressEvents();
bindModalEvents();
bindSettingsEvents();
updateProfileUI();
updateWeekly();

Promise.all([loadAIStatus(), loadProgress(), loadProfile()]).catch(() => {
  showLoadError("Some learner data could not be loaded from the server. Refresh the page to retry.");
});
