# MedIntellect: High-End Clinical Medical Report Analyzer
### Multi-Indicator Syndromic Pattern & Cross-Biomarker Risk Reasoner

---

## 🌟 Overview
**MedIntellect** replaces generic single-value laboratory checkers with a **multivariate syndromic reasoning engine**. Instead of flagging isolated numbers in a vacuum, MedIntellect uncovers compound physiological patterns—such as how rising blood glucose paired with elevated serum creatinine signals early diabetic nephropathy.

Built with a modern **HTML5 / Vanilla CSS / JavaScript** frontend featuring:
- Medical dark-mode design system with clinical cyan, slate blue, and emerald accents
- Real-time drag-and-drop file upload for PDF and plain text reports
- Interactive multi-scenario clinical simulator
- Biological & pathophysiological mechanism explanations
- Specialist triage routing and recommended confirmatory investigations
- One-click clinical consultation brief export (`.txt`)

---

## 🚀 How to Run

### 1. Launch the Server
Open terminal in the project directory and run:
```powershell
python -m uvicorn server:app --host 127.0.0.1 --port 8000
```

### 2. Access the Application
Open your web browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📁 Project Architecture

- **`static/`**:
  - `index.html`: Modern semantic HTML structure
  - `style.css`: Custom CSS design system (glassmorphism, vibrant alert cards, typography, responsive grid)
  - `app.js`: Dynamic client-side controller with real-time API integrations and drag-and-drop
- **`server.py`**: High-performance FastAPI server for file upload processing, PDF parsing, and REST endpoints
- **`analyzer_engine.py`**: Multi-parameter syndromic reasoning engine & regex report extractor
- **`knowledge_base.py`**: Reference ranges, physiological thresholds, and clinical combination rules
- **`sample_reports/`**: Ready-to-test clinical report files (Diabetic Nephropathy, Sepsis, Microcytic Anemia)

---

## ⚖️ Clinical Scope
*MedIntellect is designed as a clinical decision-support triage aid and educational tool. It does not provide definitive medical diagnoses. Results must always be reviewed by a licensed physician.*
