"""Phase 0 Pydantic model validation tests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from prompt_assembly.runtime.models import (
    CONTRACT_VERSION,
    CompiledBundleModel,
    ConstraintSurfaceModel,
    LongContextModel,
    PromptAssemblyInputModel,
    PromptAssemblyManifestModel,
    RedactionPolicyModel,
)
from prompt_assembly.tests.fixtures import builders


# --- Happy paths -----------------------------------------------------------


def test_long_context_model_accepts_valid_input() -> None:
    model = LongContextModel.model_validate(builders.long_context())
    assert model.lane.value == "LC-1"
    assert model.contract_version == CONTRACT_VERSION


def test_constraint_surface_model_accepts_valid_input() -> None:
    model = ConstraintSurfaceModel.model_validate(builders.constraint_surface())
    assert model.authoritative is True
    assert model.trust_level.value == "authoritative"


def test_prompt_assembly_input_model_accepts_valid_input() -> None:
    model = PromptAssemblyInputModel.model_validate(builders.prompt_assembly_input())
    assert model.profile_id == "nf_local_editing_lore_safe_v1"


def test_prompt_assembly_manifest_model_accepts_valid_input() -> None:
    model = PromptAssemblyManifestModel.model_validate(builders.prompt_assembly_manifest())
    assert model.tokenizer_id.value == "qwen2.5-bpe"
    assert model.tokenizer_version == "2.5.0"


def test_compiled_bundle_model_accepts_valid_input() -> None:
    model = CompiledBundleModel.model_validate(builders.compiled_bundle())
    assert model.signature.signed is False
    assert model.compatibility.tokenizer_id.value == "qwen2.5-bpe"


def test_redaction_policy_model_accepts_valid_input() -> None:
    model = RedactionPolicyModel.model_validate(builders.redaction_policy())
    assert model.trust_level_effects.untrusted.force_masked == ("resolved_inputs.hash",)


# --- Lane / enum rejection -------------------------------------------------


@pytest.mark.parametrize("bad_lane", ["LC-3", "LC-5", "LC-99", "lc-1", ""])
def test_long_context_model_rejects_unsupported_lanes(bad_lane: str) -> None:
    payload = builders.long_context()
    payload["lane"] = bad_lane
    with pytest.raises(ValidationError):
        LongContextModel.model_validate(payload)


def test_long_context_model_rejects_empty_reason_codes() -> None:
    payload = builders.long_context()
    payload["reason_codes"] = []
    with pytest.raises(ValidationError):
        LongContextModel.model_validate(payload)


def test_long_context_model_rejects_unknown_reason_code() -> None:
    payload = builders.long_context()
    payload["reason_codes"] = ["nostalgia"]
    with pytest.raises(ValidationError):
        LongContextModel.model_validate(payload)


# --- Trust / authority coherence -------------------------------------------


def test_constraint_surface_rejects_untrusted_authoritative() -> None:
    payload = builders.constraint_surface()
    payload["trust_level"] = "untrusted"
    payload["authoritative"] = True
    with pytest.raises(ValidationError):
        ConstraintSurfaceModel.model_validate(payload)


def test_constraint_surface_rejects_derived_authoritative() -> None:
    payload = builders.constraint_surface()
    payload["trust_level"] = "derived"
    payload["authoritative"] = True
    with pytest.raises(ValidationError):
        ConstraintSurfaceModel.model_validate(payload)


@pytest.mark.parametrize("bad_trust", ["rumored", "kinda_trusted", ""])
def test_constraint_surface_rejects_unknown_trust_level(bad_trust: str) -> None:
    payload = builders.constraint_surface()
    payload["trust_level"] = bad_trust
    with pytest.raises(ValidationError):
        ConstraintSurfaceModel.model_validate(payload)


@pytest.mark.parametrize(
    "bad_type", ["vibe_alignment", "patch_contractx", "PATCH_CONTRACT", ""]
)
def test_constraint_surface_rejects_unknown_constraint_type(bad_type: str) -> None:
    payload = builders.constraint_surface()
    payload["constraint_type"] = bad_type
    with pytest.raises(ValidationError):
        ConstraintSurfaceModel.model_validate(payload)


# --- Required-field enforcement (model layer) ------------------------------


@pytest.mark.parametrize(
    "field",
    [
        "lane",
        "reason_codes",
        "summary_allowed",
        "sliding_window_allowed",
        "full_trace_required",
        "governance_no_amnesia",
        "partitioned_execution",
        "degraded",
    ],
)
def test_long_context_model_requires_all_locked_fields(field: str) -> None:
    payload = builders.long_context()
    del payload[field]
    with pytest.raises(ValidationError):
        LongContextModel.model_validate(payload)


@pytest.mark.parametrize(
    "field",
    [
        "constraint_surface_id",
        "authoritative",
        "constraint_type",
        "items",
        "source_refs",
        "trust_level",
        "created_at",
        "hash",
        "hash_algorithm",
        "serialization_format",
    ],
)
def test_constraint_surface_model_requires_all_locked_fields(field: str) -> None:
    payload = builders.constraint_surface()
    del payload[field]
    with pytest.raises(ValidationError):
        ConstraintSurfaceModel.model_validate(payload)


# --- Manifest coherence ----------------------------------------------------


def test_manifest_rejects_section_count_mismatch() -> None:
    payload = builders.prompt_assembly_manifest()
    payload["section_token_counts"] = {"different_section": 0}
    with pytest.raises(ValidationError):
        PromptAssemblyManifestModel.model_validate(payload)


def test_manifest_rejects_negative_protected_budget() -> None:
    payload = builders.prompt_assembly_manifest()
    payload["protected_budget_tokens"] = -1
    with pytest.raises(ValidationError):
        PromptAssemblyManifestModel.model_validate(payload)


# --- Bundle baseline -------------------------------------------------------


def test_compiled_bundle_rejects_unknown_signature_algorithm() -> None:
    payload = builders.compiled_bundle()
    payload["signature"]["algorithm"] = "rsa-pss"
    with pytest.raises(ValidationError):
        CompiledBundleModel.model_validate(payload)


def test_compiled_bundle_rejects_non_canonical_serialization() -> None:
    payload = builders.compiled_bundle()
    payload["serialization_format"] = "yaml"
    with pytest.raises(ValidationError):
        CompiledBundleModel.model_validate(payload)


def test_compiled_bundle_phase0_signed_flag_is_false_by_fixture() -> None:
    """Phase 0 baseline: signed is always False because signing isn't active yet."""
    model = CompiledBundleModel.model_validate(builders.compiled_bundle())
    assert model.signature.signed is False
