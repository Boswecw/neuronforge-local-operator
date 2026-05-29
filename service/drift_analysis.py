from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class DriftAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1)
    mode: str = "pov"
    anchor_text: str | None = None

    @model_validator(mode="before")
    @classmethod
    def accept_authorforge_shape(cls, data: object) -> object:
        if not isinstance(data, dict):
            return data

        working = dict(data)

        if "text" not in working and isinstance(working.get("scene_text"), str):
            working["text"] = working["scene_text"]

        return working


class DriftFinding(BaseModel):
    kind: str
    start: int
    end: int
    text: str
    evidence: str
    suggestion: str


class DriftAnalysisEnvelope(BaseModel):
    degraded: bool = False
    reason: str | None = None
    data: list[DriftFinding]


def analyze_drift(text: str, mode: str, anchor_text: str | None = None) -> DriftAnalysisEnvelope:
    normalized = text.strip()
    anchor_normalized = (anchor_text or "").strip()

    if not normalized:
        return DriftAnalysisEnvelope(
            degraded=False,
            reason=None,
            data=[],
        )

    lowered = normalized.lower()
    findings: list[DriftFinding] = []

    first_person_markers = [" i ", " me ", " my ", " mine ", " myself "]
    second_person_markers = [" you ", " your ", " yours ", " yourself "]

    padded = f" {lowered} "

    fp_hit = any(marker in padded for marker in first_person_markers)
    sp_hit = any(marker in padded for marker in second_person_markers)
    differs_from_anchor = bool(anchor_normalized and anchor_normalized.lower() != normalized.lower())

    kind_map = {
        "pov": "pov-drift",
        "voice": "voice-drift",
        "tone": "tone-drift",
        "continuity": "continuity-drift",
    }
    drift_kind = kind_map.get(mode, "pov-drift")

    evidence_parts: list[str] = []
    suggestion_parts: list[str] = []

    if fp_hit:
        evidence_parts.append("First-person markers detected in the scene text.")
        suggestion_parts.append("Check whether first-person phrasing matches the intended POV.")
    if sp_hit:
        evidence_parts.append("Second-person markers detected in the scene text.")
        suggestion_parts.append("Check whether second-person phrasing is intentional.")
    if differs_from_anchor:
        evidence_parts.append("Scene text differs from the anchor text.")
        suggestion_parts.append("Compare the scene against the anchor for consistency.")

    if evidence_parts:
        findings.append(
            DriftFinding(
                kind=drift_kind,
                start=0,
                end=min(len(normalized), max(1, len(normalized))),
                text=normalized[:200],
                evidence=" ".join(evidence_parts),
                suggestion=" ".join(suggestion_parts) or "Review the scene for drift.",
            )
        )

    return DriftAnalysisEnvelope(
        degraded=False,
        reason=None,
        data=findings,
    )