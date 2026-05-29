"""
Pydantic models for contract: analyze.style.scene.v1

Task family:    analysis
Task type:      style_analysis
Contract:       v1
Scope:          scene
Output mode:    STRUCTURED_ANALYSIS
Runtime posture: WORKHORSE_LOCAL

V1 frozen dimension set: clarity, flow, voice_consistency, pov_fidelity, sentence_variety, pacing
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ---------------------------------------------------------------------------
# Sub-models: output payload components
# ---------------------------------------------------------------------------


class EvidenceSpan(BaseModel):
    """A character-offset span in the input scene text with a reason label."""

    start: int = Field(..., ge=0, description="Character offset start (0-based, inclusive)")
    end: int = Field(..., description="Character offset end (exclusive)")
    reason: str = Field(..., min_length=1, description="Why this span is relevant evidence")

    @model_validator(mode="after")
    def end_after_start(self) -> "EvidenceSpan":
        if self.end <= self.start:
            raise ValueError(f"end ({self.end}) must be greater than start ({self.start})")
        return self


class StyleFinding(BaseModel):
    """A single style finding: strength, weakness, or observation."""

    type: Literal["strength", "weakness", "observation"]
    label: str = Field(..., min_length=1, description="Short review-friendly label")
    detail: str = Field(..., min_length=1, description="Explanation of the finding")


class StyleRecommendation(BaseModel):
    """A single style recommendation with priority."""

    priority: Literal["high", "medium", "low"]
    label: str = Field(..., min_length=1, description="Short label for the recommendation")
    detail: str = Field(..., min_length=1, description="Description of the recommendation")


# V1 frozen dimensions — do not add or remove without a contract version bump.
_V1_DIMENSIONS: frozenset[str] = frozenset(
    {"clarity", "flow", "voice_consistency", "pov_fidelity", "sentence_variety", "pacing"}
)


class StyleAnalysisOutputPayload(BaseModel):
    """Structured output payload for analyze.style.scene.v1."""

    summary: str = Field(..., min_length=1, description="Short summary of overall scene style")
    overall_assessment: str = Field(
        ..., min_length=1, description="Detailed advisory assessment of scene style"
    )
    dimension_scores: dict[str, float] = Field(
        ...,
        description=(
            "Scores for each frozen v1 dimension (clarity, flow, voice_consistency, "
            "pov_fidelity, sentence_variety, pacing). Values 0.0–1.0."
        ),
    )
    findings: list[StyleFinding] = Field(
        default_factory=list, description="Style findings (strengths, weaknesses, observations)"
    )
    recommendations: list[StyleRecommendation] = Field(
        default_factory=list, description="Style recommendations with priority"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Model confidence in this analysis (0.0–1.0)"
    )
    evidence_spans: list[EvidenceSpan] = Field(
        default_factory=list, description="Character-offset evidence spans from the scene text"
    )

    @model_validator(mode="after")
    def validate_dimension_scores(self) -> "StyleAnalysisOutputPayload":
        for key, value in self.dimension_scores.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"dimension_scores[{key!r}] must be a number, got {type(value).__name__}")
            if not (0.0 <= float(value) <= 1.0):
                raise ValueError(
                    f"dimension_scores[{key!r}] must be between 0.0 and 1.0, got {value}"
                )
        return self


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------


class StyleAnalysisInputPayload(BaseModel):
    """Input payload for a style analysis request."""

    scene_text: str = Field(..., min_length=1, description="The full scene text to analyze")


class StyleAnalysisRequest(BaseModel):
    """
    Full request envelope for analyze.style.scene.v1.

    Layer A (shared envelope) fields are present here alongside the
    task-specific input_payload (Layer C).
    """

    request_id: str = Field(..., min_length=1, description="Caller-supplied request / trace id")
    task_family: Literal["analysis"] = "analysis"
    task_type: Literal["style_analysis"] = "style_analysis"
    contract_version: Literal["v1"] = "v1"
    source_scope: Literal["scene"] = "scene"
    input_payload: StyleAnalysisInputPayload
    desired_runtime_mode: str = Field(
        default="WORKHORSE_LOCAL",
        description="Requested runtime route class",
    )
    output_strictness: Literal["structured"] = "structured"


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------


class StyleAnalysisResponse(BaseModel):
    """
    Full response envelope for analyze.style.scene.v1.

    schema_validation_status drives consumer trust posture:
      - "valid"    → all required fields present, scores valid
      - "degraded" → required fields present but confidence < 0.4,
                     evidence_spans empty, or some dimensions missing (filled 0.0)
      - "failed"   → JSON parse failure, missing core fields, or prose-only output
    """

    model_config = ConfigDict(protected_namespaces=())

    route_class: str = Field(default="WORKHORSE_LOCAL")
    model_id: str = Field(default="", description="Ollama model that executed the task")
    runtime_mode_used: str = Field(default="WORKHORSE_LOCAL")
    provenance_class: str = Field(default="inferred_candidate")
    schema_validation_status: Literal["valid", "degraded", "failed"]
    warnings: list[str] = Field(default_factory=list)
    output_payload: StyleAnalysisOutputPayload | None = None
