"""Phase 0 error taxonomy stability tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from prompt_assembly.runtime.errors import (
    ERROR_CODE_VALUES,
    BundleSignatureInvalidError,
    BundleVersionIncompatibleError,
    ConstraintSurfaceHashInvalidError,
    ErrorCode,
    ErrorEnvelope,
    LaneUnsupportedLocalError,
    ProfileInactiveError,
    ProfileLaneIncompatibleError,
    ProfileUnknownError,
    PromptAssemblyError,
    ProtectedBudgetImpossibleError,
    RequiredConstraintSurfaceMissingError,
    RequiredReferenceUnresolvedError,
    RequiredStaleInputError,
    SectionConflictUnresolvedError,
)

CONTRACTS_DIR = Path(__file__).resolve().parents[1] / "contracts"

EXPECTED_ERROR_CODES = (
    "ERR_PROFILE_UNKNOWN",
    "ERR_PROFILE_INACTIVE",
    "ERR_LANE_UNSUPPORTED_LOCAL",
    "ERR_PROFILE_LANE_INCOMPATIBLE",
    "ERR_REQUIRED_REFERENCE_UNRESOLVED",
    "ERR_REQUIRED_CONSTRAINT_SURFACE_MISSING",
    "ERR_CONSTRAINT_SURFACE_HASH_INVALID",
    "ERR_REQUIRED_STALE_INPUT",
    "ERR_PROTECTED_BUDGET_IMPOSSIBLE",
    "ERR_SECTION_CONFLICT_UNRESOLVED",
    "ERR_BUNDLE_VERSION_INCOMPATIBLE",
    "ERR_BUNDLE_SIGNATURE_INVALID",
)


def test_runtime_enum_matches_expected_phase0_set() -> None:
    assert tuple(code.value for code in ErrorCode) == EXPECTED_ERROR_CODES


def test_error_code_values_module_constant() -> None:
    assert ERROR_CODE_VALUES == EXPECTED_ERROR_CODES


def test_error_code_enum_matches_common_enums_schema() -> None:
    schema = json.loads((CONTRACTS_DIR / "common_enums.schema.json").read_text())
    json_codes = tuple(schema["$defs"]["error_code"]["enum"])
    assert json_codes == EXPECTED_ERROR_CODES


def test_error_envelope_is_immutable_and_strict() -> None:
    envelope = ErrorEnvelope(code=ErrorCode.PROFILE_UNKNOWN, message="missing")
    with pytest.raises(Exception):
        envelope.code = ErrorCode.PROFILE_INACTIVE  # frozen


def test_error_envelope_rejects_extras() -> None:
    with pytest.raises(Exception):
        ErrorEnvelope(
            code=ErrorCode.PROFILE_UNKNOWN,
            message="missing",
            sneaky_field="not allowed",  # type: ignore[call-arg]
        )


def test_error_envelope_requires_message() -> None:
    with pytest.raises(Exception):
        ErrorEnvelope(code=ErrorCode.PROFILE_UNKNOWN, message="")


@pytest.mark.parametrize(
    "exc_cls,args,expected_code",
    [
        (ProfileUnknownError, ("missing_profile",), ErrorCode.PROFILE_UNKNOWN),
        (ProfileInactiveError, ("inactive_profile",), ErrorCode.PROFILE_INACTIVE),
        (LaneUnsupportedLocalError, ("LC-5",), ErrorCode.LANE_UNSUPPORTED_LOCAL),
        (
            ProfileLaneIncompatibleError,
            ("nf_local_editing_lore_safe_v1", "LC-4"),
            ErrorCode.PROFILE_LANE_INCOMPATIBLE,
        ),
        (
            RequiredReferenceUnresolvedError,
            ("input://missing",),
            ErrorCode.REQUIRED_REFERENCE_UNRESOLVED,
        ),
        (
            RequiredConstraintSurfaceMissingError,
            ("cs_missing",),
            ErrorCode.REQUIRED_CONSTRAINT_SURFACE_MISSING,
        ),
        (
            ConstraintSurfaceHashInvalidError,
            ("cs_001",),
            ErrorCode.CONSTRAINT_SURFACE_HASH_INVALID,
        ),
        (RequiredStaleInputError, ("input_001",), ErrorCode.REQUIRED_STALE_INPUT),
        (
            ProtectedBudgetImpossibleError,
            (8000, 4096),
            ErrorCode.PROTECTED_BUDGET_IMPOSSIBLE,
        ),
        (
            SectionConflictUnresolvedError,
            (["a", "b"],),
            ErrorCode.SECTION_CONFLICT_UNRESOLVED,
        ),
        (
            BundleVersionIncompatibleError,
            ("0.0.1", "0.1.0"),
            ErrorCode.BUNDLE_VERSION_INCOMPATIBLE,
        ),
        (BundleSignatureInvalidError, ("bundle_001",), ErrorCode.BUNDLE_SIGNATURE_INVALID),
    ],
)
def test_specific_errors_carry_locked_codes(exc_cls, args, expected_code) -> None:
    err = exc_cls(*args)
    assert isinstance(err, PromptAssemblyError)
    assert err.envelope.code is expected_code
    assert err.envelope.message
    assert isinstance(err.envelope.details, dict)


def test_error_envelope_contains_iso_raised_at() -> None:
    envelope = ErrorEnvelope(code=ErrorCode.PROFILE_UNKNOWN, message="missing")
    iso = envelope.raised_at.isoformat()
    assert "T" in iso
