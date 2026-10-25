"""
Knowledge Base of Clinical Biomarkers, Reference Ranges, and Multi-Indicator Syndromic Combinations.
NOTE: For educational and decision-support triage only. Not a diagnostic tool.
"""

REFERENCE_RANGES = {
    # Complete Blood Count (CBC)
    "hemoglobin": {
        "name": "Hemoglobin (Hb)",
        "min": 13.0,
        "max": 17.5,
        "unit": "g/dL",
        "category": "Hematology",
        "low_desc": "Low hemoglobin indicates possible anemia, occult blood loss, nutritional deficit, or bone marrow suppression.",
        "high_desc": "Elevated hemoglobin suggests polycythemia, chronic hypoxemia, dehydration, or smoker's erythrocytosis."
    },
    "rbc": {
        "name": "Red Blood Cell Count (RBC)",
        "min": 4.5,
        "max": 5.9,
        "unit": "million/mcL",
        "category": "Hematology",
        "low_desc": "Decreased red blood cells point towards anemia or hemolysis.",
        "high_desc": "Elevated red blood cells suggest secondary erythrocytosis or dehydration."
    },
    "mcv": {
        "name": "Mean Corpuscular Volume (MCV)",
        "min": 80.0,
        "max": 100.0,
        "unit": "fL",
        "category": "Hematology",
        "low_desc": "Microcytic erythrocytes commonly seen in iron deficiency anemia, thalassemia trait, or chronic disease.",
        "high_desc": "Macrocytic erythrocytes commonly seen in Vitamin B12/folate deficiency, alcohol misuse, or liver disease."
    },
    "wbc": {
        "name": "White Blood Cell Count (WBC)",
        "min": 4500,
        "max": 11000,
        "unit": "cells/mcL",
        "category": "Hematology",
        "low_desc": "Leukopenia indicates potential bone marrow suppression, severe viral infection, or autoimmune condition.",
        "high_desc": "Leukocytosis suggests active bacterial infection, acute systemic inflammation, tissue necrosis, or hematologic malignancy."
    },
    "platelets": {
        "name": "Platelet Count",
        "min": 150000,
        "max": 450000,
        "unit": "platelets/mcL",
        "category": "Hematology",
        "low_desc": "Thrombocytopenia increases hemorrhagic risk; possible causes include immune destruction (ITP), sepsis, splenic sequestration, or drug-induced.",
        "high_desc": "Thrombocytosis may reflect reactive thrombocytosis (infection/inflammation/iron deficit) or essential thrombocythemia."
    },

    # Metabolic & Renal
    "fasting_glucose": {
        "name": "Fasting Blood Glucose",
        "min": 70.0,
        "max": 99.0,
        "unit": "mg/dL",
        "category": "Metabolic & Endocrine",
        "low_desc": "Hypoglycemia may cause neuroglycopenic symptoms, diaphoresis, tachycardia.",
        "high_desc": "Impaired fasting glucose (100-125) or provisional diabetes (>=126 mg/dL)."
    },
    "hba1c": {
        "name": "Glycated Hemoglobin (HbA1c)",
        "min": 4.0,
        "max": 5.6,
        "unit": "%",
        "category": "Metabolic & Endocrine",
        "low_desc": "Unusually low HbA1c may occur with shortened erythrocyte lifespan or hemolytic anemia.",
        "high_desc": "HbA1c 5.7-6.4% indicates prediabetes; >=6.5% indicates diabetes mellitus."
    },
    "creatinine": {
        "name": "Serum Creatinine",
        "min": 0.6,
        "max": 1.2,
        "unit": "mg/dL",
        "category": "Renal Panel",
        "low_desc": "Low creatinine typically indicates decreased muscle mass or cachexia.",
        "high_desc": "Elevated creatinine indicates acute kidney injury (AKI) or chronic kidney disease (CKD) filtration impairment."
    },
    "bun": {
        "name": "Blood Urea Nitrogen (BUN)",
        "min": 7.0,
        "max": 20.0,
        "unit": "mg/dL",
        "category": "Renal Panel",
        "low_desc": "Low BUN may be seen in severe liver disease or malnutrition.",
        "high_desc": "Elevated BUN suggests reduced renal clearance, prerenal azotemia (dehydration/heart failure), or GI bleed."
    },
    "egfr": {
        "name": "Estimated GFR (eGFR)",
        "min": 90.0,
        "max": 120.0,
        "unit": "mL/min/1.73m2",
        "category": "Renal Panel",
        "low_desc": "Reduced glomerular filtration rate indicating stages of kidney damage (G1-G5 CKD criteria).",
        "high_desc": "Hyperfiltration may occur in early nephropathy or pregnancy."
    },
    "potassium": {
        "name": "Potassium (K+)",
        "min": 3.5,
        "max": 5.1,
        "unit": "mEq/L",
        "category": "Electrolytes",
        "low_desc": "Hypokalemia poses cardiac arrhythmia risks, muscle weakness, and ileus.",
        "high_desc": "Hyperkalemia poses acute arrhythmogenic and cardiac arrest risks (peaked T waves)."
    },
    "sodium": {
        "name": "Sodium (Na+)",
        "min": 135.0,
        "max": 145.0,
        "unit": "mEq/L",
        "category": "Electrolytes",
        "low_desc": "Hyponatremia can induce cerebral edema, confusion, lethargy, or seizures.",
        "high_desc": "Hypernatremia indicates hyperosmolar dehydration or unreplaced water loss."
    },

    # Liver Function Test (LFT)
    "alt": {
        "name": "Alanine Aminotransferase (ALT)",
        "min": 7.0,
        "max": 56.0,
        "unit": "U/L",
        "category": "Hepatic Panel",
        "low_desc": "Generally has minimal clinical significance.",
        "high_desc": "Specific marker for hepatocellular damage, viral hepatitis, toxic injury, or steatohepatitis."
    },
    "ast": {
        "name": "Aspartate Aminotransferase (AST)",
        "min": 10.0,
        "max": 40.0,
        "unit": "U/L",
        "category": "Hepatic Panel",
        "low_desc": "Generally has minimal clinical significance.",
        "high_desc": "Elevated in hepatocellular injury, cardiac muscle damage, or skeletal muscle breakdown."
    },
    "bilirubin_total": {
        "name": "Total Bilirubin",
        "min": 0.2,
        "max": 1.2,
        "unit": "mg/dL",
        "category": "Hepatic Panel",
        "low_desc": "Within normal lower limits.",
        "high_desc": "Hyperbilirubinemia causes jaundice, cholestasis, biliary obstruction, or brisk hemolysis."
    },
    "alk_phos": {
        "name": "Alkaline Phosphatase (ALP)",
        "min": 44.0,
        "max": 147.0,
        "unit": "U/L",
        "category": "Hepatic Panel",
        "low_desc": "Rarely indicates zinc deficiency or hypophosphatasia.",
        "high_desc": "Marked elevation suggests biliary obstruction, cholestatic liver disease, or bone turnover."
    },

    # Lipid Panel & Cardiovascular
    "total_cholesterol": {
        "name": "Total Cholesterol",
        "min": 125.0,
        "max": 200.0,
        "unit": "mg/dL",
        "category": "Lipid & Cardiovascular",
        "low_desc": "Severe hypocholesterolemia may correlate with malnutrition or critical illness.",
        "high_desc": "Hypercholesterolemia accelerates atherosclerotic cardiovascular risk."
    },
    "ldl": {
        "name": "LDL Cholesterol ('Bad' Cholesterol)",
        "min": 0.0,
        "max": 100.0,
        "unit": "mg/dL",
        "category": "Lipid & Cardiovascular",
        "low_desc": "Optimal cardiovascular risk profile level.",
        "high_desc": "Elevated LDL drives plaque deposition, elevating ischemic heart disease risk."
    },
    "hdl": {
        "name": "HDL Cholesterol ('Good' Cholesterol)",
        "min": 40.0,
        "max": 60.0,
        "unit": "mg/dL",
        "category": "Lipid & Cardiovascular",
        "low_desc": "Low HDL reduces reverse cholesterol transport; independent atherogenic risk factor.",
        "high_desc": "Protective against cardiovascular disease."
    },
    "triglycerides": {
        "name": "Triglycerides",
        "min": 0.0,
        "max": 150.0,
        "unit": "mg/dL",
        "category": "Lipid & Cardiovascular",
        "low_desc": "Normal physiological level.",
        "high_desc": "Hypertriglyceridemia accelerates atherogenesis and, at extreme levels (>500 mg/dL), acute pancreatitis."
    },
    "crp": {
        "name": "C-Reactive Protein (hs-CRP)",
        "min": 0.0,
        "max": 3.0,
        "unit": "mg/L",
        "category": "Inflammatory / Cardiovascular",
        "low_desc": "Normal baseline systemic inflammatory state.",
        "high_desc": "Elevated systemic inflammatory marker; high values indicate acute infection or active cardiovascular inflammation."
    },

    # Thyroid Function
    "tsh": {
        "name": "Thyroid Stimulating Hormone (TSH)",
        "min": 0.4,
        "max": 4.0,
        "unit": "mIU/L",
        "category": "Endocrine",
        "low_desc": "Low TSH indicates primary hyperthyroidism or pituitary deficit.",
        "high_desc": "Elevated TSH indicates primary hypothyroidism or inadequate thyroid replacement."
    },
    "free_t4": {
        "name": "Free Thyroxine (FT4)",
        "min": 0.8,
        "max": 1.8,
        "unit": "ng/dL",
        "category": "Endocrine",
        "low_desc": "Hypothyroid circulating hormone deficiency.",
        "high_desc": "Hyperthyroid circulating hormone excess."
    }
}

