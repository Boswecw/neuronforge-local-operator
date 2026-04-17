"""Stable Phase 0 error taxonomy for NeuronForge Local prompt assembly.

This module is the single source of truth for error codes. JSON contracts
reference the same names via ``common_enums.schema.json#/$defs/error_code``;
the test suite enforces parity between the two.

Phase 0 only locks the *taxonomy*. The conditions under which each code is
raised are described in the docstrings, but the assembler that emits them
lives in later phases.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorCode(str, Enum):
    """Stable Phase 0 error codes.

    Order is irrelevant for stability; the *string values* are the contract.
    Never rename a value. Add new codes only with explicit Phase planning.
    """

    PROFILE_UNKNOWN = "ERR_PROFILE_UNKNOWN"
    PROFILE_INACTIVE = "ERR_PROFILE_INACTIVE"
    LANE_UNSUPPORTED_LOCAL = "ERR_LANE_UNSUPPORTED_LOCAL"
    PROFILE_LANE_INCOMPATIBLE = "ERR_PROFILE_LANE_INCOMPATIBLE"
    REQUIRED_REFERENCE_UNRESOLVED = "ERR_REQUIRED_REFERENCE_UNRESOLVED"
    REQUIRED_CONSTRAINT_SURFACE_MISSING = "ERR_REQUIRED_CONSTRAINT_SURFACE_MISSING"
    CONSTRAINT_SURFACE_HASH_INVALID = "ERR_CONSTRAINT_SURFACE_HASH_INVALID"
    REQUIRED_STALE_INPUT = "ERR_REQUIRED_STALE_INPUT"
    PROTECTED_BUDGET_IMPOSSIBLE = "ERR_PROTECTED_BUDGET_IMPOSSIBLE"
    SECTION_CONFLICT_UNRESOLVED = "ERR_SECTION_CONFLICT_UNRESOLVED"
    BUNDLE_VERSION_INCOMPATIBLE = "ERR_BUNDLE_VERSION_INCOMPATIBLE"
    BUNDLE_SIGNATURE_INVALID = "ERR_BUNDLE_SIGNATURE_INVALID"


# Frozen ordered tuple — used for parity checks against the JSON enum.
ERROR_CODE_VALUES: tuple[str, ...] = tuple(code.value for code in ErrorCode)


class ErrorEnvelope(BaseModel):
    """Wire envelope for any Phase 0 error surface.

    The envelope is intentionally narrow: a stable code, a human-readable
    message, optional structured details, and a timestamp. No stack traces,
    no implementation hints, no caller-controlled fields.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
    )

    code: ErrorCode
    message: str = Field(min_length=1)
    details: dict[str, Any] = Field(default_factory=dict)
    raised_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PromptAssemblyError(Exception):
    """Base class for any Phase 0 prompt-assembly error.

    Always carries an :class:`ErrorEnvelope`. Callers should pattern-match
    on ``error.envelope.code`` rather than on the Python class name.
    """

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.envelope = ErrorEnvelope(
            code=code,
            message=message,
            details=details or {},
        )
        super().__init__(f"{code.value}: {message}")


class ProfileUnknownError(PromptAssemblyError):
    """ERR_PROFILE_UNKNOWN — caller asked for a profile_id not in the registry."""

    def __init__(self, profile_id: str) -> None:
        super().__init__(
            ErrorCode.PROFILE_UNKNOWN,
            f"Unknown profile_id: {profile_id!r}",
            details={"profile_id": profile_id},
        )


class ProfileInactiveError(PromptAssemblyError):
    """ERR_PROFILE_INACTIVE — profile exists but is not active in this build."""

    def __init__(self, profile_id: str) -> None:
        super().__init__(
            ErrorCode.PROFILE_INACTIVE,
            f"Profile is not active: {profile_id!r}",
            details={"profile_id": profile_id},
        )


class LaneUnsupportedLocalError(PromptAssemblyError):
    """ERR_LANE_UNSUPPORTED_LOCAL — lane is reserved but not locally executable in V1.1."""

    def __init__(self, lane: str) -> None:
        super().__init__(
            ErrorCode.LANE_UNSUPPORTED_LOCAL,
            f"Lane {lane!r} is not supported for local execution in V1.1",
            details={"lane": lane},
        )


class ProfileLaneIncompatibleError(PromptAssemblyError):
    """ERR_PROFILE_LANE_INCOMPATIBLE — selected profile cannot serve the requested lane."""

    def __init__(self, profile_id: str, lane: str) -> None:
        super().__init__(
            ErrorCode.PROFILE_LANE_INCOMPATIBLE,
            f"Profile {profile_id!r} is not compatible with lane {lane!r}",
            details={"profile_id": profile_id, "lane": lane},
        )


