const state = {
  dashboard: null,
  selectedId: null,
};

const els = {
  status: document.querySelector("#status"),
  minScore: document.querySelector("#minScore"),
  refreshBtn: document.querySelector("#refreshBtn"),
  runDemoBtn: document.querySelector("#runDemoBtn"),
  generatedAt: document.querySelector("#generatedAt"),
  opportunityList: document.querySelector("#opportunityList"),
  emptyState: document.querySelector("#emptyState"),
  detailContent: document.querySelector("#detailContent"),
  detailTitle: document.querySelector("#detailTitle"),
  detailStatus: document.querySelector("#detailStatus"),
  kpiOpportunities: document.querySelector("#kpiOpportunities"),
  kpiTopScore: document.querySelector("#kpiTopScore"),
  kpiAverageScore: document.querySelector("#kpiAverageScore"),
  kpiReady: document.querySelector("#kpiReady"),
  scoreBars: document.querySelector("#scoreBars"),
  seoSubtitle: document.querySelector("#seoSubtitle"),
  keywordTags: document.querySelector("#keywordTags"),
  seoBullets: document.querySelector("#seoBullets"),
  chapterList: document.querySelector("#chapterList"),
  positioning: document.querySelector("#positioning"),
  launchTasks: document.querySelector("#launchTasks"),
  publicationChecklist: document.querySelector("#publicationChecklist"),
  protocolTruth: document.querySelector("#protocolTruth"),
  protocolCadence: document.querySelector("#protocolCadence"),
  protocolChannels: document.querySelector("#protocolChannels"),
  decisionPacket: document.querySelector("#decisionPacket"),
};

els.refreshBtn.addEventListener("click", () => loadDashboard());
els.minScore.addEventListener("change", () => loadDashboard());
els.runDemoBtn.addEventListener("click", () => runDemo());

loadDashboard();

async function loadDashboard() {
  setBusy(true, "Loading dashboard...");
  try {
    const minScore = Number(els.minScore.value || 0);
    const response = await fetch(`/api/dashboard?min_score=${encodeURIComponent(minScore)}`);
    if (!response.ok) {
      throw new Error(`Dashboard failed with HTTP ${response.status}`);
    }
    const dashboard = await response.json();
    state.dashboard = dashboard;
    state.selectedId = state.selectedId || dashboard.items?.[0]?.opportunity?.id || null;
    render();
    setStatus(`Updated ${formatDate(dashboard.generated_at)}`);
  } catch (error) {
    setError(error.message);
  } finally {
    setBusy(false);
  }
}

async function runDemo() {
  setBusy(true, "Running opportunity demo...");
  try {
    const response = await fetch("/api/run-demo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    if (!response.ok) {
      throw new Error(`Demo failed with HTTP ${response.status}`);
    }
    state.dashboard = await response.json();
    state.selectedId = state.dashboard.items?.[0]?.opportunity?.id || null;
    render();
    setStatus("Demo completed and dashboard refreshed.");
  } catch (error) {
    setError(error.message);
  } finally {
    setBusy(false);
  }
}

function render() {
  const dashboard = state.dashboard || {};
  const items = dashboard.items || [];
  const kpis = dashboard.kpis || {};

  els.kpiOpportunities.textContent = kpis.opportunities ?? 0;
  els.kpiTopScore.textContent = formatScore(kpis.top_score ?? 0);
  els.kpiAverageScore.textContent = formatScore(kpis.average_score ?? 0);
  els.kpiReady.textContent = kpis.ready_for_review ?? 0;
  els.generatedAt.textContent = dashboard.generated_at ? formatDate(dashboard.generated_at) : "";

  renderOpportunityList(items);
  renderProtocol(dashboard.ceo_cto_protocol || {});

  const selected = items.find((item) => item.opportunity.id === state.selectedId) || items[0];
  if (selected) {
    state.selectedId = selected.opportunity.id;
    renderDetail(selected);
  } else {
    renderEmpty();
  }
}