COMBINATION_RULES = [
    {
        "id": "DIABETIC_NEPHROPATHY",
        "name": "Diabetic Nephropathy Risk Pattern",
        "severity": "CRITICAL",
        "summary": "Co-occurrence of sustained hyperglycemia (elevated HbA1c/Glucose) with compromised renal excretion (elevated Creatinine/BUN or reduced eGFR).",
        "mechanism": "Chronic microvascular endothelial damage induced by advanced glycation end-products triggers glomerulosclerosis and tubular atrophy, drastically accelerating end-stage renal vulnerability.",
        "conditions": [
            {"param": "hba1c", "direction": "high"},
            {"param": "creatinine", "direction": "high"}
        ],
        "also_matching": [
            {"param": "fasting_glucose", "direction": "high"},
            {"param": "egfr", "direction": "low"}
        ],
        "recommended_specialty": "Nephrology & Endocrinology",
        "suggested_investigations": [
            "Spot urine albumin-to-creatinine ratio (uACR)",
            "Renal duplex ultrasonography",
            "Continuous glucose monitoring (CGM) or tighter glycemic regimen"
        ]
    },
    {
        "id": "ACUTE_SYSTEMIC_INFECTION_SEPSIS_RISK",
        "name": "Systemic Inflammatory Response / Severe Infection Pattern",
        "severity": "CRITICAL",
        "summary": "Severe leukocytosis or leukopenia combined with marked inflammatory elevation (hs-CRP) and/or platelet consumption.",
        "mechanism": "Systemic cytokine storm in response to bacterial or pathogen invasion stimulates massive leukocyte mobilization and hepatic acute-phase reactant synthesis (CRP). Concomitant thrombocytopenia points to platelet consumption or early DIC.",
        "conditions": [
            {"param": "wbc", "direction": "high"},
            {"param": "crp", "direction": "high"}
        ],
        "also_matching": [
            {"param": "platelets", "direction": "low"}
        ],
        "recommended_specialty": "Internal Medicine / Infectious Disease (Urgent Evaluation)",
        "suggested_investigations": [
            "Blood cultures (aerobic and anaerobic sets)",
            "Serum lactate and procalcitonin",
            "Urinalysis and chest radiography"
        ]
    },
    {
        "id": "ACUTE_LIVER_INJURY_HEPATOCELLULAR",
        "name": "Acute Hepatocellular Injury / Cholestatic Pattern",
        "severity": "HIGH",
        "summary": "Co-elevation of transaminases (ALT & AST) with concurrent hyperbilirubinemia or elevated alkaline phosphatase.",
        "mechanism": "Cellular rupture of hepatocytes releases ALT/AST into systemic circulation. Concomitant elevation of total bilirubin or ALP demonstrates hepatic clearance insufficiency or intra/extrahepatic biliary tree stasis.",
        "conditions": [
            {"param": "alt", "direction": "high"},
            {"param": "ast", "direction": "high"}
        ],
        "also_matching": [
            {"param": "bilirubin_total", "direction": "high"},
            {"param": "alk_phos", "direction": "high"}
        ],
        "recommended_specialty": "Gastroenterology & Hepatology",
        "suggested_investigations": [
            "Abdominal ultrasound with hepatobiliary evaluation",
            "Viral hepatitis serologies (Hep A, B, C, E panel)",
            "Coagulation profile (PT / INR)"
        ]
    },
    {
        "id": "ATHEROGENIC_METABOLIC_SYNDROME",
        "name": "Metabolic Syndrome & Accelerated Atherogenic Profile",
        "severity": "HIGH",
        "summary": "Dyslipidemic triad (high Triglycerides, low HDL, elevated LDL) combined with elevated fasting glucose or HbA1c.",
        "mechanism": "Peripheral insulin resistance induces adipose tissue lipolysis, generating free fatty acids that stimulate hepatic VLDL synthesis. High triglycerides exchange with HDL and LDL, producing small dense LDL particles that penetrate endothelium, vastly increasing coronary artery disease risk.",
        "conditions": [
            {"param": "triglycerides", "direction": "high"},
            {"param": "hdl", "direction": "low"}
        ],
        "also_matching": [
            {"param": "fasting_glucose", "direction": "high"},
            {"param": "ldl", "direction": "high"},
            {"param": "total_cholesterol", "direction": "high"}
        ],
        "recommended_specialty": "Preventive Cardiology & Metabolic Medicine",
        "suggested_investigations": [
            "Coronary Artery Calcium (CAC) scan or Exercise Stress ECG",
            "Comprehensive cardiovascular 10-year ASCVD risk calculation",
            "Lifestyle and nutritional intervention with medical lipid therapy review"
        ]
    },
    {
        "id": "MICROCYTIC_HYPOCHROMIC_ANEMIA",
        "name": "Microcytic Anemia Profile (Iron Deficiency vs Hemoglobinopathy)",
        "severity": "MODERATE",
        "summary": "Subnormal Hemoglobin (Hb) coupled with reduced Mean Corpuscular Volume (MCV) and RBC alterations.",
        "mechanism": "Impaired heme synthesis (most commonly due to iron exhaustion from occult blood loss or dietary deficit) produces abnormally small, pale red cells unable to adequately oxygenate peripheral tissues.",
        "conditions": [
            {"param": "hemoglobin", "direction": "low"},
            {"param": "mcv", "direction": "low"}
        ],
        "also_matching": [
            {"param": "rbc", "direction": "low"}
        ],
        "recommended_specialty": "Hematology / General Medicine",
        "suggested_investigations": [
            "Serum Ferritin, Total Iron Binding Capacity (TIBC), and Transferrin saturation",
            "Fecal occult blood test (FIT) or colonoscopy/endoscopy to rule out occult GI loss",
            "Peripheral blood smear morphology"
        ]
    },
    {
        "id": "MACROCYTIC_ANEMIA_PATTERN",
        "name": "Macrocytic Anemia Profile (Megaloblastic / B12-Folate Deficiency)",
        "severity": "MODERATE",
        "summary": "Reduced Hemoglobin coupled with elevated Mean Corpuscular Volume (MCV > 100 fL).",
        "mechanism": "Nuclear-cytoplasmic maturation dyssynchrony during erythropoiesis due to Vitamin B12 or Folate synthesis failure causes unusually large erythrocytes with abnormal chromatin.",
        "conditions": [
            {"param": "hemoglobin", "direction": "low"},
            {"param": "mcv", "direction": "high"}
        ],
        "recommended_specialty": "Hematology",
        "suggested_investigations": [
            "Serum Vitamin B12 and Folate assays",
            "Methylmalonic acid (MMA) and Homocysteine levels",
            "Medication review (e.g., hydroxyurea, methotrexate)"
        ]
    },
    {
        "id": "OVERT_PRIMARY_HYPOTHYROIDISM",
        "name": "Overt Primary Thyroid Dysfunction Pattern",
        "severity": "MODERATE",
        "summary": "Elevated TSH paired with abnormally depressed Free T4 (FT4).",
        "mechanism": "Failure of the thyroid gland to synthesize thyroxine triggers negative feedback amplification at the anterior pituitary, releasing excess TSH to stimulate the failing gland.",
        "conditions": [
            {"param": "tsh", "direction": "high"},
            {"param": "free_t4", "direction": "low"}
        ],
        "recommended_specialty": "Endocrinology",
        "suggested_investigations": [
            "Anti-Thyroid Peroxidase (anti-TPO) antibodies",
            "Thyroid ultrasonography",
            "Endocrine evaluation for levothyroxine initiation"
        ]
    },
    {
        "id": "RENAL_ELECTROLYTE_DYSREGULATION",
        "name": "Renal Impairment with Critical Electrolyte Imbalance",
        "severity": "CRITICAL",
        "summary": "Elevated Creatinine/BUN coupled with abnormal serum Potassium (K+ > 5.1 or < 3.5 mEq/L).",
        "mechanism": "As glomerular filtration and distal tubular exchange deteriorate, potassium excretion diminishes, leading to dangerous cardiotoxic potassium accumulation capable of precipitating ventricular arrhythmias.",
        "conditions": [
            {"param": "creatinine", "direction": "high"},
            {"param": "potassium", "direction": "high"}
        ],
        "also_matching": [
            {"param": "bun", "direction": "high"},
            {"param": "egfr", "direction": "low"}
        ],
        "recommended_specialty": "Emergency Medicine / Nephrology (Urgent)",
        "suggested_investigations": [
            "12-Lead Electrocardiogram (ECG) for peaked T waves or widened QRS",
            "Immediate repeat venous blood gas / stat electrolyte check",
            "Medication audit (ACE inhibitors, ARBs, potassium-sparing diuretics)"
        ]
    }
]

