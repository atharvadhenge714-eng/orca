let currentAnalysisData = null;
let currentSamples = [];

// Initialize on page load
document.addEventListener("DOMContentLoaded", async () => {
  await fetchSampleScenarios();
  setupDragAndDrop();
});

// Switch Input Tabs
function switchInputMode(mode) {
  document.getElementById("modePresets").style.display = mode === 'presets' ? 'block' : 'none';
  document.getElementById("modeUpload").style.display = mode === 'upload' ? 'block' : 'none';
  document.getElementById("modeText").style.display = mode === 'text' ? 'block' : 'none';

  document.getElementById("tabPresetsBtn").className = 'tab-btn' + (mode === 'presets' ? ' active' : '');
  document.getElementById("tabUploadBtn").className = 'tab-btn' + (mode === 'upload' ? ' active' : '');
  document.getElementById("tabTextBtn").className = 'tab-btn' + (mode === 'text' ? ' active' : '');
}

// Fetch Predefined Cases
async function fetchSampleScenarios() {
  try {
    const res = await fetch("/api/samples");
    const data = await res.json();
    currentSamples = data.samples;
    renderSamplesList();
    // Default load first sample
    if (currentSamples.length > 0) {
      loadSample(currentSamples[0].id);
    }
  } catch (err) {
    console.error("Error loading sample cases:", err);
  }
}

function renderSamplesList() {
  const container = document.getElementById("samplesListContainer");
  container.innerHTML = "";

  currentSamples.forEach((s, idx) => {
    const card = document.createElement("div");
    card.className = "case-card" + (idx === 0 ? " active" : "");
    card.id = `sample-card-${idx}`;
    card.onclick = () => {
      document.querySelectorAll(".case-card").forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      loadSample(s.id);
    };

    card.innerHTML = `
      <div class="case-card-title">${s.name}</div>
      <div class="case-card-desc">${s.description}</div>
    `;
    container.appendChild(card);
  });
}

async function loadSample(sampleId) {
  const sample = currentSamples.find(s => s.id === sampleId);
  if (!sample) return;

  try {
    const res = await fetch("/api/analyze-values", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ values: sample.values })
    });
    const results = await res.json();
    renderAnalysis(results);
  } catch (err) {
    console.error("Error analyzing sample:", err);
  }
}

// Upload & Drag-and-Drop handling
function setupDragAndDrop() {
  const dropZone = document.getElementById("dropZone");

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.add("dragover");
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      dropZone.classList.remove("dragover");
    }, false);
  });

  dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
      uploadFile(files[0]);
    }
  });
}

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (file) {
    uploadFile(file);
  }
}

async function uploadFile(file) {
  const statusEl = document.getElementById("fileUploadStatus");
  statusEl.innerHTML = `<span style="color:var(--accent-cyan)">Uploading & parsing: ${file.name}...</span>`;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/api/analyze-file", {
      method: "POST",
      body: formData
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to parse report file");
    }
    const results = await res.json();
    statusEl.innerHTML = `<span style="color:var(--success)">✓ Successfully parsed & analyzed: ${file.name}</span>`;
    renderAnalysis(results);
  } catch (err) {
    statusEl.innerHTML = `<span style="color:var(--danger)">⚠️ ${err.message}</span>`;
  }
}

// Text analysis
async function analyzePastedText() {
  const text = document.getElementById("rawReportText").value;
  if (!text.trim()) {
    alert("Please paste report text first.");
    return;
  }

  try {
    const res = await fetch("/api/analyze-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Analysis failed.");
    }
    const results = await res.json();
    renderAnalysis(results);
  } catch (err) {
    alert("Error: " + err.message);
  }
}

