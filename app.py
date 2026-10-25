"""
Interactive Clinical Decision-Support Web Application.
Intelligent Medical Report Analyzer with Multi-Indicator Combinations.
DISCLAIMER: Non-diagnostic tool for clinical decision-support and educational triage.
"""
import streamlit as st
import pandas as pd
import json
import io
from knowledge_base import REFERENCE_RANGES, SAMPLE_REPORTS
from analyzer_engine import parse_report_text, analyze_biomarkers

# Try importing PDF reader if available
try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# Streamlit Page Setup
st.set_page_config(
    page_title="MedIntellect - Clinical Report Analyzer",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Top Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
        padding: 24px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        max-width: 850px;
        line-height: 1.5;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        background: rgba(14, 165, 233, 0.2);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.4);
        margin-bottom: 12px;
    }

    /* Metric Stat Cards */
    .stat-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
    }

    /* Alert Boxes */
    .alert-critical {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
        border-left: 6px solid #e11d48;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(225, 29, 72, 0.08);
    }
    .alert-high {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 6px solid #d97706;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(217, 119, 6, 0.08);
    }
    .alert-normal {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 6px solid #16a34a;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.08);
    }

    /* Multi-Indicator Combo Card */
    .combo-card {
        background: #ffffff;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    }
    .combo-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }
    .tag-critical {
        background: #ffe4e6;
        color: #be123c;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .tag-high {
        background: #fef3c7;
        color: #b45309;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .tag-moderate {
        background: #e0f2fe;
        color: #0369a1;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .mechanism-box {
        background: #f8fafc;
        border-radius: 8px;
        border-left: 4px solid #0284c7;
        padding: 14px 18px;
        font-size: 0.92rem;
        line-height: 1.55;
        color: #334155;
        margin-top: 12px;
        margin-bottom: 14px;
    }
    .disclaimer-footer {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 14px 20px;
        font-size: 0.85rem;
        color: #475569;
        margin-top: 35px;
    }
</style>
""", unsafe_allow_html=True)

# Top Hero Section
st.markdown("""
<div class="hero-banner">
    <div class="badge-pill">Clinical Decision Support Triage • v2.4</div>
    <div class="hero-title">MedIntellect Report Analyzer</div>
    <div class="hero-subtitle">
        High-precision biomarker deviation flagging and multi-indicator syndromic cross-analysis. Uncovers clinically actionable combinations that single lab values obscure.
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Controls & Input
with st.sidebar:
    st.header("📋 Input Source")
    input_mode = st.radio(
        "Choose Medical Report Input Mode:",
        ["Preset Clinical Cases", "Upload Report File (PDF/TXT)", "Manual Biomarker Entry"],
        index=0
    )

    extracted_biomarkers = {}

    if input_mode == "Preset Clinical Cases":
        st.subheader("Select Clinical Scenario:")
        selected_case_name = st.selectbox("Choose Case:", list(SAMPLE_REPORTS.keys()))
        case_info = SAMPLE_REPORTS[selected_case_name]
        st.info(f"**Scenario Context:**\n{case_info['description']}")
        extracted_biomarkers = case_info["values"]

    elif input_mode == "Upload Report File (PDF/TXT)":
        uploaded_file = st.file_uploader("Upload Lab Report", type=["pdf", "txt"])
        if uploaded_file is not None:
            raw_text = ""
            if uploaded_file.name.endswith(".pdf") and HAS_PYPDF:
                try:
                    pdf_reader = pypdf.PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        raw_text += page.extract_text() or ""
                except Exception as e:
                    st.error(f"Error extracting PDF: {e}")
            else:
                raw_text = uploaded_file.read().decode("utf-8", errors="ignore")

            with st.expander("View Extracted Raw Text", expanded=False):
                st.text(raw_text[:1200] + ("..." if len(raw_text) > 1200 else ""))

            extracted_biomarkers = parse_report_text(raw_text)
            st.success(f"Parsed {len(extracted_biomarkers)} recognized lab parameters.")
        else:
            st.info("Upload a standard laboratory report text or PDF file to start auto-extraction.")

    elif input_mode == "Manual Biomarker Entry":
        st.subheader("Customize Values:")
        # Group by category
        categories = sorted(list(set(b["category"] for b in REFERENCE_RANGES.values())))
        for cat in categories:
            with st.expander(cat, expanded=(cat in ["Hematology", "Metabolic & Endocrine"])):
                cat_params = [k for k, v in REFERENCE_RANGES.items() if v["category"] == cat]
                for p in cat_params:
                    ref = REFERENCE_RANGES[p]
                    val = st.number_input(
                        f"{ref['name']} ({ref['unit']})",
                        min_value=0.0,
                        max_value=float(ref['max'] * 5),
                        value=float(round((ref['min'] + ref['max'])/2, 2)),
                        step=0.1 if ref['max'] < 20 else 1.0,
                        key=f"input_{p}"
                    )
                    extracted_biomarkers[p] = val

    st.markdown("---")
    st.markdown("### ⚖️ Clinical Scope Notice")
    st.caption(
        "This software serves as a decision-support and educational analysis tool. "
        "It does not provide a definitive medical diagnosis. Clinical correlation by a licensed physician is essential."
    )

