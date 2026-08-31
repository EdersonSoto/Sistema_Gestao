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

loadHealthStatus();
