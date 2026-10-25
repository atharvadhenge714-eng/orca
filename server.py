"""
FastAPI Server for MedIntellect Medical Report Analyzer.
Provides endpoints for analyzing reports, listing samples, reference ranges, and serving HTML frontend.
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from knowledge_base import REFERENCE_RANGES, COMBINATION_RULES, SAMPLE_REPORTS
from analyzer_engine import parse_report_text, analyze_biomarkers

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

app = FastAPI(title="MedIntellect API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/samples")
async def get_samples():
    return {
        "samples": [
            {
                "id": key,
                "name": key,
                "description": val["description"],
                "values": val["values"]
            }
            for key, val in SAMPLE_REPORTS.items()
        ]
    }

@app.get("/api/reference-ranges")
async def get_reference_ranges():
    return REFERENCE_RANGES

@app.post("/api/analyze-values")
async def analyze_values(data: dict):
    values = data.get("values", {})
    if not values:
        raise HTTPException(status_code=400, detail="No biomarker values provided.")
    results = analyze_biomarkers(values)
    return results

@app.post("/api/analyze-text")
async def analyze_text(data: dict):
    raw_text = data.get("text", "")
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Empty text provided.")
    extracted = parse_report_text(raw_text)
    if not extracted:
        raise HTTPException(status_code=400, detail="Could not identify any known clinical biomarkers in the provided text.")
    results = analyze_biomarkers(extracted)
    results["extracted_biomarkers"] = extracted
    return results

@app.post("/api/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    raw_text = ""
    content = await file.read()

    if filename.endswith(".pdf"):
        if not HAS_PYPDF:
            raise HTTPException(status_code=500, detail="pypdf is not installed on the server.")
        import io
        pdf_reader = pypdf.PdfReader(io.BytesIO(content))
        for page in pdf_reader.pages:
            raw_text += (page.extract_text() or "") + "\n"
    else:
        raw_text = content.decode("utf-8", errors="ignore")

    extracted = parse_report_text(raw_text)
    if not extracted:
        raise HTTPException(status_code=400, detail="No recognized clinical biomarkers could be parsed from this file.")
    results = analyze_biomarkers(extracted)
    results["extracted_biomarkers"] = extracted
    results["raw_text_preview"] = raw_text[:800]
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
