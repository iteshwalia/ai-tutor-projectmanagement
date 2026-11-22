async function requestJSON(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || `Request failed with status ${response.status}`);
  }
  return data;
}

function postJSON(url, body) {
  return requestJSON(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

export const tutorAPI = {
  chat: message => postJSON("/api/chat", { message }),
  question: () => requestJSON("/api/question"),
  evaluate: answer => postJSON("/api/evaluate", { answer }),
  status: () => requestJSON("/api/status"),
};

export const learnerAPI = {
  getProfile: () => requestJSON("/api/profile"),
  saveProfile: profile => postJSON("/api/profile", profile),
  getProgress: () => requestJSON("/api/progress"),
  reset: () => postJSON("/api/reset", {}),
};