// Main Render Function
function renderAnalysis(data) {
  currentAnalysisData = data;
  const triage = data.triage_summary;

  // 1. Triage Banner
  const banner = document.getElementById("triageBanner");
  banner.className = "triage-banner triage-" + (triage.risk_level.includes("CRITICAL") ? "CRITICAL" : (triage.risk_level.includes("ELEVATED") ? "ELEVATED" : "NORMAL"));

  const icon = triage.risk_level.includes("CRITICAL") ? "🚨" : (triage.risk_level.includes("ELEVATED") ? "⚠️" : "✅");
  document.getElementById("triageRiskTitle").innerHTML = `${icon} ${triage.risk_level}`;
  document.getElementById("triageUrgencyDesc").innerHTML = `<strong>Clinical Direction:</strong> ${triage.urgency}`;

  // 2. Metrics
  document.getElementById("valTotalAnalyzed").textContent = data.total_analyzed;
  document.getElementById("valNormal").textContent = data.normal_count;
  document.getElementById("valAbnormal").textContent = data.abnormal_count;
  document.getElementById("valSyndromes").textContent = data.combinations_detected.length;

  // 3. Syndromic Combinations (Standout Feature)
  const comboContainer = document.getElementById("combosList");
  comboContainer.innerHTML = "";

  if (data.combinations_detected.length === 0) {
    comboContainer.innerHTML = `
      <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid var(--success-border); padding: 18px 24px; border-radius: var(--radius-sm); color: #34d399;">
        ✓ <strong>No Compound Syndromic Abnormalities Detected.</strong> All biomarker deviations appear isolated and do not trigger compound pathophysiological risk criteria.
      </div>
    `;
  } else {
    data.combinations_detected.forEach(c => {
      const card = document.createElement("div");
      card.className = `syndrome-card ${c.severity}`;

      const allBios = [...c.primary_biomarkers, ...c.corroborating_biomarkers];
      const bioPills = allBios.map(b => `
        <span class="bio-pill">
          <strong>${b.name}</strong>: ${b.value} ${b.unit} 
          <span class="tag-dir-${b.status}">[${b.status}]</span>
        </span>
      `).join("");

      const investigations = c.suggested_investigations.map(inv => `
        <li>🔎 ${inv}</li>
      `).join("");

      card.innerHTML = `
        <div class="syndrome-header">
          <div class="syndrome-title">🩺 ${c.name}</div>
          <span class="badge-severity badge-${c.severity}">${c.severity} SEVERITY</span>
        </div>
        <div class="syndrome-summary">${c.summary}</div>
        
        <div class="mechanism-quote">
          <strong>🔬 Biological & Pathophysiological Mechanism:</strong><br>
          ${c.biological_mechanism}
        </div>

        <div class="syndrome-grid">
          <div>
            <div class="sub-title">Contributing Biomarkers</div>
            <div>${bioPills}</div>
          </div>
          <div>
            <div class="sub-title">Recommended Specialist Triage</div>
            <div style="color: #38bdf8; font-weight: 600; font-size: 0.88rem; margin-bottom: 8px;">
              🏥 ${c.recommended_specialty}
            </div>
            <div class="sub-title" style="margin-top: 10px;">Suggested Workup</div>
            <ul class="investigation-list">
              ${investigations}
            </ul>
          </div>
        </div>
      `;
      comboContainer.appendChild(card);
    });
  }

  // 4. Abnormal Flags Table
  const flagsTable = document.getElementById("flagsTableBody");
  flagsTable.innerHTML = "";

  if (data.abnormal_flags.length === 0) {
    flagsTable.innerHTML = `<tr><td colspan="6" style="text-align:center; color:#34d399; padding:20px;">✓ All evaluated metrics are within standard physiological ranges.</td></tr>`;
  } else {
    data.abnormal_flags.forEach(f => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td><strong>${f.name}</strong> <span style="font-size:0.75rem; color:var(--text-muted);">(${f.category})</span></td>
        <td><strong>${f.value}</strong> ${f.unit}</td>
        <td>${f.min} - ${f.max} ${f.unit}</td>
        <td><span class="badge-status ${f.status}">${f.status}</span></td>
        <td><strong>+${f.deviation_pct}%</strong> <span style="font-size:0.75rem; color:var(--text-muted);">(${f.severity})</span></td>
        <td style="font-size:0.82rem; color:#cbd5e1;">${f.clinical_significance}</td>
      `;
      flagsTable.appendChild(row);
    });
  }

  // 5. Complete Panel Table
  const allTable = document.getElementById("allDataTableBody");
  allTable.innerHTML = "";

  Object.values(data.results).forEach(r => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${r.name}</td>
      <td style="color:var(--text-muted); font-size:0.8rem;">${r.category}</td>
      <td><strong>${r.value}</strong> ${r.unit}</td>
      <td>${r.reference_range}</td>
      <td><span class="badge-status ${r.status}">${r.status}</span></td>
    `;
    allTable.appendChild(row);
  });
}

// Export Summary to TXT
function exportSummary() {
  if (!currentAnalysisData) return;
  const d = currentAnalysisData;
  const triage = d.triage_summary;

  let reportText = `======================================================================
MEDINTELLECT CLINICAL REPORT ANALYSIS & SYNDROMIC REASONING BRIEF
======================================================================
TRIAGE STATUS: ${triage.risk_level}
RECOMMENDATION: ${triage.urgency}
TOTAL ANALYZED: ${d.total_analyzed} | NORMAL: ${d.normal_count} | FLAGGED: ${d.abnormal_count}

----------------------------------------------------------------------
1. MULTI-INDICATOR SYNDROMIC PATTERNS DETECTED (${d.combinations_detected.length})
----------------------------------------------------------------------
`;

  if (d.combinations_detected.length === 0) {
    reportText += "No compound multi-indicator risks detected.\n";
  } else {
    d.combinations_detected.forEach((c, idx) => {
      reportText += `\n[${idx + 1}] ${c.name} [Severity: ${c.severity}]\n`;
      reportText += `    Summary: ${c.summary}\n`;
      reportText += `    Mechanism: ${c.biological_mechanism}\n`;
      reportText += `    Specialist Triage: ${c.recommended_specialty}\n`;
      reportText += `    Suggested Follow-Up:\n`;
      c.suggested_investigations.forEach(inv => {
        reportText += `      - ${inv}\n`;
      });
    });
  }

  reportText += `\n----------------------------------------------------------------------
2. FLAGGED OUT-OF-RANGE BIOMARKERS (${d.abnormal_flags.length})
----------------------------------------------------------------------\n`;

  d.abnormal_flags.forEach(f => {
    reportText += `- ${f.name}: ${f.value} ${f.unit} [${f.status} | Dev: +${f.deviation_pct}% | Ref: ${f.reference_range}]\n`;
    reportText += `  Note: ${f.clinical_significance}\n`;
  });

  reportText += `\n======================================================================
DISCLAIMER: Non-diagnostic clinical decision-support triage aid.
Requires evaluation and clinical verification by a certified physician.
======================================================================`;

  const blob = new Blob([reportText], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "medintellect_clinical_brief.txt";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
