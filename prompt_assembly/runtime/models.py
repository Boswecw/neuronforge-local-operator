"""Pydantic v2 runtime models for NeuronForge Local prompt assembly (Phase 0).

These models mirror the JSON contracts under ``prompt_assembly/contracts/``
exactly. Any divergence is a bug — see ``prompt_assembly/tests/`` for the
parity checks.

Phase 0 only locks the *shape*. None of these models contain assembly logic.
The presence of a model does not imply the assembler that produces it exists.
"""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

# ---------------------------------------------------------------------------
# Locked baselines (Phase 0)
# ---------------------------------------------------------------------------

#: Single canonical contract version string for every Phase 0 artifact.
CONTRACT_VERSION: Literal["1.1.0-phase0"] = "1.1.0-phase0"

#: Phase 0 hash algorithm baseline.
HASH_ALGORITHM_BASELINE: Literal["blake3"] = "blake3"

#: Phase 0 structured-content serialization baseline.
SERIALIZATION_FORMAT_BASELINE: Literal["canonical_json"] = "canonical_json"

#: Phase 0 bundle signature algorithm baseline.
SIGNATURE_ALGORITHM_BASELINE: Literal["ed25519"] = "ed25519"


# ---------------------------------------------------------------------------
# Controlled enums
# ---------------------------------------------------------------------------


class LaneId(str, Enum):
    """Long-context lane identifiers supported in V1.1 local execution.

    LC-3 and LC-5 are intentionally absent: they are not standard supported
    local execution lanes in V1.1. Requests for them must raise
    ``ERR_LANE_UNSUPPORTED_LOCAL`` rather than be modeled here.
    """

    LC_1 = "LC-1"
    LC_2 = "LC-2"
    LC_4 = "LC-4"


class TrustLevel(str, Enum):
    AUTHORITATIVE = "authoritative"
    TRUSTED_RUNTIME = "trusted_runtime"
    DERIVED = "derived"
    UNTRUSTED = "untrusted"


class ConstraintType(str, Enum):
    PATCH_CONTRACT = "patch_contract"
    WORKSPACE_BOUNDARY = "workspace_boundary"
    EVIDENCE_BUNDLE = "evidence_bundle"
    ACCEPTANCE_CRITERIA = "acceptance_criteria"
    AUTHORITY_BOUNDARY = "authority_boundary"
    LIFECYCLE_BOUNDARY = "lifecycle_boundary"


class HashAlgorithm(str, Enum):
    BLAKE3 = "blake3"


class SerializationFormat(str, Enum):
    CANONICAL_JSON = "canonical_json"


class SignatureAlgorithm(str, Enum):
    ED25519 = "ed25519"


class ReasonCode(str, Enum):
    SUMMARY_LOSSY = "summary_lossy"
    SLIDING_WINDOW_LOSSY = "sliding_window_lossy"
    GOVERNANCE_CONTINUITY_REQUIRED = "governance_continuity_required"
    FULL_TRACE_REQUIRED = "full_trace_required"
    PARTITIONED_EXECUTION_REQUIRED = "partitioned_execution_required"
    AMNESIA_FORBIDDEN = "amnesia_forbidden"
    DEGRADED_LANE_FALLBACK = "degraded_lane_fallback"


class PolicyDecision(str, Enum):
    ADMIT = "admit"
    REJECT = "reject"
    REQUIRE_REVIEW = "require_review"


class CompactionEventKind(str, Enum):
    SUMMARY_SYNTHESIZED = "summary_synthesized"
    WINDOW_TRUNCATED = "window_truncated"
    SECTION_DROPPED = "section_dropped"
    SECTION_DEMOTED = "section_demoted"
    NO_COMPACTION = "no_compaction"


class TokenizerId(str, Enum):
    QWEN25_BPE = "qwen2.5-bpe"
    PHI4_BPE = "phi4-bpe"
    LLAMA3_BPE = "llama3-bpe"


# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

NonEmptyStr = Annotated[str, StringConstraints(min_length=1)]

_HASH_RE = re.compile(r"^[0-9a-f]{16,128}$")
HashHex = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{16,128}$")]

_SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")
SemVer = Annotated[str, StringConstraints(pattern=r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")]


# ---------------------------------------------------------------------------
# Base config
# ---------------------------------------------------------------------------


class _LockedModel(BaseModel):
    """Base config for every Phase 0 model: strict, frozen, forbids extras."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        validate_assignment=True,
        use_enum_values=False,
    )


class _ContractVersionedModel(_LockedModel):
    """Adds the locked contract_version / schema_version constant."""


# ---------------------------------------------------------------------------
# LongContext
# ---------------------------------------------------------------------------


class LongContextModel(_ContractVersionedModel):
    """Normalized long-context lane assignment.

    Always present, never inferred downstream, and treated as immutable.
    Phase 0 supports only LC-1, LC-2, and LC-4.
    """

    lane: LaneId
    reason_codes: tuple[ReasonCode, ...] = Field(min_length=1)
    summary_allowed: bool
    sliding_window_allowed: bool
    full_trace_required: bool
    governance_no_amnesia: bool
    partitioned_execution: bool
    degraded: bool
    contract_version: Literal["1.1.0-phase0"] = CONTRACT_VERSION

    @field_validator("reason_codes")
    @classmethod
    def _unique_reason_codes(cls, value: tuple[ReasonCode, ...]) -> tuple[ReasonCode, ...]:
        if len(set(value)) != len(value):
            raise ValueError("reason_codes must be unique")
        return value


# ---------------------------------------------------------------------------
# ConstraintSurface
# ---------------------------------------------------------------------------


class ConstraintSurfaceModel(_ContractVersionedModel):
    """Typed, hashed, source-attributed constraint object."""

    constraint_surface_id: NonEmptyStr
    schema_version: Literal["1.1.0-phase0"] = CONTRACT_VERSION
    authoritative: bool
    constraint_type: ConstraintType
    items: tuple[dict[str, Any], ...] = Field(min_length=1)
    source_refs: tuple[NonEmptyStr, ...] = Field(min_length=1)
    trust_level: TrustLevel
    created_at: datetime
    hash: HashHex
    hash_algorithm: HashAlgorithm
    serialization_format: SerializationFormat

    @field_validator("source_refs")
    @classmethod
    def _unique_source_refs(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("source_refs must be unique")
        return value

    @model_validator(mode="after")
    def _trust_authority_coherence(self) -> "ConstraintSurfaceModel":
        if self.trust_level in (TrustLevel.UNTRUSTED, TrustLevel.DERIVED) and self.authoritative:
            raise ValueError(
                f"trust_level={self.trust_level.value!r} cannot be authoritative"
            )
        return self


# ---------------------------------------------------------------------------
# PromptAssemblyInput
# ---------------------------------------------------------------------------


class PromptAssemblyInputModel(_ContractVersionedModel):
    """Caller-facing assembly request envelope."""

    schema_version: Literal["1.1.0-phase0"] = CONTRACT_VERSION
    profile_id: NonEmptyStr
    lane_request: LaneId
    constraint_surface_refs: tuple[NonEmptyStr, ...] = Field(default_factory=tuple)
    long_context: LongContextModel
    submitted_at: datetime
    caller_metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("constraint_surface_refs")
    @classmethod
    def _unique_refs(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("constraint_surface_refs must be unique")
        return value


# ---------------------------------------------------------------------------
# Resolver / policy / compaction sub-records
# ---------------------------------------------------------------------------


class ResolverEnvelopeModel(_LockedModel):
    """Descriptor for a resolved input as recorded in the manifest."""

    input_id: NonEmptyStr
    trust_level: TrustLevel
    hash: HashHex
    hash_algorithm: HashAlgorithm
    stale: bool


class PolicyDecisionModel(_LockedModel):
    """A single admit/reject/require_review event the policy layer rendered."""

    decision_id: NonEmptyStr
    subject: NonEmptyStr
    decision: PolicyDecision
    rationale_code: NonEmptyStr


class CompactionEventModel(_LockedModel):
    """A single compaction event recorded against an assembled section."""

    event_id: NonEmptyStr
    kind: CompactionEventKind
    section_id: NonEmptyStr
    tokens_before: int = Field(ge=0)
    tokens_after: int = Field(ge=0)


# ---------------------------------------------------------------------------
# PromptAssemblyManifest
# ---------------------------------------------------------------------------


class PromptAssemblyManifestModel(_ContractVersionedModel):
    """Runtime-truth manifest produced by the assembler.

    Records actual decisions, not intended ones. Phase 0 locks the field set;
    populating it from real assembler events is later-phase work.
    """

    manifest_id: NonEmptyStr
    schema_version: Literal["1.1.0-phase0"] = CONTRACT_VERSION
    profile_id: NonEmptyStr
    tokenizer_id: TokenizerId
    tokenizer_version: NonEmptyStr
    long_context: LongContextModel
    constraint_surfaces: tuple[ConstraintSurfaceModel, ...]
    resolved_inputs: tuple[ResolverEnvelopeModel, ...]
    policy_decisions: tuple[PolicyDecisionModel, ...]
    compaction_events: tuple[CompactionEventModel, ...]
    section_order: tuple[NonEmptyStr, ...]
    section_token_counts: dict[str, int]
    protected_budget_tokens: int = Field(ge=0)
    total_token_count: int = Field(ge=0)
    assembled_at: datetime
    assembler_version: NonEmptyStr
    redaction_policy_id: NonEmptyStr

    @field_validator("section_token_counts")
    @classmethod
    def _non_negative_counts(cls, value: dict[str, int]) -> dict[str, int]:
        for k, v in value.items():
            if not k:
                raise ValueError("section_token_counts keys must be non-empty")
            if v < 0:
                raise ValueError(f"section_token_counts[{k!r}] must be >= 0")
        return value

    @model_validator(mode="after")
    def _section_keys_match_order(self) -> "PromptAssemblyManifestModel":
        order_set = set(self.section_order)
        count_set = set(self.section_token_counts.keys())
        if order_set != count_set:
            missing = order_set - count_set
            extra = count_set - order_set
            raise ValueError(
                f"section_token_counts keys must match section_order "
                f"(missing={sorted(missing)}, extra={sorted(extra)})"
            )
        return self


# ---------------------------------------------------------------------------
# CompiledBundle
# ---------------------------------------------------------------------------


class _BundleSignature(_LockedModel):
    algorithm: SignatureAlgorithm
    key_id: str  # may be empty in Phase 0
    value: str  # may be empty in Phase 0
    signed: bool


class _BundleCompatibility(_LockedModel):
    min_consumer_version: SemVer
    min_tokenizer_version: NonEmptyStr
    tokenizer_id: TokenizerId


class CompiledBundleModel(_ContractVersionedModel):
    """Format contract for the artifact handed to a model executor."""

    bundle_id: NonEmptyStr
    bundle_version: SemVer
    schema_version: Literal["1.1.0-phase0"] = CONTRACT_VERSION
    manifest_id: NonEmptyStr
    serialization_format: SerializationFormat
    content_hash: HashHex
    content_hash_algorithm: HashAlgorithm
    signature: _BundleSignature
    compatibility: _BundleCompatibility
    created_at: datetime
    body: dict[str, Any]


# ---------------------------------------------------------------------------
# RedactionPolicy
# ---------------------------------------------------------------------------


class _TrustEffect(_LockedModel):
    force_masked: tuple[NonEmptyStr, ...] = Field(default_factory=tuple)
    force_reference_only: tuple[NonEmptyStr, ...] = Field(default_factory=tuple)


class _TrustLevelEffects(_LockedModel):
    authoritative: _TrustEffect
    trusted_runtime: _TrustEffect
    derived: _TrustEffect
    untrusted: _TrustEffect


class RedactionPolicyModel(_ContractVersionedModel):
    redaction_policy_id: NonEmptyStr
    schema_version: Literal["1.1.0-phase0"] = CONTRACT_VERSION
    manifest_visible_fields: tuple[NonEmptyStr, ...]
    debug_visible_fields: tuple[NonEmptyStr, ...]
    masked_fields: tuple[NonEmptyStr, ...]
    reference_only_fields: tuple[NonEmptyStr, ...]
    trust_level_effects: _TrustLevelEffects

    @field_validator(
        "manifest_visible_fields",
        "debug_visible_fields",
        "masked_fields",
        "reference_only_fields",
    )
    @classmethod
    def _unique_field_lists(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("redaction policy field lists must be unique")
        return value


# ---------------------------------------------------------------------------
# ErrorEnvelope re-export (kept on this module for symmetry with the plan)
# ---------------------------------------------------------------------------

from prompt_assembly.runtime.errors import ErrorEnvelope as ErrorEnvelopeModel  # noqa: E402,F401


__all__ = [
    "CONTRACT_VERSION",
    "HASH_ALGORITHM_BASELINE",
    "SERIALIZATION_FORMAT_BASELINE",
    "SIGNATURE_ALGORITHM_BASELINE",
    "LaneId",
    "TrustLevel",
    "ConstraintType",
    "HashAlgorithm",
    "SerializationFormat",
    "SignatureAlgorithm",
    "ReasonCode",
    "PolicyDecision",
    "CompactionEventKind",
    "TokenizerId",
    "LongContextModel",
    "ConstraintSurfaceModel",
    "PromptAssemblyInputModel",
    "ResolverEnvelopeModel",
    "PolicyDecisionModel",
    "CompactionEventModel",
    "PromptAssemblyManifestModel",
    "CompiledBundleModel",
    "RedactionPolicyModel",
    "ErrorEnvelopeModel",
]
