"""
FastAPI application for analyze.style.scene.v1.

Route: POST /api/v1/authorforge/style-analysis

Execution path:
  1. Validate the request envelope (fail closed on malformed input).
  2. Call the Ollama adapter to get raw model output.
  3. Normalize raw output into the structured response envelope.
  4. Return the response — never fake success.

To run locally (development):
  uvicorn scripts.style_analysis.app:app --reload --port 8765
"""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .adapter import DEFAULT_MODEL, call_ollama
from .models import StyleAnalysisRequest, StyleAnalysisResponse
from .normalizer import normalize_model_output

app = FastAPI(
    title="NeuronForge — Style Analysis",
    description="analyze.style.scene.v1: single-scene style analysis",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

_ROUTE = "/api/v1/authorforge/style-analysis"


@app.post(_ROUTE, response_model=StyleAnalysisResponse)
async def style_analysis(request: StyleAnalysisRequest) -> StyleAnalysisResponse:
    """
    POST /api/v1/authorforge/style-analysis

    Accepts a style analysis request envelope (contract: analyze.style.scene.v1)
    and returns a structured advisory analysis of the supplied scene text.

    Request validation is handled by FastAPI/Pydantic.  A malformed envelope
    returns HTTP 422 (Unprocessable Entity) — fail closed.

    Model execution failure or prose-only model output returns HTTP 200 with
    schema_validation_status: "failed" and output_payload: null.
    """
    model = os.environ.get("NF_STYLE_MODEL", DEFAULT_MODEL)
    runtime_mode = request.desired_runtime_mode or "WORKHORSE_LOCAL"

    try:
        raw_output = call_ollama(
            scene_text=request.input_payload.scene_text,
            model=model,
        )
    except RuntimeError as exc:
        # Ollama unavailable or execution error — return failed envelope.
        return StyleAnalysisResponse(
            route_class="WORKHORSE_LOCAL",
            model_id=model,
            runtime_mode_used=runtime_mode,
            provenance_class="inferred_candidate",
            schema_validation_status="failed",
            warnings=[f"model execution error: {exc}"],
            output_payload=None,
        )

    return normalize_model_output(
        raw_text=raw_output,
        model_id=model,
        runtime_mode_used=runtime_mode,
    )
