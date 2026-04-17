"""Phase 0 fixture builders.

These build the smallest *valid* Phase 0 instances of every contract object,
so individual tests can mutate one field at a time and assert rejection.

Builders return plain ``dict``s. Pydantic model construction happens in
the tests themselves so model-level errors are surfaced clearly.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

# A 64-char hex string — within the contract pattern ^[0-9a-f]{16,128}$.
SAMPLE_HASH = "a" * 64
ISO_NOW = datetime(2026, 4, 6, 12, 0, 0, tzinfo=timezone.utc).isoformat()


def long_context() -> dict[str, Any]:
    return {
        "lane": "LC-1",
        "reason_codes": ["governance_continuity_required"],
        "summary_allowed": False,
        "sliding_window_allowed": False,
        "full_trace_required": True,
        "governance_no_amnesia": True,
        "partitioned_execution": False,
        "degraded": False,
        "contract_version": "1.1.0-phase0",
    }


def constraint_surface() -> dict[str, Any]:
    return {
        "constraint_surface_id": "cs_authoritative_001",
        "schema_version": "1.1.0-phase0",
        "authoritative": True,
        "constraint_type": "patch_contract",
        "items": [{"rule": "no_overwrite_existing_files"}],
        "source_refs": ["forgecommand://run/abc123"],
        "trust_level": "authoritative",
        "created_at": ISO_NOW,
        "hash": SAMPLE_HASH,
        "hash_algorithm": "blake3",
        "serialization_format": "canonical_json",
    }


def prompt_assembly_input() -> dict[str, Any]:
    return {
        "schema_version": "1.1.0-phase0",
        "profile_id": "nf_local_editing_lore_safe_v1",
        "lane_request": "LC-1",
        "constraint_surface_refs": ["cs_authoritative_001"],
        "long_context": long_context(),
        "submitted_at": ISO_NOW,
    }


def prompt_assembly_manifest() -> dict[str, Any]:
    return {
        "manifest_id": "manifest_001",
        "schema_version": "1.1.0-phase0",
        "profile_id": "nf_local_editing_lore_safe_v1",
        "tokenizer_id": "qwen2.5-bpe",
        "tokenizer_version": "2.5.0",
        "long_context": long_context(),
        "constraint_surfaces": [constraint_surface()],
        "resolved_inputs": [
            {
                "input_id": "input_001",
                "trust_level": "trusted_runtime",
                "hash": SAMPLE_HASH,
                "hash_algorithm": "blake3",
                "stale": False,
            }
        ],
        "policy_decisions": [
            {
                "decision_id": "pd_001",
                "subject": "input_001",
                "decision": "admit",
                "rationale_code": "trusted_runtime_default_admit",
            }
        ],
        "compaction_events": [
            {
                "event_id": "ce_001",
                "kind": "no_compaction",
                "section_id": "section_main",
                "tokens_before": 0,
                "tokens_after": 0,
            }
        ],
        "section_order": ["section_main"],
        "section_token_counts": {"section_main": 0},
        "protected_budget_tokens": 0,
        "total_token_count": 0,
        "assembled_at": ISO_NOW,
        "assembler_version": "0.1.0-phase0",
        "redaction_policy_id": "rp_default_v1",
    }


def compiled_bundle() -> dict[str, Any]:
    return {
        "bundle_id": "bundle_001",
        "bundle_version": "0.1.0",
        "schema_version": "1.1.0-phase0",
        "manifest_id": "manifest_001",
        "serialization_format": "canonical_json",
        "content_hash": SAMPLE_HASH,
        "content_hash_algorithm": "blake3",
        "signature": {
            "algorithm": "ed25519",
            "key_id": "",
            "value": "",
            "signed": False,
        },
        "compatibility": {
            "min_consumer_version": "0.1.0",
            "min_tokenizer_version": "2.5.0",
            "tokenizer_id": "qwen2.5-bpe",
        },
        "created_at": ISO_NOW,
        "body": {"sections": []},
    }


def redaction_policy() -> dict[str, Any]:
    return {
        "redaction_policy_id": "rp_default_v1",
        "schema_version": "1.1.0-phase0",
        "manifest_visible_fields": [
            "manifest_id",
            "profile_id",
            "long_context",
            "section_order",
        ],
        "debug_visible_fields": [
            "policy_decisions",
            "compaction_events",
        ],
        "masked_fields": [
            "resolved_inputs.hash",
        ],
        "reference_only_fields": [
            "constraint_surfaces.items",
        ],
        "trust_level_effects": {
            "authoritative": {"force_masked": [], "force_reference_only": []},
            "trusted_runtime": {"force_masked": [], "force_reference_only": []},
            "derived": {
                "force_masked": [],
                "force_reference_only": ["constraint_surfaces.items"],
            },
            "untrusted": {
                "force_masked": ["resolved_inputs.hash"],
                "force_reference_only": ["constraint_surfaces.items"],
            },
        },
    }


def clone(value: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(value)
