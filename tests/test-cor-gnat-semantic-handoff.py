#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from asyncio import run
from copy import deepcopy
from pathlib import Path

from pydantic import ValidationError


_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from service.cor_gnat_semantic_handoff import (  # noqa: E402
    CorGnatSemanticHandoffRequest,
    accept_cor_gnat_semantic_handoff,
)


def valid_payload() -> dict:
    return {
        "contract_version": "GnatSemanticHandoff.v1",
        "handoff_id": "gnat-semantic-handoff-001",
        "request_id": "gnat-request-001",
        "source_service_id": "cortex",
        "destination_service_id": "neuronforge-local",
        "source_artifact": {
            "artifact_ref": "pkg-gnat-001",
            "artifact_class": "retrieval_package",
            "artifact_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "source_gnat_run_id": "gnat-run-001",
            "source_plan_hash": "plan-hash-001",
            "source_state": "ready",
            "completeness_status": "complete",
            "retrieval_profile_id": "gnat.retrieval-prep-bounded.v1",
        },
        "explicit_request": {
            "request_scope": "app_request",
            "requested_by": "authorforge",
            "operator_visible_summary": (
                "AuthorForge requested non-canonical semantic candidates from the referenced GNAT artifact."
            ),
        },
        "candidate_generation": {
            "candidate_contract_family": "neuronforge.cor_gnat.semantic-candidates.v1",
            "semantic_result_posture": "non_canonical_candidate",
            "allowed_candidate_classes": [
                "structure_summary_candidate",
                "continuity_candidate",
            ],
            "model_resource_disclosure": {
                "route_class": "WORKHORSE_LOCAL",
                "model_id": "qwen2.5:14b",
                "resource_budget_class": "workhorse_local",
                "execution_mode": "local_model",
            },
        },
        "transfer_guardrails": {
            "cor_receipts_immutable": True,
            "receipt_mutation_allowed": False,
            "semantic_output_canonical": False,
            "raw_content_included": False,
            "details_redacted": True,
        },
        "operator_visible_message": (
            "NeuronForge may generate reviewable non-canonical semantic candidates only; "
            "COR receipts remain immutable."
        ),
        "created_at": "2026-06-07T00:00:00Z",
    }


class CorGnatSemanticHandoffTests(unittest.TestCase):
    def test_valid_handoff_accepts_candidate_generation_only(self) -> None:
        request = CorGnatSemanticHandoffRequest.model_validate(valid_payload())
        receipt = accept_cor_gnat_semantic_handoff(request)

        self.assertEqual(receipt.source_handoff_id, request.handoff_id)
        self.assertEqual(receipt.request_id, request.request_id)
        self.assertEqual(receipt.candidate_generation_state, "accepted_for_candidate_generation")
        self.assertEqual(receipt.semantic_result_posture, "non_canonical_candidate")
        self.assertEqual(receipt.provenance_class, "inferred_candidate")
        self.assertFalse(receipt.cor_receipts_mutation_allowed)
        self.assertEqual(receipt.model_resource_disclosure.model_id, "qwen2.5:14b")

    def test_raw_content_is_rejected(self) -> None:
        payload = valid_payload()
        payload["raw_content"] = "source text must not ride inside this envelope"

        with self.assertRaises(ValidationError):
            CorGnatSemanticHandoffRequest.model_validate(payload)

    def test_missing_model_resource_disclosure_is_rejected(self) -> None:
        payload = valid_payload()
        del payload["candidate_generation"]["model_resource_disclosure"]

        with self.assertRaises(ValidationError):
            CorGnatSemanticHandoffRequest.model_validate(payload)

    def test_mutable_cor_receipt_guardrail_is_rejected(self) -> None:
        payload = valid_payload()
        payload["transfer_guardrails"]["receipt_mutation_allowed"] = True

        with self.assertRaises(ValidationError):
            CorGnatSemanticHandoffRequest.model_validate(payload)

    def test_partial_source_must_be_marked_incomplete(self) -> None:
        payload = valid_payload()
        payload["source_artifact"]["source_state"] = "partial_success"
        payload["source_artifact"]["completeness_status"] = "complete"

        with self.assertRaises(ValidationError):
            CorGnatSemanticHandoffRequest.model_validate(payload)

    def test_route_handler_returns_candidate_receipt(self) -> None:
        from service.main import app, cor_gnat_semantic_handoff

        route_paths = {getattr(route, "path", "") for route in app.routes}
        self.assertIn("/api/v1/cortex/gnat-semantic-handoff", route_paths)

        request = CorGnatSemanticHandoffRequest.model_validate(deepcopy(valid_payload()))
        receipt = run(cor_gnat_semantic_handoff(request))

        self.assertEqual(receipt.receipt_version, "NeuronForgeGnatSemanticHandoffReceipt.v1")
        self.assertEqual(receipt.source_handoff_id, "gnat-semantic-handoff-001")
        self.assertEqual(receipt.candidate_generation_state, "accepted_for_candidate_generation")
        self.assertEqual(receipt.semantic_result_posture, "non_canonical_candidate")
        self.assertFalse(receipt.cor_receipts_mutation_allowed)


if __name__ == "__main__":
    unittest.main()
