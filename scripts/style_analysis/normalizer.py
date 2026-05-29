"""
Output normalization and validation for analyze.style.scene.v1.

This module converts raw model output (which may include reasoning blocks,
markdown fences, or partial JSON) into a validated StyleAnalysisResponse.

Normalization rules
-------------------
success:
  All required fields present, all dimension scores parseable and within
  0.0–1.0, summary and overall_assessment non-empty, schema validates.

degraded:
  Required fields present AND at least one of:
  - evidence_spans is empty or absent
  - confidence < 0.4
  - One or more v1 dimension scores missing (filled with 0.0, warned)

failed:
  Any of:
  - JSON cannot be parsed from model output
  - summary or overall_assessment missing or empty
  - dimension_scores missing entirely
  - Output is prose-only with no extractable JSON object
"""

from __future__ import annotations

import json
import re
from typing import Any

from .models import (
    EvidenceSpan,
    StyleAnalysisOutputPayload,
    StyleAnalysisResponse,
    StyleFinding,
    StyleRecommendation,
    _V1_DIMENSIONS,
)

# Confidence threshold below which a result is degraded (not failed).
_DEGRADED_CONFIDENCE_THRESHOLD = 0.4


# ---------------------------------------------------------------------------
# JSON extraction helpers (mirror the pattern in validate-continuity-candidate.py)
# ---------------------------------------------------------------------------


