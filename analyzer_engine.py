"""
Core Medical Report Analyzer Engine.
Extracts biomarkers, computes deviations, identifies single-abnormal flags,
and executes syndromic multi-indicator combination matching with pathophysiology explanations.
"""
import re
from typing import Dict, List, Any, Tuple
from knowledge_base import REFERENCE_RANGES, COMBINATION_RULES

# Synonyms for lab biomarkers to parse freeform text and PDFs
SYNONYMS = {
    "hemoglobin": ["hemoglobin", "haemoglobin", "hb", "hgb"],
    "rbc": ["rbc", "red blood cells", "erythrocytes", "total rbc"],
    "mcv": ["mcv", "mean corpuscular volume"],
    "wbc": ["wbc", "white blood cells", "leukocytes", "total leukocyte count", "tlc"],
    "platelets": ["platelet", "platelets", "plt", "thrombocytes", "platelet count"],
    "fasting_glucose": ["fasting blood sugar", "fbs", "fasting glucose", "glucose fasting", "blood glucose"],
    "hba1c": ["hba1c", "glycated hemoglobin", "glycohemoglobin", "a1c"],
    "creatinine": ["serum creatinine", "creatinine", "creat"],
    "bun": ["bun", "blood urea nitrogen", "urea"],
    "egfr": ["egfr", "estimated gfr", "glomerular filtration rate", "gfr"],
    "potassium": ["potassium", "k+", "serum potassium"],
    "sodium": ["sodium", "na+", "serum sodium"],
    "alt": ["alt", "sgpt", "alanine aminotransferase"],
    "ast": ["ast", "sgot", "aspartate aminotransferase"],
    "bilirubin_total": ["total bilirubin", "bilirubin total", "serum bilirubin"],
    "alk_phos": ["alkaline phosphatase", "alp", "alk phos"],
    "total_cholesterol": ["total cholesterol", "cholesterol total", "serum cholesterol"],
    "ldl": ["ldl", "ldl cholesterol", "low density lipoprotein"],
    "hdl": ["hdl", "hdl cholesterol", "high density lipoprotein"],
    "triglycerides": ["triglycerides", "tg", "trigs"],
    "crp": ["crp", "c-reactive protein", "hs-crp", "hscrp"],
    "tsh": ["tsh", "thyroid stimulating hormone", "ultra tsh"],
    "free_t4": ["free t4", "ft4", "free thyroxine"]
}

def parse_report_text(raw_text: str) -> Dict[str, float]:
    """
    Parses unstructured text or OCR extraction to extract numerical values for biomarkers.
    """
    extracted = {}
    lines = raw_text.splitlines()

    for line in lines:
        cleaned_line = line.strip().lower()
        if not cleaned_line:
            continue

        for param_key, alias_list in SYNONYMS.items():
            if param_key in extracted:
                continue
            for alias in alias_list:
                # Look for alias followed by colon, space, or tab, and then a number
                pattern = rf"(?:\b{re.escape(alias)}\b)[\s:=|-]+([0-9]+(?:\.[0-9]+)?)"
                match = re.search(pattern, cleaned_line)
                if match:
                    try:
                        extracted[param_key] = float(match.group(1))
                        break
                    except ValueError:
                        pass
                else:
                    # Also check if alias is at start of line with number later in line
                    if alias in cleaned_line:
                        # find numbers in the line
                        numbers = re.findall(r"\b([0-9]+(?:\.[0-9]+)?)\b", cleaned_line)
                        if numbers:
                            try:
                                # filter out non-viable numbers (e.g. dates like 2024)
                                val = float(numbers[0])
                                # verify it falls in a reasonable biological range
                                ref = REFERENCE_RANGES[param_key]
                                if 0.05 * ref["min"] <= val <= 20.0 * ref["max"]:
                                    extracted[param_key] = val
                                    break
                            except ValueError:
                                pass
    return extracted

