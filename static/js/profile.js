import { learnerAPI, tutorAPI } from "./api.js";
import { addMessage, closeModal, escapeHTML, openModal } from "./dom.js";
import { state } from "./state.js";

export function updateProfileUI() {
  const firstName = state.name.split(" ")[0] || "Learner";
  const initial = firstName.charAt(0).toUpperCase();
  document.getElementById("profileName").textContent = state.name;
  document.getElementById("profileLevel").textContent = `${state.level} learner`;
  document.getElementById("profileDifficulty").textContent =
    `${state.difficulty} difficulty`;
  document.getElementById("avatarInitial").textContent = initial;
  document.getElementById("topAvatar").textContent = initial;
  document.getElementById("welcomeName").textContent = firstName;
  document.getElementById("currentTopic").textContent = state.topic;
  document.getElementById("initialMessage").innerHTML =
    `Today, let's work through <strong>${escapeHTML(state.topic)}</strong>. ` +
    "I’ll start with a clear explanation, then we can practice it through a real-world scenario.";
}

export async function loadProfile() {
  Object.assign(state, await learnerAPI.getProfile());
  document.getElementById("nameInput").value = state.name;
  document.getElementById("levelInput").value = state.level;
  document.getElementById("difficultyInput").value = state.difficulty;
  document.getElementById("topicInput").value = state.topic;
  updateProfileUI();
}

async function saveProfile(event) {
  event.preventDefault();
  const saveButton = document.querySelector("#profileForm button[type='submit']");
  const saveStatus = document.getElementById("profileSaveStatus");
  const profile = {
    name: document.getElementById("nameInput").value.trim() || "Learner",
    level: document.getElementById("levelInput").value,
    difficulty: document.getElementById("difficultyInput").value,
    topic: document.getElementById("topicInput").value,
  };
  saveButton.disabled = true;
  saveButton.textContent = "Saving…";
  saveStatus.hidden = true;
  saveStatus.textContent = "";
  saveStatus.setAttribute("role", "status");
  saveStatus.setAttribute("aria-live", "polite");
  try {
    Object.assign(state, await learnerAPI.saveProfile(profile));
  } catch {
    saveStatus.textContent = "Could not save your profile. Check your connection and try again.";
    saveStatus.hidden = false;
    saveStatus.setAttribute("role", "alert");
    saveStatus.setAttribute("aria-live", "assertive");
    return;
  } finally {
    saveButton.disabled = false;
    saveButton.textContent = "Save profile";
  }
  updateProfileUI();
  closeModal("profileModal");
  addMessage(
    "assistant",
    `<p>Your profile is updated, ${escapeHTML(state.name.split(" ")[0])}. ` +
    `We’ll use <strong>${escapeHTML(state.topic)}</strong> at ` +
    `<strong>${escapeHTML(state.difficulty)}</strong> level.</p>`,
  );
}

export async function loadAIStatus() {
  try {
    const status = await tutorAPI.status();
    const statusText = document.querySelector(".composer-footer span");
    if (statusText) {
      const source = status.api_configured
        ? `${escapeHTML(status.provider)} · ${escapeHTML(status.model)}`
        : "Demo tutor · no model API key";
      statusText.innerHTML = `<span class="status-dot"></span> ${source}`;
    }

    const settingsBody = document.querySelector("#settingsModal .settings-content");
    const panel = document.createElement("div");
    panel.id = "aiStatusPanel";
    panel.style.cssText =
      "border:1px solid #dde4ed;border-radius:8px;background:#f8fafc;padding:10px;font-size:11px;color:#5f6b7c;";
    panel.innerHTML =
      `<strong>Current response source:</strong> ${escapeHTML(status.provider)}<br>` +
      `<strong>API key variable:</strong> ${escapeHTML(status.key_name)}<br>` +
      `<strong>Model:</strong> ${escapeHTML(status.model)}`;
    settingsBody.prepend(panel);
  } catch {
    // The tutor UI remains usable if the optional provider status is unavailable.
  }
}

export function bindProfileEvents() {
  document.getElementById("editProfile").addEventListener("click", () => openModal("profileModal"));
  document.getElementById("profileButton").addEventListener("click", () => openModal("profileModal"));
  document.getElementById("topicSelector").addEventListener("click", () => openModal("profileModal"));
  document.getElementById("profileForm").addEventListener("submit", saveProfile);
}
