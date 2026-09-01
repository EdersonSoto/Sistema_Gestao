const SESSION_KEY = "gestao_access_token";

function getToken() {
  return sessionStorage.getItem(SESSION_KEY);
}

function showLogin(message = "") {
  document.getElementById("loginView")?.classList.remove("d-none");
  document.getElementById("dashboardView")?.classList.add("d-none");
  const errorEl = document.getElementById("loginError");
  if (errorEl) {
    errorEl.textContent = message;
    errorEl.classList.toggle("d-none", !message);
  }
}

function showDashboard(user) {
  document.getElementById("loginView")?.classList.add("d-none");
  document.getElementById("dashboardView")?.classList.remove("d-none");
  const userEl = document.getElementById("currentUser");
  if (userEl) {
    userEl.textContent = `Usuário: ${user.full_name}`;
  }
}

async function loadHealthStatus() {
  const statusEl = document.getElementById("apiStatus");
  const detailsEl = document.getElementById("apiDetails");

  if (!statusEl || !detailsEl) {
    return;
  }

  try {
    const response = await fetch("/api/health");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    statusEl.textContent = data.status === "ok" ? "API online" : "API com alerta";
    statusEl.classList.remove("text-muted", "text-danger");
    statusEl.classList.add("text-success");
    detailsEl.textContent = `${data.system} - versão ${data.version}`;
  } catch (error) {
    statusEl.textContent = "API offline";
    statusEl.classList.remove("text-muted", "text-success");
    statusEl.classList.add("text-danger");
    detailsEl.textContent = "Não foi possível consultar o backend no momento.";
    console.error("Falha ao carregar o status da API:", error);
  }
}

async function loadCurrentUser() {
  const token = getToken();
  if (!token) {
    showLogin();
    return;
  }

  const response = await fetch("/api/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) {
    sessionStorage.removeItem(SESSION_KEY);
    showLogin("Sua sessão expirou. Entre novamente.");
    return;
  }

  const user = await response.json();
  showDashboard(user);
  loadHealthStatus();
}

async function handleLogin(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const button = document.getElementById("loginButton");
  const errorEl = document.getElementById("loginError");
  const payload = {
    username: form.username.value.trim(),
    password: form.password.value,
  };

  errorEl.classList.add("d-none");
  button.disabled = true;
  button.textContent = "Entrando...";

  try {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(response.status === 401 ? "Usuário ou senha inválidos." : "Não foi possível entrar agora.");
    }

    const data = await response.json();
    sessionStorage.setItem(SESSION_KEY, data.access_token);
    form.reset();
    await loadCurrentUser();
  } catch (error) {
    errorEl.textContent = error.message;
    errorEl.classList.remove("d-none");
  } finally {
    button.disabled = false;
    button.textContent = "Entrar";
  }
}

document.getElementById("loginForm")?.addEventListener("submit", handleLogin);
document.getElementById("logoutButton")?.addEventListener("click", () => {
  sessionStorage.removeItem(SESSION_KEY);
  showLogin();
});

loadCurrentUser().catch(() => showLogin("Não foi possível validar sua sessão."));
