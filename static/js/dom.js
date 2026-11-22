export function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  })[char]);
}

export function scrollChat() {
  const chatScroll = document.getElementById("chatScroll");
  requestAnimationFrame(() => {
    chatScroll.scrollTop = chatScroll.scrollHeight;
  });
}

export function addMessage(role, html) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role === "user" ? "user-message" : "assistant-message"}`;
  wrapper.innerHTML = role === "user"
    ? `<div class="message-body"><div class="message-meta"><span>Just now</span><strong>You</strong></div><div class="bubble">${html}</div></div>`
    : `<div class="message-avatar">PM</div><div class="message-body"><div class="message-meta"><strong>PM Mentor</strong><span>Just now</span></div><div class="bubble">${html}</div></div>`;
  document.getElementById("chatContent").appendChild(wrapper);
  scrollChat();
  return wrapper;
}

export function showTyping() {
  return addMessage("assistant", "<div class=\"typing\"><i></i><i></i><i></i></div>");
}

export function removeElement(element) {
  element?.remove();
}

export function openModal(id) {
  const modal = document.getElementById(id);
  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
}

export function closeModal(id) {
  const modal = document.getElementById(id);
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

export function bindModalEvents() {
  document.querySelectorAll(".modal-close").forEach(button => {
    button.addEventListener("click", () => closeModal(button.dataset.close));
  });
  document.querySelectorAll(".modal-backdrop").forEach(backdrop => {
    backdrop.addEventListener("click", event => {
      if (event.target === backdrop) closeModal(backdrop.id);
    });
  });
}