# Main Body Execution
if not extracted_biomarkers:
    st.warning("Please select a sample scenario or upload/enter laboratory test values from the sidebar to begin analysis.")
else:
    # Run analysis engine
    analysis = analyze_biomarkers(extracted_biomarkers)
    triage = analysis["triage_summary"]
    risk_level = triage["risk_level"]
    urgency = triage["urgency"]

    # Top Triage Status Display
    if risk_level == "CRITICAL ALERT":
        alert_class = "alert-critical"
        icon = "🚨"
    elif risk_level == "ELEVATED RISK":
        alert_class = "alert-high"
        icon = "⚠️"
    else:
        alert_class = "alert-normal"
        icon = "✅"

    st.markdown(f"""
    <div class="{alert_class}">
        <div style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Triage Urgency Tier</div>
        <div style="font-size: 1.4rem; font-weight: 800; margin: 4px 0;">{icon} {risk_level}</div>
        <div style="font-size: 1rem; color: #334155;"><strong>Clinical Direction:</strong> {urgency}</div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Quick Metric Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Tested Biomarkers", analysis["total_analyzed"])
    with c2:
        st.metric("Normal Range Indicators", analysis["normal_count"])
    with c3:
        st.metric("Abnormal / Out-of-Range", analysis["abnormal_count"], delta=f"{analysis['abnormal_count']} flagged" if analysis['abnormal_count'] else "0", delta_color="inverse")
    with c4:
        st.metric("Syndromic Patterns Identified", len(analysis["combinations_detected"]), delta=f"{triage['critical_flags_count']} Critical", delta_color="inverse")

    st.write("")

    # Tabs for structured viewing
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧬 Multi-Indicator Combinations (Deep Analysis)",
        "⚠️ Abnormal Lab Values Table",
        "📊 Complete Panel Breakdown",
        "📑 Export Clinical Summary"
    ])

    # TAB 1: Multi-Indicator Combinations
    with tab1:
        st.subheader("Cross-Biomarker Syndromic Patterns")
        st.markdown(
            "Isolated abnormal markers often fail to convey the full clinical picture. "
            "Our multi-indicator rules engine cross-evaluates interrelated physiological axes to identify syndromic risk patterns."
        )

        combos = analysis["combinations_detected"]
        if not combos:
            st.success("✨ No concerning multi-indicator patterns detected. Biomarkers do not exhibit compound syndromic elevation.")
        else:
            for combo in combos:
                tag_class = "tag-critical" if combo["severity"] == "CRITICAL" else ("tag-high" if combo["severity"] == "HIGH" else "tag-moderate")
                
                with st.container():
                    st.markdown(f"""
                    <div class="combo-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="combo-title">🩺 {combo['name']}</span>
                            <span class="{tag_class}">{combo['severity']} SEVERITY</span>
                        </div>
                        <p style="font-size: 0.95rem; color: #475569; margin-top: 4px;">{combo['summary']}</p>
                        
                        <div class="mechanism-box">
                            <strong>🔬 Physiological & Pathophysiological Mechanism:</strong><br>
                            {combo['biological_mechanism']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Sub-columns for indicators and clinical recommendations
                    col_left, col_right = st.columns([1, 1])

                    with col_left:
                        st.markdown("**Contributing Biomarkers:**")
                        for bio in combo["primary_biomarkers"] + combo["corroborating_biomarkers"]:
                            role_color = "#dc2626" if bio["status"] == "HIGH" else "#2563eb"
                            st.markdown(
                                f"- **{bio['name']}**: `{bio['value']} {bio['unit']}` "
                                f"<span style='color:{role_color}; font-weight:600;'>[{bio['status']}]</span> — *({bio['role']})*",
                                unsafe_allow_html=True
                            )

                    with col_right:
                        st.markdown(f"**Recommended Specialist Triage:** `{combo['recommended_specialty']}`")
                        st.markdown("**Suggested Follow-up Investigations:**")
                        for inv in combo["suggested_investigations"]:
                            st.markdown(f"- 🔎 {inv}")
                    
                    st.markdown("---")

    # TAB 2: Abnormal Flags
    with tab2:
        st.subheader("Values Outside Predefined Reference Limits")
        flags = analysis["abnormal_flags"]
        
        if not flags:
            st.success("All lab parameters are currently within their respective biological reference ranges.")
        else:
            # Format flag table nicely
            flag_rows = []
            for f in flags:
                flag_rows.append({
                    "Biomarker": f["name"],
                    "Category": f["category"],
                    "Report Value": f"{f['value']} {f['unit']}",
                    "Normal Reference": f"{f['min']} - {f['max']} {f['unit']}",
                    "Status": f["status"],
                    "Deviation": f"{f['deviation_pct']}%",
                    "Severity": f["severity"],
                    "Clinical Note": f["clinical_significance"]
                })
            df_flags = pd.DataFrame(flag_rows)
            st.dataframe(df_flags, use_container_width=True)

            # Graphical deviation bar
            st.subheader("Deviation Magnitude from Standard Reference")
            chart_data = pd.DataFrame({
                "Biomarker": [f["name"] for f in flags],
                "Deviation (%)": [f["deviation_pct"] for f in flags]
            }).set_index("Biomarker")
            st.bar_chart(chart_data)

    # TAB 3: Complete Panel Breakdown
    with tab3:
        st.subheader("Comprehensive Laboratory Panel Overview")
        all_res = analysis["results"]
        
        categories = sorted(list(set(r["category"] for r in all_res.values())))
        for cat in categories:
            st.markdown(f"#### 🧪 {cat}")
            cat_items = [r for r in all_res.values() if r["category"] == cat]
            
            c_data = []
            for item in cat_items:
                c_data.append({
                    "Parameter": item["name"],
                    "Observed Value": f"{item['value']} {item['unit']}",
                    "Normal Range": item["reference_range"],
                    "Status": "✅ NORMAL" if item["status"] == "NORMAL" else f"⚠️ {item['status']} ({item['severity']})",
                    "Significance / Interpretation": item["clinical_significance"]
                })
            st.dataframe(pd.DataFrame(c_data), use_container_width=True)

    # TAB 4: Export Summary
    with tab4:
        st.subheader("Export Clinical Evaluation Brief")
        st.write("Generate a standardized summary document for clinical consultation or personal medical record archiving.")

        # Prepare summary report text
        summary_text = f"""=======================================================
MEDINTELLECT CLINICAL DECISION-SUPPORT REPORT BRIEF
=======================================================
Triage Status: {risk_level}
Urgency Recommendation: {urgency}
Total Biomarkers Analyzed: {analysis['total_analyzed']}
Normal Count: {analysis['normal_count']} | Abnormal Count: {analysis['abnormal_count']}

-------------------------------------------------------
1. MULTI-INDICATOR SYNDROMIC PATTERNS DETECTED ({len(combos)})
-------------------------------------------------------
"""
        if not combos:
            summary_text += "No high-risk multi-indicator combinations identified.\n"
        else:
            for i, c in enumerate(combos, 1):
                summary_text += f"\n[{i}] {c['name']} (Severity: {c['severity']})\n"
                summary_text += f"    Summary: {c['summary']}\n"
                summary_text += f"    Mechanism: {c['biological_mechanism']}\n"
                summary_text += f"    Triage Specialty: {c['recommended_specialty']}\n"
                summary_text += f"    Recommended Follow-up:\n"
                for inv in c['suggested_investigations']:
                    summary_text += f"      - {inv}\n"

        summary_text += """
-------------------------------------------------------
2. OUT-OF-RANGE BIOMARKERS SUMMARY
-------------------------------------------------------
"""
        for f in flags:
            summary_text += f"- {f['name']}: {f['value']} {f['unit']} [{f['status']} | {f['severity']} Deviation: {f['deviation_pct']}%] (Ref: {f['reference_range']})\n"
            summary_text += f"  Clinical note: {f['clinical_significance']}\n"

        summary_text += """
=======================================================
DISCLAIMER: This document is produced by an automated
decision-support software for informational and educational
triage purposes only. It is NOT a definitive clinical
diagnosis. Review with a licensed physician is required.
=======================================================
"""
        st.text_area("Generated Summary Brief", summary_text, height=320)

        c_down1, c_down2 = st.columns(2)
        with c_down1:
            st.download_button(
                label="📥 Download Clinical Summary (.txt)",
                data=summary_text,
                file_name="medintellect_clinical_summary.txt",
                mime="text/plain"
            )
        with c_down2:
            st.download_button(
                label="📥 Download Full Analysis Data (.json)",
                data=json.dumps(analysis, indent=2),
                file_name="medintellect_analysis_results.json",
                mime="application/json"
            )

# Regulatory Disclaimer Footer
st.markdown("""
<div class="disclaimer-footer">
    <strong>⚖️ Regulatory & Diagnostic Disclaimer:</strong><br>
    This software is designed strictly as a clinical decision-support triage aid and educational tool. 
    It is not certified as a primary diagnostic medical device (SaMD). Laboratory values must always be evaluated 
    in context with complete patient history, physical examination, and direct consultation with a qualified medical professional.
</div>
""", unsafe_allow_html=True)