function renderOpportunityList(items) {
  els.opportunityList.innerHTML = "";
  if (!items.length) {
    els.opportunityList.innerHTML =
      '<div class="empty-state">No hay oportunidades. Ejecuta la demo para crear datos.</div>';
    return;
  }

  for (const item of items) {
    const opportunity = item.opportunity;
    const button = document.createElement("button");
    button.type = "button";
    button.className = `opportunity-button ${opportunity.id === state.selectedId ? "active" : ""}`;
    button.innerHTML = `
      <span class="opportunity-title">${escapeHtml(opportunity.title_angle)}</span>
      <span class="opportunity-meta">
        <span>${escapeHtml(opportunity.audience)}</span>
        <span class="score-pill">${formatScore(opportunity.total_score)}</span>
      </span>
    `;
    button.addEventListener("click", () => {
      state.selectedId = opportunity.id;
      render();
    });
    els.opportunityList.appendChild(button);
  }
}

function renderDetail(item) {
  const opportunity = item.opportunity;
  els.emptyState.classList.add("hidden");
  els.detailContent.classList.remove("hidden");
  els.detailTitle.textContent = opportunity.title_angle;
  els.detailStatus.textContent = `${opportunity.status} | ${opportunity.id}`;

  renderScores(opportunity);
  renderSeo(item.seo_pack);
  renderChapters(item.structure);
  renderMarketing(item.marketing_plan);
  renderPublication(item.publication);
}

function renderEmpty() {
  els.detailTitle.textContent = "Selecciona una oportunidad";
  els.detailStatus.textContent = "";
  els.emptyState.classList.remove("hidden");
  els.detailContent.classList.add("hidden");
}

function renderScores(opportunity) {
  const rows = [
    ["Total", opportunity.total_score],
    ["Demanda", opportunity.demand_score],
    ["Tendencia", opportunity.trend_score],
    ["Competencia", 100 - opportunity.competition_score],
    ["Margen", opportunity.margin_score],
    ["SEO", opportunity.seo_score],
  ];
  els.scoreBars.innerHTML = rows
    .map(
      ([label, score]) => `
        <div class="score-row">
          <span>${label}</span>
          <span class="bar-track"><span class="bar-fill" style="width:${clamp(score)}%"></span></span>
          <strong>${formatScore(score)}</strong>
        </div>
      `,
    )
    .join("");
}

function renderSeo(seoPack) {
  els.seoSubtitle.textContent = seoPack.subtitle;
  els.keywordTags.innerHTML = seoPack.backend_keywords
    .map((keyword) => `<span class="tag">${escapeHtml(keyword)}</span>`)
    .join("");
  renderList(els.seoBullets, seoPack.description_bullets);
}

function renderChapters(structure) {
  els.chapterList.innerHTML = structure.chapters
    .map(
      (chapter) => `
        <li>
          <strong>${chapter.number}. ${escapeHtml(chapter.title)}</strong><br />
          <span>${escapeHtml(chapter.objective)}</span>
        </li>
      `,
    )
    .join("");
}

function renderMarketing(marketingPlan) {
  els.positioning.textContent = marketingPlan.positioning;
  renderList(els.launchTasks, marketingPlan.launch_tasks);
}

function renderPublication(publication) {
  renderList(els.publicationChecklist, publication.checklist);
}

function renderProtocol(protocol) {
  els.protocolTruth.textContent = protocol.source_of_truth || "";
  els.protocolCadence.textContent = protocol.cadence || "";
  renderList(
    els.protocolChannels,
    (protocol.channels || []).map((channel) => `${channel.name}: ${channel.use}`),
  );
  renderList(els.decisionPacket, protocol.decision_packet || []);
}

function renderList(node, values) {
  node.innerHTML = values.map((value) => `<li>${escapeHtml(value)}</li>`).join("");
}

function setBusy(isBusy, message = "") {
  els.refreshBtn.disabled = isBusy;
  els.runDemoBtn.disabled = isBusy;
  if (message) {
    setStatus(message);
  }
}

function setStatus(message) {
  els.status.classList.remove("error");
  els.status.textContent = message;
}

function setError(message) {
  els.status.classList.add("error");
  els.status.textContent = message;
}

function formatScore(value) {
  return Number(value || 0).toFixed(1);
}

function formatDate(value) {
  return new Intl.DateTimeFormat("es", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function clamp(value) {
  return Math.max(0, Math.min(100, Number(value || 0)));
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

