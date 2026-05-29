from __future__ import annotations

from fastapi import FastAPI

from scripts.style_analysis.app import app as style_analysis_app
from service.drift_analysis import DriftAnalysisRequest, analyze_drift

app = FastAPI(
    title="NeuronForge Local Service",
    description="Local NeuronForge service surface for AuthorForge",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "neuronforge-local",
    }


@app.post("/api/v1/authorforge/drift-analysis")
async def drift_analysis(payload: DriftAnalysisRequest) -> dict:
    result = analyze_drift(payload.text, payload.mode, payload.anchor_text)
    return result.model_dump()


app.mount("/", style_analysis_app)