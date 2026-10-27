const samples = {
  credible: "Scientists publish a peer-reviewed study showing that regular sleep improves memory in adults. The researchers described the sample size, methods, and limitations in the report.",
  suspicious: "SHOCKING! This secret cure will change your life overnight!!! Experts are hiding the truth. SHARE NOW before they delete this unbelievable story!!!",
  opinion: "In my opinion, the city should invest more money in public transport because it could make daily travel easier for residents."
};

const riskWords = ["shocking", "secret", "miracle", "unbelievable", "exposed", "they don't want", "share now", "overnight", "urgent", "hidden", "guaranteed", "breaking"];
const evidenceWords = ["study", "research", "peer-reviewed", "data", "method", "sample", "report", "according", "source", "published", "evidence", "limitations"];
const input = document.querySelector("#news-input");
const count = document.querySelector("#char-count");

function analyse(text) {
  const lower = text.toLowerCase();
  const tokens = lower.match(/[a-z]+(?:'[a-z]+)?/g) || [];
  const hits = riskWords.filter(word => lower.includes(word));
  const evidence = evidenceWords.filter(word => lower.includes(word));
  const exclamations = (text.match(/!/g) || []).length;
  const capitals = (text.match(/[A-Z]{3,}/g) || []).length;
  const questionMarks = (text.match(/\?/g) || []).length;
  let score = 22;
  score += Math.min(42, hits.length * 8);
  score += Math.min(18, exclamations * 3 + capitals * 4);
  score += questionMarks * 2;
  score -= Math.min(30, evidence.length * 5);
  score = Math.max(2, Math.min(97, score));
  const label = score >= 65 ? "High-risk language" : score >= 38 ? "Needs verification" : "Lower-risk language";
  const description = score >= 65 ? "Several persuasive or sensational patterns were detected. Check the original source before sharing." : score >= 38 ? "The text contains mixed signals. Compare the claim with independent, reliable sources." : "The text contains comparatively few sensational signals, but a language score cannot establish truth.";
  const signals = [];
  if (hits.length) signals.push({ type: "risk", title: "Sensational vocabulary", detail: `${hits.slice(0, 3).join(", ")}${hits.length > 3 ? "…" : ""} detected` });
  if (exclamations || capitals) signals.push({ type: "risk", title: "Emphasis pattern", detail: `${exclamations} exclamation mark${exclamations === 1 ? "" : "s"} · ${capitals} uppercase burst${capitals === 1 ? "" : "s"}` });
  if (evidence.length) signals.push({ type: "good", title: "Evidence language", detail: `${evidence.slice(0, 4).join(", ")} detected` });
  signals.push({ type: "neutral", title: "Text statistics", detail: `${tokens.length} tokens · ${text.split(/[.!?]+/).filter(Boolean).length} sentence${text.split(/[.!?]+/).filter(Boolean).length === 1 ? "" : "s"}` });
  return { score, label, description, signals };
}

function renderLocal() {
  const text = input.value.trim();
  count.textContent = `${input.value.length.toLocaleString()} / 2,000`;
  if (!text) return;
  const result = analyse(text);
  document.querySelector("#score-value").textContent = result.score;
  document.querySelector("#result-label").textContent = result.label;
  document.querySelector("#result-description").textContent = result.description;
  document.querySelector("#confidence-badge").textContent = result.score >= 65 ? "CHECK CAREFULLY" : result.score >= 38 ? "REVIEW" : "LOWER SIGNAL";
  document.querySelector("#score-ring").style.setProperty("--score", `${result.score * 3.6}deg`);
  document.querySelector("#score-ring").dataset.level = result.score >= 65 ? "high" : result.score >= 38 ? "medium" : "low";
  document.querySelector("#signal-list").innerHTML = result.signals.map(signal => `<div class="signal signal-${signal.type}"><span class="signal-icon">${signal.type === "risk" ? "!" : signal.type === "good" ? "✓" : "·"}</span><div><strong>${signal.title}</strong><small>${signal.detail}</small></div></div>`).join("");
}

function renderResult(result) {
  document.querySelector("#score-value").textContent = result.score;
  document.querySelector("#result-label").textContent = result.label;
  document.querySelector("#result-description").textContent = result.description;
  document.querySelector("#confidence-badge").textContent = result.score >= 65 ? "CHECK CAREFULLY" : result.score >= 38 ? "REVIEW" : "LOWER SIGNAL";
  document.querySelector("#score-ring").style.setProperty("--score", `${result.score * 3.6}deg`);
  document.querySelector("#score-ring").dataset.level = result.score >= 65 ? "high" : result.score >= 38 ? "medium" : "low";
  document.querySelector("#signal-list").innerHTML = result.signals.map(signal => `<div class="signal signal-${signal.type}"><span class="signal-icon">${signal.type === "risk" ? "!" : signal.type === "good" ? "✓" : "·"}</span><div><strong>${signal.title}</strong><small>${signal.detail}</small></div></div>`).join("");
}

async function render() {
  const text = input.value.trim();
  count.textContent = `${input.value.length.toLocaleString()} / 2,000`;
  if (!text) return;
  try {
    const response = await fetch("/api/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }) });
    if (!response.ok) throw new Error("API unavailable");
    renderResult(await response.json());
  } catch (error) {
    document.querySelector("#score-value").textContent = "—";
    document.querySelector("#result-label").textContent = "Model unavailable";
    document.querySelector("#result-description").textContent = "Start the Flask server and train a valid model artifact before analysing text.";
    document.querySelector("#confidence-badge").textContent = "OFFLINE";
    document.querySelector("#signal-list").innerHTML = "<div class=\"empty-signal\">No prediction was produced.</div>";
  }
}

input.addEventListener("input", () => { count.textContent = `${input.value.length.toLocaleString()} / 2,000`; });
document.querySelector("#analyse-btn").addEventListener("click", render);
document.querySelectorAll("[data-sample]").forEach(button => button.addEventListener("click", () => { input.value = samples[button.dataset.sample]; render(); }));
render();
