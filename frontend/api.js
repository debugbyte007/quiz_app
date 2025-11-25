// api.js
const API_BASE = "https://quiz-app-sdc.onrender.com/api";

function $(id) {
  return document.getElementById(id);
}

async function apiRequest(path, method = "GET", body) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  };

  if (body) {
    opts.body = JSON.stringify(body);
  }

  const res = await fetch(`${API_BASE}${path}`, opts);
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.error || "Request failed");
  }

  return data;
}