class RequiredReferenceUnresolvedError(PromptAssemblyError):
    """ERR_REQUIRED_REFERENCE_UNRESOLVED — a required input reference could not be resolved."""

    def __init__(self, reference: str) -> None:
        super().__init__(
            ErrorCode.REQUIRED_REFERENCE_UNRESOLVED,
            f"Required reference could not be resolved: {reference!r}",
            details={"reference": reference},
        )


class RequiredConstraintSurfaceMissingError(PromptAssemblyError):
    """ERR_REQUIRED_CONSTRAINT_SURFACE_MISSING — a constraint surface declared as required is absent."""

    def __init__(self, constraint_surface_id: str) -> None:
        super().__init__(
            ErrorCode.REQUIRED_CONSTRAINT_SURFACE_MISSING,
            f"Required constraint surface missing: {constraint_surface_id!r}",
            details={"constraint_surface_id": constraint_surface_id},
        )


class ConstraintSurfaceHashInvalidError(PromptAssemblyError):
    """ERR_CONSTRAINT_SURFACE_HASH_INVALID — declared constraint surface hash failed verification."""

    def __init__(self, constraint_surface_id: str) -> None:
        super().__init__(
            ErrorCode.CONSTRAINT_SURFACE_HASH_INVALID,
            f"Constraint surface hash invalid: {constraint_surface_id!r}",
            details={"constraint_surface_id": constraint_surface_id},
        )


class RequiredStaleInputError(PromptAssemblyError):
    """ERR_REQUIRED_STALE_INPUT — an input the profile required is stale and cannot be used."""

    def __init__(self, input_id: str) -> None:
        super().__init__(
            ErrorCode.REQUIRED_STALE_INPUT,
            f"Required input is stale: {input_id!r}",
            details={"input_id": input_id},
        )


class ProtectedBudgetImpossibleError(PromptAssemblyError):
    """ERR_PROTECTED_BUDGET_IMPOSSIBLE — protected sections cannot fit the token budget."""

    def __init__(self, requested: int, available: int) -> None:
        super().__init__(
            ErrorCode.PROTECTED_BUDGET_IMPOSSIBLE,
            f"Protected budget impossible: requested {requested}, available {available}",
            details={"requested": requested, "available": available},
        )


class SectionConflictUnresolvedError(PromptAssemblyError):
    """ERR_SECTION_CONFLICT_UNRESOLVED — section ordering or content conflict could not be resolved."""

    def __init__(self, section_ids: list[str]) -> None:
        super().__init__(
            ErrorCode.SECTION_CONFLICT_UNRESOLVED,
            f"Section conflict unresolved among: {section_ids!r}",
            details={"section_ids": section_ids},
        )


class BundleVersionIncompatibleError(PromptAssemblyError):
    """ERR_BUNDLE_VERSION_INCOMPATIBLE — bundle/consumer version mismatch detected."""

    def __init__(self, bundle_version: str, consumer_min: str) -> None:
        super().__init__(
            ErrorCode.BUNDLE_VERSION_INCOMPATIBLE,
            f"Bundle version {bundle_version!r} below consumer minimum {consumer_min!r}",
            details={"bundle_version": bundle_version, "consumer_min": consumer_min},
        )


class BundleSignatureInvalidError(PromptAssemblyError):
    """ERR_BUNDLE_SIGNATURE_INVALID — bundle signature verification failed.

    Phase 0 does not yet sign bundles, but the error code is locked so future
    signature-enforcement phases can adopt it without churn.
    """

    def __init__(self, bundle_id: str) -> None:
        super().__init__(
            ErrorCode.BUNDLE_SIGNATURE_INVALID,
            f"Bundle signature invalid for bundle_id={bundle_id!r}",
            details={"bundle_id": bundle_id},
        )


__all__ = [
    "ErrorCode",
    "ERROR_CODE_VALUES",
    "ErrorEnvelope",
    "PromptAssemblyError",
    "ProfileUnknownError",
    "ProfileInactiveError",
    "LaneUnsupportedLocalError",
    "ProfileLaneIncompatibleError",
    "RequiredReferenceUnresolvedError",
    "RequiredConstraintSurfaceMissingError",
    "ConstraintSurfaceHashInvalidError",
    "RequiredStaleInputError",
    "ProtectedBudgetImpossibleError",
    "SectionConflictUnresolvedError",
    "BundleVersionIncompatibleError",
    "BundleSignatureInvalidError",
]
