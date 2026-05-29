#!/usr/bin/env python3
"""
Contract-level tests for analyze.style.scene.v1.

Tests:
  1.  Valid request schema accepted
  2.  Malformed request rejected (missing required fields)
  3.  Success path — mock model returns valid structured JSON → valid response
  4.  Degraded path — mock model returns JSON with empty evidence_spans → degraded
  5.  Degraded path — mock model returns JSON with confidence < 0.4 → degraded
  6.  Degraded path — mock model returns JSON with missing dimension score → degraded
  7.  Failed path — mock model returns prose-only text → failed, output_payload None
  8.  Failed path — mock model returns JSON missing summary → failed
  9.  Failed path — mock model returns JSON missing overall_assessment → failed
  10. Failed path — mock model returns JSON missing dimension_scores → failed
  11. Failed path — mock model returns unparseable JSON → failed
  12. Route test — POST /api/v1/authorforge/style-analysis returns 200 with correct envelope
  13. Route test — POST with missing task_type returns 422
  14. Dimension score clamping — out-of-range scores clamped, warnings emitted
  15. Dimension score missing key — filled 0.0, warned, result is degraded

Usage:
  python3 tests/test-style-analysis.py
  python3 -m pytest tests/test-style-analysis.py   (if pytest is available)

Exit codes:
  0 = all tests passed
  1 = one or more tests failed
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Path setup: allow import from scripts/style_analysis/ when running from
# the project root or from the tests/ directory.
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))

from style_analysis.models import (
    StyleAnalysisInputPayload,
    StyleAnalysisRequest,
    StyleAnalysisResponse,
)
from style_analysis.normalizer import normalize_model_output

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_SCENE_TEXT = (
    "Rawn crossed the ford without speaking. The water was cold against his boots. "
    "Behind him, Mira watched from the bank, her expression unreadable. "
    "He did not turn back. The far shore offered nothing but more silence."
)

_VALID_MODEL_JSON = json.dumps(
    {
        "summary": "A terse, restrained scene with controlled pacing.",
        "overall_assessment": (
            "The scene maintains strong voice consistency and clear, uncluttered prose. "
            "Flow is smooth but sentence variety is slightly limited by the short declarative pattern."
        ),
        "dimension_scores": {
            "clarity": 0.85,
            "flow": 0.78,
            "voice_consistency": 0.90,
            "pov_fidelity": 0.85,
            "sentence_variety": 0.55,
            "pacing": 0.80,
        },
        "findings": [
            {
                "type": "strength",
                "label": "Clean declarative style",
                "detail": "Sentences are clear and direct, supporting the restrained tone.",
            },
            {
                "type": "weakness",
                "label": "Limited sentence variety",
                "detail": "Most sentences follow a short subject-verb pattern which may feel monotonous.",
            },
        ],
        "recommendations": [
            {
                "priority": "medium",
                "label": "Vary sentence length",
                "detail": "Introduce one or two longer sentences to vary rhythm without breaking tone.",
            }
        ],
        "confidence": 0.75,
        "evidence_spans": [
            {"start": 0, "end": 35, "reason": "Opening sentence sets restrained tone"},
            {"start": 80, "end": 130, "reason": "Mira observation point of view shift"},
        ],
    }
)

_DEGRADED_EMPTY_SPANS_JSON = json.dumps(
    {
        "summary": "A terse scene.",
        "overall_assessment": "The scene is controlled and restrained.",
        "dimension_scores": {
            "clarity": 0.8,
            "flow": 0.7,
            "voice_consistency": 0.85,
            "pov_fidelity": 0.90,
            "sentence_variety": 0.5,
            "pacing": 0.75,
        },
        "findings": [],
        "recommendations": [],
        "confidence": 0.70,
        "evidence_spans": [],  # empty → degraded
    }
)

_DEGRADED_LOW_CONFIDENCE_JSON = json.dumps(
    {
        "summary": "A terse scene.",
        "overall_assessment": "The scene is controlled and restrained.",
        "dimension_scores": {
            "clarity": 0.8,
            "flow": 0.7,
            "voice_consistency": 0.85,
            "pov_fidelity": 0.90,
            "sentence_variety": 0.5,
            "pacing": 0.75,
        },
        "findings": [],
        "recommendations": [],
        "confidence": 0.30,  # < 0.4 → degraded
        "evidence_spans": [{"start": 0, "end": 10, "reason": "opening"}],
    }
)

_DEGRADED_MISSING_DIMENSION_JSON = json.dumps(
    {
        "summary": "A terse scene.",
        "overall_assessment": "The scene is controlled.",
        "dimension_scores": {
            "clarity": 0.8,
            "flow": 0.7,
            # voice_consistency missing → degraded
            "pov_fidelity": 0.90,
            "sentence_variety": 0.5,
            "pacing": 0.75,
        },
        "findings": [],
        "recommendations": [],
        "confidence": 0.70,
        "evidence_spans": [{"start": 0, "end": 10, "reason": "opening"}],
    }
)

_PROSE_ONLY = (
    "This scene has good clarity and flow. The voice is consistent. "
    "Sentence variety is moderate. Pacing is effective."
)

_MISSING_SUMMARY_JSON = json.dumps(
    {
        # no summary
        "overall_assessment": "Good scene.",
        "dimension_scores": {
            "clarity": 0.8,
            "flow": 0.7,
            "voice_consistency": 0.85,
            "pov_fidelity": 0.90,
            "sentence_variety": 0.5,
            "pacing": 0.75,
        },
        "findings": [],
        "recommendations": [],
        "confidence": 0.70,
        "evidence_spans": [],
    }
)

_MISSING_OVERALL_ASSESSMENT_JSON = json.dumps(
    {
        "summary": "Terse scene.",
        # no overall_assessment
        "dimension_scores": {
            "clarity": 0.8,
            "flow": 0.7,
            "voice_consistency": 0.85,
            "pov_fidelity": 0.90,
            "sentence_variety": 0.5,
            "pacing": 0.75,
        },
        "findings": [],
        "recommendations": [],
        "confidence": 0.70,
        "evidence_spans": [],
    }
)

_MISSING_DIMENSION_SCORES_JSON = json.dumps(
    {
        "summary": "Terse scene.",
        "overall_assessment": "Good.",
        # no dimension_scores
        "findings": [],
        "recommendations": [],
        "confidence": 0.70,
        "evidence_spans": [],
    }
)

_CLAMPED_SCORES_JSON = json.dumps(
    {
        "summary": "A scene.",
        "overall_assessment": "Acceptable.",
        "dimension_scores": {
            "clarity": 1.5,    # > 1.0 → clamped to 1.0
            "flow": -0.2,      # < 0.0 → clamped to 0.0
            "voice_consistency": 0.9,
            "pov_fidelity": 0.85,
            "sentence_variety": 0.5,
            "pacing": 0.6,
        },
        "findings": [],
        "recommendations": [],
        "confidence": 0.60,
        "evidence_spans": [{"start": 0, "end": 5, "reason": "test span"}],
    }
)


# ---------------------------------------------------------------------------
# Test: Pydantic models (Phase 0 contract freeze)
# ---------------------------------------------------------------------------


class TestRequestSchema(unittest.TestCase):
    """Tests for the request schema."""

    def test_valid_request_accepted(self) -> None:
        """Test 1: Valid request schema accepted."""
        req = StyleAnalysisRequest(
            request_id="test-001",
            task_family="analysis",
            task_type="style_analysis",
            contract_version="v1",
            source_scope="scene",
            input_payload=StyleAnalysisInputPayload(scene_text=_SCENE_TEXT),
        )
        self.assertEqual(req.request_id, "test-001")
        self.assertEqual(req.task_family, "analysis")
        self.assertEqual(req.task_type, "style_analysis")
        self.assertEqual(req.contract_version, "v1")
        self.assertEqual(req.source_scope, "scene")
        self.assertEqual(req.input_payload.scene_text, _SCENE_TEXT)
        self.assertEqual(req.desired_runtime_mode, "WORKHORSE_LOCAL")
        self.assertEqual(req.output_strictness, "structured")

    def test_malformed_request_missing_request_id(self) -> None:
        """Test 2a: Malformed request rejected — missing request_id."""
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            StyleAnalysisRequest(
                # request_id omitted
                task_family="analysis",
                task_type="style_analysis",
                contract_version="v1",
                source_scope="scene",
                input_payload=StyleAnalysisInputPayload(scene_text=_SCENE_TEXT),
            )

    def test_malformed_request_wrong_task_family(self) -> None:
        """Test 2b: Malformed request rejected — wrong task_family."""
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            StyleAnalysisRequest(
                request_id="test-001",
                task_family="extraction",  # wrong — must be "analysis"
                task_type="style_analysis",
                contract_version="v1",
                source_scope="scene",
                input_payload=StyleAnalysisInputPayload(scene_text=_SCENE_TEXT),
            )

    def test_malformed_request_wrong_contract_version(self) -> None:
        """Test 2c: Malformed request rejected — wrong contract_version."""
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            StyleAnalysisRequest(
                request_id="test-001",
                task_family="analysis",
                task_type="style_analysis",
                contract_version="v2",  # wrong — must be "v1"
                source_scope="scene",
                input_payload=StyleAnalysisInputPayload(scene_text=_SCENE_TEXT),
            )

    def test_malformed_request_wrong_source_scope(self) -> None:
        """Test 2d: Malformed request rejected — wrong source_scope."""
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            StyleAnalysisRequest(
                request_id="test-001",
                task_family="analysis",
                task_type="style_analysis",
                contract_version="v1",
                source_scope="chapter",  # wrong — must be "scene"
                input_payload=StyleAnalysisInputPayload(scene_text=_SCENE_TEXT),
            )

    def test_malformed_request_empty_scene_text(self) -> None:
        """Test 2e: Malformed request rejected — empty scene_text."""
        from pydantic import ValidationError

        with self.assertRaises(ValidationError):
            StyleAnalysisInputPayload(scene_text="")


# ---------------------------------------------------------------------------
# Test: Normalizer (Phase 2)
# ---------------------------------------------------------------------------


class TestNormalizer(unittest.TestCase):
    """Tests for the output normalizer."""

    def test_success_path_valid_json(self) -> None:
        """Test 3: Success path — valid structured JSON → valid response."""
        result = normalize_model_output(_VALID_MODEL_JSON, model_id="qwen2.5:14b")
        self.assertEqual(result.schema_validation_status, "valid")
        self.assertIsNotNone(result.output_payload)
        assert result.output_payload is not None
        self.assertGreater(len(result.output_payload.summary), 0)
        self.assertGreater(len(result.output_payload.overall_assessment), 0)
        self.assertIn("clarity", result.output_payload.dimension_scores)
        self.assertIn("flow", result.output_payload.dimension_scores)
        self.assertIn("voice_consistency", result.output_payload.dimension_scores)
        self.assertIn("pov_fidelity", result.output_payload.dimension_scores)
        self.assertIn("sentence_variety", result.output_payload.dimension_scores)
        self.assertIn("pacing", result.output_payload.dimension_scores)
        for score in result.output_payload.dimension_scores.values():
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)
        self.assertGreater(len(result.output_payload.evidence_spans), 0)
        self.assertGreaterEqual(result.output_payload.confidence, 0.4)
        self.assertEqual(result.provenance_class, "inferred_candidate")
        self.assertEqual(result.route_class, "WORKHORSE_LOCAL")

    def test_degraded_path_empty_evidence_spans(self) -> None:
        """Test 4: Degraded path — empty evidence_spans → degraded."""
        result = normalize_model_output(_DEGRADED_EMPTY_SPANS_JSON, model_id="qwen2.5:14b")
        self.assertEqual(result.schema_validation_status, "degraded")
        self.assertIsNotNone(result.output_payload)
        any_degraded_warning = any(
            "evidence_spans is empty" in w for w in result.warnings
        )
        self.assertTrue(
            any_degraded_warning,
            f"Expected evidence_spans warning in: {result.warnings}",
        )

    def test_degraded_path_low_confidence(self) -> None:
        """Test 5: Degraded path — confidence < 0.4 → degraded."""
        result = normalize_model_output(
            _DEGRADED_LOW_CONFIDENCE_JSON, model_id="qwen2.5:14b"
        )
        self.assertEqual(result.schema_validation_status, "degraded")
        self.assertIsNotNone(result.output_payload)
        assert result.output_payload is not None
        self.assertLess(result.output_payload.confidence, 0.4)
        any_confidence_warning = any("confidence" in w for w in result.warnings)
        self.assertTrue(
            any_confidence_warning,
            f"Expected confidence warning in: {result.warnings}",
        )

    def test_degraded_path_missing_dimension_score(self) -> None:
        """Test 6: Degraded path — missing dimension score → filled 0.0 + degraded."""
        result = normalize_model_output(
            _DEGRADED_MISSING_DIMENSION_JSON, model_id="qwen2.5:14b"
        )
        self.assertEqual(result.schema_validation_status, "degraded")
        self.assertIsNotNone(result.output_payload)
        assert result.output_payload is not None
        # Missing voice_consistency should be filled with 0.0
        self.assertEqual(result.output_payload.dimension_scores.get("voice_consistency"), 0.0)
        # A warning about the missing key must exist
        any_missing_warning = any("voice_consistency" in w for w in result.warnings)
        self.assertTrue(
            any_missing_warning,
            f"Expected voice_consistency warning in: {result.warnings}",
        )

    def test_failed_path_prose_only(self) -> None:
        """Test 7: Failed path — prose-only output → failed, output_payload None."""
        result = normalize_model_output(_PROSE_ONLY, model_id="qwen2.5:14b")
        self.assertEqual(result.schema_validation_status, "failed")
        self.assertIsNone(result.output_payload)
        self.assertGreater(len(result.warnings), 0)

    def test_failed_path_missing_summary(self) -> None:
        """Test 8: Failed path — JSON missing summary → failed."""
        result = normalize_model_output(_MISSING_SUMMARY_JSON, model_id="qwen2.5:14b")
        self.assertEqual(result.schema_validation_status, "failed")
        self.assertIsNone(result.output_payload)

    def test_failed_path_missing_overall_assessment(self) -> None:
        """Test 9: Failed path — JSON missing overall_assessment → failed."""
        result = normalize_model_output(
            _MISSING_OVERALL_ASSESSMENT_JSON, model_id="qwen2.5:14b"
        )
        self.assertEqual(result.schema_validation_status, "failed")
        self.assertIsNone(result.output_payload)

    def test_failed_path_missing_dimension_scores(self) -> None:
        """Test 10: Failed path — JSON missing dimension_scores entirely → failed."""
        result = normalize_model_output(
            _MISSING_DIMENSION_SCORES_JSON, model_id="qwen2.5:14b"
        )
        self.assertEqual(result.schema_validation_status, "failed")
        self.assertIsNone(result.output_payload)

    def test_failed_path_unparseable_json(self) -> None:
        """Test 11: Failed path — unparseable JSON → failed."""
        broken = '{"summary": "test", "dimension_scores": {invalid json here'
        result = normalize_model_output(broken, model_id="qwen2.5:14b")
        self.assertEqual(result.schema_validation_status, "failed")
        self.assertIsNone(result.output_payload)

    def test_dimension_score_clamping(self) -> None:
        """Test 14: Out-of-range dimension scores are clamped with warnings."""
        result = normalize_model_output(_CLAMPED_SCORES_JSON, model_id="qwen2.5:14b")
        # clarity was 1.5 → clamped 1.0; flow was -0.2 → clamped 0.0
        # Scores still present and valid, but warnings issued
        # Output may be degraded (due to evidence span having valid entries)
        # or valid — the key is clamping happened
        self.assertIsNotNone(result.output_payload)
        assert result.output_payload is not None
        self.assertEqual(result.output_payload.dimension_scores["clarity"], 1.0)
        self.assertEqual(result.output_payload.dimension_scores["flow"], 0.0)
        # Warnings should mention the clamping
        any_clamp_warning = any("clamped" in w for w in result.warnings)
        self.assertTrue(
            any_clamp_warning,
            f"Expected clamping warning in: {result.warnings}",
        )

    def test_json_in_markdown_fences(self) -> None:
        """Valid JSON wrapped in markdown fences is extracted and normalized."""
        fenced = f"```json\n{_VALID_MODEL_JSON}\n```"
        result = normalize_model_output(fenced, model_id="qwen2.5:14b")
        self.assertIn(result.schema_validation_status, ("valid", "degraded"))
        self.assertIsNotNone(result.output_payload)

    def test_think_blocks_stripped(self) -> None:
        """<think>...</think> blocks from reasoning models are stripped before parsing."""
        with_think = f"<think>\nLet me analyze...\n</think>\n{_VALID_MODEL_JSON}"
        result = normalize_model_output(with_think, model_id="phi4-reasoning:latest")
        self.assertIn(result.schema_validation_status, ("valid", "degraded"))
        self.assertIsNotNone(result.output_payload)


# ---------------------------------------------------------------------------
# Test: FastAPI route (Phase 1)
# ---------------------------------------------------------------------------


class TestRoute(unittest.TestCase):
    """Tests for the FastAPI route."""

    def setUp(self) -> None:
        try:
            from fastapi.testclient import TestClient
            from style_analysis.app import app

            self.client = TestClient(app)
            self.skip_reason = None
        except ImportError as exc:
            self.client = None  # type: ignore[assignment]
            self.skip_reason = str(exc)

    def _skip_if_no_client(self) -> None:
        if self.client is None:
            self.skipTest(f"FastAPI TestClient unavailable: {self.skip_reason}")

    def _make_request_payload(self, scene_text: str = _SCENE_TEXT) -> dict:
        return {
            "request_id": "route-test-001",
            "task_family": "analysis",
            "task_type": "style_analysis",
            "contract_version": "v1",
            "source_scope": "scene",
            "input_payload": {"scene_text": scene_text},
            "desired_runtime_mode": "WORKHORSE_LOCAL",
            "output_strictness": "structured",
        }

    def test_route_returns_200_with_valid_mock_model(self) -> None:
        """Test 12: POST returns 200 with correct envelope when model returns valid JSON."""
        self._skip_if_no_client()

        with patch(
            "style_analysis.app.call_ollama", return_value=_VALID_MODEL_JSON
        ):
            response = self.client.post(
                "/api/v1/authorforge/style-analysis",
                json=self._make_request_payload(),
            )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("schema_validation_status", body)
        self.assertIn(body["schema_validation_status"], ("valid", "degraded"))
        self.assertIn("output_payload", body)
        self.assertIsNotNone(body["output_payload"])
        self.assertIn("route_class", body)
        self.assertIn("provenance_class", body)
        self.assertEqual(body["provenance_class"], "inferred_candidate")

    def test_route_returns_200_with_failed_envelope_when_model_returns_prose(
        self,
    ) -> None:
        """Test 12b: Route returns 200 with failed envelope when model returns prose."""
        self._skip_if_no_client()

        with patch(
            "style_analysis.app.call_ollama", return_value=_PROSE_ONLY
        ):
            response = self.client.post(
                "/api/v1/authorforge/style-analysis",
                json=self._make_request_payload(),
            )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["schema_validation_status"], "failed")
        self.assertIsNone(body["output_payload"])

    def test_route_returns_422_for_missing_task_type(self) -> None:
        """Test 13: Missing task_type field → 422 Unprocessable Entity."""
        self._skip_if_no_client()

        bad_payload = self._make_request_payload()
        del bad_payload["task_type"]

        with patch("style_analysis.app.call_ollama", return_value=_VALID_MODEL_JSON):
            response = self.client.post(
                "/api/v1/authorforge/style-analysis",
                json=bad_payload,
            )

        self.assertEqual(response.status_code, 422)

    def test_route_returns_422_for_wrong_task_family(self) -> None:
        """Test 13b: Wrong task_family → 422."""
        self._skip_if_no_client()

        bad_payload = self._make_request_payload()
        bad_payload["task_family"] = "extraction"

        with patch("style_analysis.app.call_ollama", return_value=_VALID_MODEL_JSON):
            response = self.client.post(
                "/api/v1/authorforge/style-analysis",
                json=bad_payload,
            )

        self.assertEqual(response.status_code, 422)

    def test_route_returns_200_with_failed_envelope_when_ollama_unavailable(
        self,
    ) -> None:
        """Route returns 200 with failed envelope when Ollama raises RuntimeError."""
        self._skip_if_no_client()

        with patch(
            "style_analysis.app.call_ollama",
            side_effect=RuntimeError("Ollama server unreachable"),
        ):
            response = self.client.post(
                "/api/v1/authorforge/style-analysis",
                json=self._make_request_payload(),
            )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["schema_validation_status"], "failed")
        self.assertIsNone(body["output_payload"])
        any_error_warning = any("model execution error" in w for w in body["warnings"])
        self.assertTrue(
            any_error_warning,
            f"Expected model execution error warning in: {body['warnings']}",
        )


# ---------------------------------------------------------------------------
# Test: Missing dimension score (Test 15)
# ---------------------------------------------------------------------------


class TestDimensionNormalization(unittest.TestCase):
    """Tests for dimension score normalization specifics."""

    def test_missing_dimension_filled_zero_and_warned(self) -> None:
        """Test 15: Missing dimension score filled with 0.0 and warned; result is degraded."""
        result = normalize_model_output(
            _DEGRADED_MISSING_DIMENSION_JSON, model_id="qwen2.5:14b"
        )
        self.assertEqual(result.schema_validation_status, "degraded")
        assert result.output_payload is not None
        self.assertEqual(result.output_payload.dimension_scores["voice_consistency"], 0.0)
        # All other dimensions should be present
        for dim in ("clarity", "flow", "pov_fidelity", "sentence_variety", "pacing"):
            self.assertIn(dim, result.output_payload.dimension_scores)
        # Warning must mention the missing key
        missing_warned = any("voice_consistency" in w for w in result.warnings)
        self.assertTrue(missing_warned)

    def test_all_six_dimensions_always_present_in_output(self) -> None:
        """Normalized output always contains all six v1 dimensions."""
        result = normalize_model_output(_VALID_MODEL_JSON, model_id="qwen2.5:14b")
        assert result.output_payload is not None
        for dim in ("clarity", "flow", "voice_consistency", "pov_fidelity", "sentence_variety", "pacing"):
            self.assertIn(dim, result.output_payload.dimension_scores)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    # Use verbosity=2 for clear per-test output matching the bash test style.
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