def analyze_biomarkers(extracted_data: Dict[str, float]) -> Dict[str, Any]:
    """
    Analyzes all provided biomarkers against predefined clinical reference ranges.
    """
    flags = []
    normal_count = 0
    abnormal_count = 0
    analyzed_results = {}

    for param, value in extracted_data.items():
        if param not in REFERENCE_RANGES:
            continue
        
        ref = REFERENCE_RANGES[param]
        min_v = ref["min"]
        max_v = ref["max"]
        status = "NORMAL"
        severity = "LOW"
        deviation_pct = 0.0
        flag_note = "Within healthy reference range."

        if value < min_v:
            status = "LOW"
            deviation_pct = ((min_v - value) / (min_v if min_v > 0 else 1.0)) * 100
            flag_note = ref.get("low_desc", "Below normal reference limit.")
            if deviation_pct > 30:
                severity = "HIGH"
            elif deviation_pct > 15:
                severity = "MODERATE"
            else:
                severity = "MILD"
            abnormal_count += 1
        elif value > max_v:
            status = "HIGH"
            deviation_pct = ((value - max_v) / (max_v if max_v > 0 else 1.0)) * 100
            flag_note = ref.get("high_desc", "Above normal reference limit.")
            if deviation_pct > 30:
                severity = "HIGH"
            elif deviation_pct > 15:
                severity = "MODERATE"
            else:
                severity = "MILD"
            abnormal_count += 1
        else:
            normal_count += 1

        result_item = {
            "param": param,
            "name": ref["name"],
            "category": ref["category"],
            "value": value,
            "unit": ref["unit"],
            "reference_range": f"{min_v} - {max_v} {ref['unit']}",
            "min": min_v,
            "max": max_v,
            "status": status,
            "severity": severity,
            "deviation_pct": round(deviation_pct, 1),
            "clinical_significance": flag_note
        }
        analyzed_results[param] = result_item
        if status != "NORMAL":
            flags.append(result_item)

    # Sort flags by deviation percentage descending
    flags.sort(key=lambda x: x["deviation_pct"], reverse=True)

    # Identify multi-indicator combinations
    combinations = evaluate_combinations(analyzed_results)

    # Calculate overall risk triage tier
    risk_level, urgency_recommendation = compute_triage_score(flags, combinations)

    return {
        "total_analyzed": len(analyzed_results),
        "normal_count": normal_count,
        "abnormal_count": abnormal_count,
        "results": analyzed_results,
        "abnormal_flags": flags,
        "combinations_detected": combinations,
        "triage_summary": {
            "risk_level": risk_level,
            "urgency": urgency_recommendation,
            "critical_flags_count": sum(1 for c in combinations if c["severity"] == "CRITICAL"),
            "high_flags_count": sum(1 for c in combinations if c["severity"] == "HIGH")
        }
    }

def evaluate_combinations(analyzed_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Evaluates cross-parameter syndromic patterns.
    Explains the combined significance, physiological mechanism, and recommended specialist triage.
    """
    matched_combinations = []

    for rule in COMBINATION_RULES:
        primary_conditions_met = True
        matched_indicators = []

        # Check required primary conditions
        for cond in rule["conditions"]:
            p = cond["param"]
            req_dir = cond["direction"]
            if p not in analyzed_results:
                primary_conditions_met = False
                break
            
            res = analyzed_results[p]
            if res["status"] != req_dir.upper():
                primary_conditions_met = False
                break
            
            matched_indicators.append({
                "param": p,
                "name": res["name"],
                "value": res["value"],
                "unit": res["unit"],
                "status": res["status"],
                "role": "Primary Indicator"
            })

        if primary_conditions_met:
            # Check for contributing/secondary indicators
            secondary_indicators = []
            for sec in rule.get("also_matching", []):
                p = sec["param"]
                req_dir = sec["direction"]
                if p in analyzed_results and analyzed_results[p]["status"] == req_dir.upper():
                    res = analyzed_results[p]
                    secondary_indicators.append({
                        "param": p,
                        "name": res["name"],
                        "value": res["value"],
                        "unit": res["unit"],
                        "status": res["status"],
                        "role": "Corroborating Biomarker"
                    })

            matched_combinations.append({
                "rule_id": rule["id"],
                "name": rule["name"],
                "severity": rule["severity"],
                "summary": rule["summary"],
                "biological_mechanism": rule["mechanism"],
                "primary_biomarkers": matched_indicators,
                "corroborating_biomarkers": secondary_indicators,
                "recommended_specialty": rule["recommended_specialty"],
                "suggested_investigations": rule["suggested_investigations"]
            })

    # Sort matched combinations: CRITICAL first, then HIGH, then MODERATE
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MODERATE": 2, "LOW": 3}
    matched_combinations.sort(key=lambda x: priority_order.get(x["severity"], 99))
    return matched_combinations

def compute_triage_score(flags: List[Dict[str, Any]], combinations: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Determines clinical urgency classification without claiming a definitive diagnosis.
    """
    has_critical_combo = any(c["severity"] == "CRITICAL" for c in combinations)
    has_high_combo = any(c["severity"] == "HIGH" for c in combinations)
    high_single_dev = any(f["deviation_pct"] > 50 for f in flags)

    if has_critical_combo:
        return "CRITICAL ALERT", "Prompt Medical Evaluation Urgently Advised (within 24-48 hours or emergency care if acute symptoms are present)."
    elif has_high_combo or high_single_dev:
        return "ELEVATED RISK", "Specialist Consultation Recommended. Schedule an appointment for focused clinical assessment and confirmatory workup."
    elif len(flags) > 0:
        return "BORDERLINE / MONITOR", "Routine Clinical Review Recommended. Discuss these minor abnormalities with your primary healthcare provider."
    else:
        return "NORMAL RANGE", "All tested indicators fall within standard adult physiological reference limits."