def _strip_think_blocks(text: str) -> str:
    """Remove <think>...</think> blocks produced by reasoning models."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


def _extract_json(text: str) -> str | None:
    """
    Extract a JSON object from model output that may contain markdown fences,
    reasoning blocks, or surrounding prose.
    """
    text = _strip_think_blocks(text).strip()
    if text.startswith("{"):
        return text
    # Strip markdown fences
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    # Find first { to last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return None


# ---------------------------------------------------------------------------
# Field coercion helpers
# ---------------------------------------------------------------------------


def _clamp_score(value: Any, key: str, warnings: list[str]) -> float:
    """
    Coerce a dimension score to float and clamp to [0.0, 1.0].
    Adds a warning if clamping occurs.
    """
    try:
        f = float(value)
    except (TypeError, ValueError):
        warnings.append(
            f"dimension_scores[{key!r}] could not be parsed as float (got {value!r}); using 0.0"
        )
        return 0.0
    if f < 0.0:
        warnings.append(f"dimension_scores[{key!r}] was {f} (< 0.0); clamped to 0.0")
        return 0.0
    if f > 1.0:
        warnings.append(f"dimension_scores[{key!r}] was {f} (> 1.0); clamped to 1.0")
        return 1.0
    return f


def _normalize_confidence(value: Any, warnings: list[str]) -> float:
    """Coerce confidence to float and clamp to [0.0, 1.0]."""
    try:
        f = float(value)
    except (TypeError, ValueError):
        warnings.append(f"confidence could not be parsed as float (got {value!r}); using 0.0")
        return 0.0
    if f < 0.0:
        warnings.append(f"confidence was {f} (< 0.0); clamped to 0.0")
        return 0.0
    if f > 1.0:
        warnings.append(f"confidence was {f} (> 1.0); clamped to 1.0")
        return 1.0
    return f


def _normalize_findings(raw: Any, warnings: list[str]) -> list[StyleFinding]:
    """Best-effort normalization of the findings array."""
    if not isinstance(raw, list):
        warnings.append("findings was not an array; using empty list")
        return []
    result: list[StyleFinding] = []
    valid_types = {"strength", "weakness", "observation"}
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            warnings.append(f"findings[{i}] is not an object; skipped")
            continue
        ftype = item.get("type", "")
        if ftype not in valid_types:
            warnings.append(
                f"findings[{i}].type {ftype!r} not in {sorted(valid_types)}; skipped"
            )
            continue
        label = item.get("label", "")
        detail = item.get("detail", "")
        if not label or not detail:
            warnings.append(
                f"findings[{i}] missing label or detail; skipped"
            )
            continue
        result.append(StyleFinding(type=ftype, label=label, detail=detail))  # type: ignore[arg-type]
    return result


def _normalize_recommendations(raw: Any, warnings: list[str]) -> list[StyleRecommendation]:
    """Best-effort normalization of the recommendations array."""
    if not isinstance(raw, list):
        warnings.append("recommendations was not an array; using empty list")
        return []
    result: list[StyleRecommendation] = []
    valid_priorities = {"high", "medium", "low"}
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            warnings.append(f"recommendations[{i}] is not an object; skipped")
            continue
        priority = item.get("priority", "")
        if priority not in valid_priorities:
            warnings.append(
                f"recommendations[{i}].priority {priority!r} not in {sorted(valid_priorities)}; skipped"
            )
            continue
        label = item.get("label", "")
        detail = item.get("detail", "")
        if not label or not detail:
            warnings.append(f"recommendations[{i}] missing label or detail; skipped")
            continue
        result.append(StyleRecommendation(priority=priority, label=label, detail=detail))  # type: ignore[arg-type]
    return result


def _normalize_evidence_spans(raw: Any, warnings: list[str]) -> list[EvidenceSpan]:
    """Best-effort normalization of the evidence_spans array."""
    if not isinstance(raw, list):
        warnings.append("evidence_spans was not an array; using empty list")
        return []
    result: list[EvidenceSpan] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            warnings.append(f"evidence_spans[{i}] is not an object; skipped")
            continue
        try:
            start = int(item.get("start", 0))
            end = int(item.get("end", 0))
        except (TypeError, ValueError):
            warnings.append(f"evidence_spans[{i}] has non-integer start/end; skipped")
            continue
        if end <= start:
            warnings.append(
                f"evidence_spans[{i}] end ({end}) <= start ({start}); skipped"
            )
            continue
        reason = item.get("reason", "")
        if not reason:
            warnings.append(f"evidence_spans[{i}] missing reason; skipped")
            continue
        result.append(EvidenceSpan(start=start, end=end, reason=reason))
    return result


# ---------------------------------------------------------------------------
# Main normalization entry point
# ---------------------------------------------------------------------------


def normalize_model_output(
    raw_text: str,
    model_id: str,
    runtime_mode_used: str = "WORKHORSE_LOCAL",
) -> StyleAnalysisResponse:
    """
    Parse and normalize raw model output into a StyleAnalysisResponse.

    Returns:
        StyleAnalysisResponse with schema_validation_status of "valid",
        "degraded", or "failed" — never fake success.
    """
    base_kwargs = {
        "route_class": "WORKHORSE_LOCAL",
        "model_id": model_id,
        "runtime_mode_used": runtime_mode_used,
        "provenance_class": "inferred_candidate",
    }
    warnings: list[str] = []

    # --- Step 1: Extract JSON from raw text ---
    json_text = _extract_json(raw_text)
    if json_text is None:
        return StyleAnalysisResponse(
            **base_kwargs,
            schema_validation_status="failed",
            warnings=["model output contains no extractable JSON object (prose-only output)"],
            output_payload=None,
        )

    try:
        data: dict[str, Any] = json.loads(json_text)
    except json.JSONDecodeError as exc:
        return StyleAnalysisResponse(
            **base_kwargs,
            schema_validation_status="failed",
            warnings=[f"JSON parse error: {exc}"],
            output_payload=None,
        )

    if not isinstance(data, dict):
        return StyleAnalysisResponse(
            **base_kwargs,
            schema_validation_status="failed",
            warnings=["model output JSON root is not an object"],
            output_payload=None,
        )

    # --- Step 2: Check hard-required fields ---
    summary = data.get("summary", "")
    overall_assessment = data.get("overall_assessment", "")

    if not isinstance(summary, str) or not summary.strip():
        return StyleAnalysisResponse(
            **base_kwargs,
            schema_validation_status="failed",
            warnings=["model output missing or empty 'summary' field"],
            output_payload=None,
        )

    if not isinstance(overall_assessment, str) or not overall_assessment.strip():
        return StyleAnalysisResponse(
            **base_kwargs,
            schema_validation_status="failed",
            warnings=["model output missing or empty 'overall_assessment' field"],
            output_payload=None,
        )

    raw_scores = data.get("dimension_scores")
    if not isinstance(raw_scores, dict):
        return StyleAnalysisResponse(
            **base_kwargs,
            schema_validation_status="failed",
            warnings=["model output missing or non-object 'dimension_scores' field"],
            output_payload=None,
        )

    # --- Step 3: Normalize dimension scores ---
    dimension_scores: dict[str, float] = {}
    for dim in _V1_DIMENSIONS:
        if dim not in raw_scores:
            warnings.append(f"dimension_scores missing key {dim!r}; using 0.0")
            dimension_scores[dim] = 0.0
        else:
            dimension_scores[dim] = _clamp_score(raw_scores[dim], dim, warnings)

    # --- Step 4: Normalize confidence ---
    raw_confidence = data.get("confidence", 0.0)
    confidence = _normalize_confidence(raw_confidence, warnings)

    # --- Step 5: Normalize optional arrays ---
    findings = _normalize_findings(data.get("findings", []), warnings)
    recommendations = _normalize_recommendations(data.get("recommendations", []), warnings)
    evidence_spans = _normalize_evidence_spans(data.get("evidence_spans", []), warnings)

    # --- Step 6: Build output payload ---
    output_payload = StyleAnalysisOutputPayload(
        summary=summary.strip(),
        overall_assessment=overall_assessment.strip(),
        dimension_scores=dimension_scores,
        findings=findings,
        recommendations=recommendations,
        confidence=confidence,
        evidence_spans=evidence_spans,
    )

    # --- Step 7: Determine status (valid vs degraded) ---
    degraded_reasons: list[str] = []

    if not evidence_spans:
        degraded_reasons.append("evidence_spans is empty")

    if confidence < _DEGRADED_CONFIDENCE_THRESHOLD:
        degraded_reasons.append(
            f"confidence {confidence:.2f} is below threshold {_DEGRADED_CONFIDENCE_THRESHOLD}"
        )

    # Warn about any missing dimension scores (already filled with 0.0 above)
    missing_dims = [w for w in warnings if "missing key" in w]
    if missing_dims:
        degraded_reasons.extend(missing_dims)

    if degraded_reasons:
        all_warnings = warnings + [f"degraded: {r}" for r in degraded_reasons]
        return StyleAnalysisResponse(
            **base_kwargs,
            schema_validation_status="degraded",
            warnings=all_warnings,
            output_payload=output_payload,
        )

    return StyleAnalysisResponse(
        **base_kwargs,
        schema_validation_status="valid",
        warnings=warnings,
        output_payload=output_payload,
    )
