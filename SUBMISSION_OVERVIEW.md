# MedIntellect - Hackathon Submission & Quick Reference Sheet

### Project Title
**MedIntellect: Clinical Decision-Support Lab Report Analyzer with Multi-Indicator Syndromic Cross-Analysis**

### Track
**Healthcare & MedTech**

---

### 1. Problem Statement Solved
Standard laboratory analyzers report individual values in isolation, creating cognitive overload and missing compound risks. A patient with mildly high glucose and slightly elevated creatinine might appear manageable in isolation, but together they represent early diabetic nephropathy—a risk factor for irreversible renal decline. 

### 2. The Solution & Standout Innovation
MedIntellect goes beyond simple out-of-range thresholds:
1. **Syndromic Multi-Indicator Engine**: Evaluates cross-biomarker combinations across renal, endocrine, hepatic, cardiovascular, and hematologic axes.
2. **Biological Mechanism Explanations**: Details the underlying pathophysiology (e.g., endothelial damage, cytokine cascades, impaired reverse cholesterol transport).
3. **Specialist Triage Routing**: Guides the user to the appropriate medical specialist (e.g., Nephrology vs. Hepatology vs. Infectious Disease) and suggests standard confirmatory tests.
4. **Safety & Diagnostic Compliance**: Adheres to medical decision-support guidelines by framing findings as risk patterns and triage levels rather than definitive medical diagnoses.

---

### 3. Demo Walkthrough Steps (For Judges / Presentation)
1. **Launch App**: `streamlit run app.py` (running on `http://localhost:8501`).
2. **Preset Scenario 1 (Diabetic Nephropathy)**:
   - Select *Preset Clinical Cases* -> *Sample 1: Diabetic Nephropathy & Renal Stress*.
   - Point out how the engine immediately flags the compound pattern: **High HbA1c + High Creatinine + Low eGFR**, citing renal microvascular risk.
3. **File Upload Demo**:
   - Switch input to *Upload Report File*.
   - Upload any file from `sample_reports/` (e.g., `sample2_sepsis_infection.txt`).
   - Notice automated parsing, WBC + hs-CRP + Platelet consumption detection, and *Critical Alert* triage generation.
4. **Export Brief**:
   - Switch to the *Export Clinical Summary* tab to download a standardized clinical consultation brief.
