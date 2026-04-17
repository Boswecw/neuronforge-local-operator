"""Schema/model alignment tests.

Phase 0 promises that the JSON contracts and the Pydantic v2 runtime models
declare the *same* required field set. These tests catch silent drift early.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from prompt_assembly.runtime.models import (
    CompactionEventModel,
    CompiledBundleModel,
    ConstraintSurfaceModel,
    LongContextModel,
    PolicyDecisionModel,
    PromptAssemblyInputModel,
    PromptAssemblyManifestModel,
    RedactionPolicyModel,
    ResolverEnvelopeModel,
)

CONTRACTS_DIR = Path(__file__).resolve().parents[1] / "contracts"


def _load(name: str) -> dict:
    return json.loads((CONTRACTS_DIR / name).read_text())


def _required(schema: dict) -> set[str]:
    return set(schema.get("required", []))


def _model_fields(model_cls) -> set[str]:
    return set(model_cls.model_fields.keys())


@pytest.mark.parametrize(
    "schema_name,model_cls",
    [
        ("long_context.schema.json", LongContextModel),
        ("constraint_surface.schema.json", ConstraintSurfaceModel),
        ("prompt_assembly_input.schema.json", PromptAssemblyInputModel),
        ("prompt_assembly_manifest.schema.json", PromptAssemblyManifestModel),
        ("compiled_bundle.schema.json", CompiledBundleModel),
        ("redaction_policy.schema.json", RedactionPolicyModel),
    ],
)
def test_required_fields_are_subset_of_model_fields(schema_name, model_cls) -> None:
    schema = _load(schema_name)
    required = _required(schema)
    fields = _model_fields(model_cls)
    missing = required - fields
    assert not missing, f"{model_cls.__name__} missing required fields: {sorted(missing)}"


def test_long_context_required_set_is_locked() -> None:
    schema = _load("long_context.schema.json")
    expected = {
        "lane",
        "reason_codes",
        "summary_allowed",
        "sliding_window_allowed",
        "full_trace_required",
        "governance_no_amnesia",
        "partitioned_execution",
        "degraded",
        "contract_version",
    }
    assert _required(schema) == expected


def test_constraint_surface_required_set_is_locked() -> None:
    schema = _load("constraint_surface.schema.json")
    expected = {
        "constraint_surface_id",
        "schema_version",
        "authoritative",
        "constraint_type",
        "items",
        "source_refs",
        "trust_level",
        "created_at",
        "hash",
        "hash_algorithm",
        "serialization_format",
    }
    assert _required(schema) == expected


def test_manifest_required_set_is_locked() -> None:
    schema = _load("prompt_assembly_manifest.schema.json")
    expected = {
        "manifest_id",
        "schema_version",
        "profile_id",
        "tokenizer_id",
        "tokenizer_version",
        "long_context",
        "constraint_surfaces",
        "resolved_inputs",
        "policy_decisions",
        "compaction_events",
        "section_order",
        "section_token_counts",
        "protected_budget_tokens",
        "total_token_count",
        "assembled_at",
        "assembler_version",
        "redaction_policy_id",
    }
    assert _required(schema) == expected


def test_resolved_input_descriptor_field_alignment() -> None:
    schema = _load("prompt_assembly_manifest.schema.json")
    descriptor = schema["properties"]["resolved_inputs"]["items"]
    expected = {
        "input_id",
        "trust_level",
        "hash",
        "hash_algorithm",
        "stale",
    }
    assert set(descriptor["required"]) == expected
    assert set(descriptor["required"]) <= _model_fields(ResolverEnvelopeModel)


def test_policy_decision_field_alignment() -> None:
    schema = _load("prompt_assembly_manifest.schema.json")
    descriptor = schema["properties"]["policy_decisions"]["items"]
    expected = {"decision_id", "subject", "decision", "rationale_code"}
    assert set(descriptor["required"]) == expected
    assert set(descriptor["required"]) <= _model_fields(PolicyDecisionModel)


def test_compaction_event_field_alignment() -> None:
    schema = _load("prompt_assembly_manifest.schema.json")
    descriptor = schema["properties"]["compaction_events"]["items"]
    expected = {"event_id", "kind", "section_id", "tokens_before", "tokens_after"}
    assert set(descriptor["required"]) == expected
    assert set(descriptor["required"]) <= _model_fields(CompactionEventModel)


def test_lane_id_enum_matches_supported_set() -> None:
    schema = _load("common_enums.schema.json")
    enum_values = tuple(schema["$defs"]["lane_id"]["enum"])
    assert enum_values == ("LC-1", "LC-2", "LC-4")
