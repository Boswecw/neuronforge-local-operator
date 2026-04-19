"""Pydantic models for the wave-1 promotion seam.

These models are the bounded *carriage* shape: they accept the PACT
promotion envelope, capture per-run lineage and admission classification,
and reject incomplete or self-invented promotion claims.

Wave-1 boundaries:
- this module never recomputes serialization truth,
- it never relaxes a missing strict hash to "good enough",
- it never invents fallback semantics.
"""

from __future__ import annotations

import datetime as _dt
import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

_SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


class AdmissionClass(str, Enum):
    """Admission classification per Canvas 01."""

    STRICT_ADMITTED = "strict_admitted"      # Class A
    NON_STRICT_ADMITTED = "non_strict_admitted"  # Class B
    NOT_ADMITTED = "not_admitted"            # Class C — block / mismatch
    NOT_PROMOTED = "not_promoted"            # no envelope present


class LineageIdentifiers(BaseModel):
    """Cross-repo lineage that must move intact through the seam."""

    model_config = ConfigDict(extra="forbid")

    task_intent_id: Optional[str] = Field(default=None, min_length=1)
    context_bundle_id: Optional[str] = Field(default=None, min_length=1)
    context_bundle_hash: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def _check_hash_shape(self) -> "LineageIdentifiers":
        if self.context_bundle_hash is not None and not _SHA256_RE.match(self.context_bundle_hash):
            raise ValueError(
                f"context_bundle_hash must match {_SHA256_RE.pattern}; "
                f"got {self.context_bundle_hash!r}"
            )
        return self


class PromotionEnvelope(BaseModel):
    """PACT-emitted wave-1 promotion envelope as carried by neuronforge.

    Field shape mirrors `pact/99-contracts/schemas/wave1_promotion_envelope.schema.json`.
    Downstream may not redefine this shape locally — adjust only by
    consuming a new envelope version emitted by PACT.
    """

    model_config = ConfigDict(extra="forbid")

    promotion_packet_version: str = Field(..., pattern=_SEMVER_RE.pattern)
    source_repo: str = Field(..., min_length=1)
    source_commit: str = Field(..., pattern=r"^[0-9a-f]{7,40}$")
    wave_manifest_path: str = Field(..., min_length=1)
    wave_manifest_hash: str = Field(..., pattern=_SHA256_RE.pattern)
    promotion_packet_path: Optional[str] = None
    promotion_packet_hash: Optional[str] = Field(default=None)
    strict_success_hash: str = Field(..., pattern=_SHA256_RE.pattern)
    non_strict_canonical_digests: dict[str, str] = Field(default_factory=dict)
    allowed_packet_classes: list[str] = Field(..., min_length=1)
    supported_requested_profiles: list[str] = Field(..., min_length=1)
    supported_used_profiles: list[str] = Field(..., min_length=1)
    fallback_reason_codes: list[str] = Field(default_factory=list)
    feature_flag_name: str = Field(..., min_length=1)
    admission_stage: str = Field(..., min_length=1)
    generated_at: str = Field(..., min_length=1)
    operator_evidence_paths: Optional[list[str]] = None
    repo_gate_report_path: Optional[str] = None
    promotion_notes: Optional[str] = None
    source_schema_versions: Optional[dict[str, str]] = None

    @model_validator(mode="after")
    def _check_digest_shape(self) -> "PromotionEnvelope":
        for name, value in self.non_strict_canonical_digests.items():
            if not _SHA256_RE.match(value):
                raise ValueError(f"non_strict_canonical_digests[{name!r}] not sha256: {value!r}")
        if self.promotion_packet_hash is not None and not _SHA256_RE.match(self.promotion_packet_hash):
            raise ValueError(f"promotion_packet_hash invalid: {self.promotion_packet_hash!r}")
        return self


class RuntimePromotionEvidence(BaseModel):
    """Per-run evidence the runtime would emit, mirroring PACT replay fields."""

    model_config = ConfigDict(extra="forbid")

    serialization_profile_requested: str = Field(..., min_length=1)
    serialization_profile_used: str = Field(..., min_length=1)
    artifact_kind: str = Field(..., min_length=1)
    fallback_used: bool
    fallback_reason: Optional[str] = None
    strict_success_hash: Optional[str] = Field(default=None)
    non_strict_canonical_digest: Optional[str] = Field(default=None)
    non_strict_canonical_case: Optional[str] = None  # which case key in envelope

    @model_validator(mode="after")
    def _check_evidence(self) -> "RuntimePromotionEvidence":
        if self.fallback_used and not self.fallback_reason:
            raise ValueError("fallback_used=True requires a fallback_reason")
        if self.strict_success_hash is not None and not _SHA256_RE.match(self.strict_success_hash):
            raise ValueError(f"strict_success_hash invalid: {self.strict_success_hash!r}")
        if (
            self.non_strict_canonical_digest is not None
            and not _SHA256_RE.match(self.non_strict_canonical_digest)
        ):
            raise ValueError(
                f"non_strict_canonical_digest invalid: {self.non_strict_canonical_digest!r}"
            )
        return self


class PromotionRunRecord(BaseModel):
    """Run-level record linking an execution to admitted PACT truth.

    This is the carriage object referenced by Canvas 02 NF-01: it stores
    the full envelope plus per-run evidence without dropping any PACT
    field that downstream evidence needs.
    """

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(..., min_length=1)
    occurred_at: str = Field(..., min_length=1)
    packet_class: str = Field(..., min_length=1)
    envelope: PromotionEnvelope
    lineage: LineageIdentifiers = Field(default_factory=LineageIdentifiers)
    runtime: RuntimePromotionEvidence
    admission_class: AdmissionClass
    blocked_reason_codes: list[str] = Field(default_factory=list)
    operator_review_state: str = Field(default="not_reviewed", min_length=1)
    repo_gate_report_path: Optional[str] = None

    @staticmethod
    def utcnow_iso() -> str:
        return _dt.datetime.now(tz=_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