SAMPLE_REPORTS = {
    "Sample 1: Diabetic Nephropathy & Renal Stress": {
        "description": "Patient presenting with uncontrolled hyperglycemia and emerging signs of nephropathic impairment.",
        "values": {
            "fasting_glucose": 182.0,
            "hba1c": 8.7,
            "creatinine": 1.85,
            "bun": 32.0,
            "egfr": 42.0,
            "potassium": 5.4,
            "sodium": 138.0,
            "hemoglobin": 11.8,
            "wbc": 6800,
            "platelets": 220000,
            "total_cholesterol": 215.0,
            "triglycerides": 210.0,
            "ldl": 132.0,
            "hdl": 38.0,
            "alt": 28.0,
            "ast": 25.0
        }
    },
    "Sample 2: Sepsis / Severe Inflammatory Alert": {
        "description": "Patient experiencing high fever, acute distress with marked inflammatory indices and consumptive platelets.",
        "values": {
            "wbc": 18500,
            "crp": 68.0,
            "platelets": 98000,
            "hemoglobin": 12.1,
            "mcv": 88.0,
            "creatinine": 1.45,
            "bun": 26.0,
            "fasting_glucose": 115.0,
            "potassium": 4.1,
            "sodium": 134.0,
            "alt": 48.0,
            "ast": 52.0
        }
    },
    "Sample 3: Acute Hepatobiliary / Liver Injury": {
        "description": "Patient with jaundice, right upper quadrant tenderness, and profound transaminase elevations.",
        "values": {
            "alt": 195.0,
            "ast": 165.0,
            "bilirubin_total": 3.4,
            "alk_phos": 240.0,
            "hemoglobin": 13.9,
            "wbc": 9100,
            "platelets": 175000,
            "creatinine": 0.9,
            "fasting_glucose": 94.0,
            "crp": 8.5
        }
    },
    "Sample 4: Severe Iron Deficiency Microcytic Anemia": {
        "description": "Patient with chronic fatigue, pallor, low hemoglobin and classical microcytic indices.",
        "values": {
            "hemoglobin": 8.4,
            "rbc": 3.8,
            "mcv": 68.0,
            "wbc": 6200,
            "platelets": 480000,
            "fasting_glucose": 88.0,
            "creatinine": 0.8,
            "alt": 18.0,
            "ast": 19.0
        }
    },
    "Sample 5: Healthy Baseline Screening": {
        "description": "Routine annual health wellness checkup exhibiting all physiological values within normal limits.",
        "values": {
            "hemoglobin": 14.8,
            "rbc": 5.1,
            "mcv": 89.0,
            "wbc": 6500,
            "platelets": 275000,
            "fasting_glucose": 84.0,
            "hba1c": 5.2,
            "creatinine": 0.95,
            "bun": 14.0,
            "egfr": 105.0,
            "potassium": 4.2,
            "sodium": 140.0,
            "alt": 22.0,
            "ast": 24.0,
            "total_cholesterol": 172.0,
            "ldl": 88.0,
            "hdl": 54.0,
            "triglycerides": 98.0,
            "crp": 0.8,
            "tsh": 1.85,
            "free_t4": 1.25
        }
    }
}
