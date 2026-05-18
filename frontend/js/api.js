const API_BASE = "http://127.0.0.1:8000";
const SESSION_KEY = "sims.account";
const SESSION_STORE = window.sessionStorage;

function getSession() {
  const raw = SESSION_STORE.getItem(SESSION_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (_) {
    SESSION_STORE.removeItem(SESSION_KEY);
    return null;
  }
}

function saveSession(session) {
  SESSION_STORE.setItem(SESSION_KEY, JSON.stringify(session));
}

function clearSession() {
  SESSION_STORE.removeItem(SESSION_KEY);
}

function getAuthHeaders() {
  const session = getSession();
  if (!session?.username || !session?.password) {
    return {};
  }
  const encoded = btoa(`${session.username}:${session.password}`);
  return { Authorization: `Basic ${encoded}` };
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || "Request failed");
  }
  return data;
}

function requireSession(allowedRoles = ["admin", "employee"]) {
  const session = getSession();
  if (!session) {
    window.location.href = "login.html";
    throw new Error("Please log in first");
  }
  if (allowedRoles.length && !allowedRoles.includes(session.role)) {
    alert("Your account does not have access to this page.");
    window.location.href = "dashboard.html";
    throw new Error("Unauthorized role");
  }
  return session;
}

function setupPage(activePage, options = {}) {
  const session = requireSession(options.allowedRoles || ["admin", "employee"]);
  document.querySelectorAll("[data-nav]").forEach((element) => {
    element.classList.toggle("active", element.dataset.nav === activePage);
  });

  const userLabel = document.getElementById("sessionUser");
  if (userLabel) {
    userLabel.textContent = `${session.username} (${session.role})`;
  }

  document.querySelectorAll("[data-admin-only]").forEach((element) => {
    element.classList.toggle("d-none", session.role !== "admin");
  });

  return session;
}

function logout() {
  clearSession();
  window.location.href = "login.html";
}
