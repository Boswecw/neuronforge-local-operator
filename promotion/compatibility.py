"""Compatibility checker for the wave-1 promotion seam.

Inputs: a PACT-emitted promotion envelope, the local trusted-mirror
envelope, and the per-run runtime evidence.

Outputs: an ``AdmissionClass`` and an explicit list of fail-closed
reason codes.  This module never coerces a partial envelope into
``strict_admitted`` — it is the explicit gate that Canvas 02 NF-02
requires.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .models import (
    AdmissionClass,
    PromotionEnvelope,
    RuntimePromotionEvidence,
)

_SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


# Fail-closed reason codes, mirroring Canvas 05 fail-closed rules.
class ReasonCode:
    MANIFEST_HASH_MISSING = "manifest_hash_missing"
    MANIFEST_HASH_MISMATCH = "manifest_hash_mismatch"
    MANIFEST_VERSION_UNSUPPORTED = "manifest_version_unsupported"
    PACKET_CLASS_UNSUPPORTED = "packet_class_unsupported"
    REQUESTED_PROFILE_UNSUPPORTED = "requested_profile_unsupported"
    USED_PROFILE_UNSUPPORTED = "used_profile_unsupported"
    STRICT_HASH_MISSING = "strict_hash_missing"
    STRICT_HASH_MISMATCH = "strict_hash_mismatch"
    NON_STRICT_DIGEST_MISSING = "non_strict_canonical_digest_missing"
    NON_STRICT_DIGEST_MISMATCH = "non_strict_canonical_digest_mismatch"
    FALLBACK_REASON_UNSUPPORTED = "fallback_reason_unsupported"
    FEATURE_FLAG_MISMATCH = "feature_flag_mismatch"
    LINEAGE_HASH_INVALID = "lineage_hash_invalid"
    SOURCE_HASH_DRIFT = "source_hash_drift"


@dataclass(frozen=True)
class CompatibilityVerdict:
    admission_class: AdmissionClass
    reason_codes: tuple[str, ...]
    posture: str

    def to_dict(self) -> dict:
        return {
            "admission_class": self.admission_class.value,
            "reason_codes": list(self.reason_codes),
            "posture": self.posture,
        }


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load_envelope(path: Path) -> PromotionEnvelope:
    """Load a promotion envelope JSON file into a validated model."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return PromotionEnvelope(**data)


def envelope_matches_local_mirror(
    envelope: PromotionEnvelope,
    mirror: PromotionEnvelope,
) -> tuple[bool, list[str]]:
    """Compare the inbound envelope against the locally-mirrored trusted copy.

    Returns ``(ok, reasons)``. We treat the mirror as the operator-trusted
    snapshot of PACT truth; every load-bearing field must match exactly.
    """
    reasons: list[str] = []
    if envelope.wave_manifest_hash != mirror.wave_manifest_hash:
        reasons.append(ReasonCode.MANIFEST_HASH_MISMATCH)
    if envelope.promotion_packet_version != mirror.promotion_packet_version:
        reasons.append(ReasonCode.MANIFEST_VERSION_UNSUPPORTED)
    if envelope.strict_success_hash != mirror.strict_success_hash:
        reasons.append(ReasonCode.STRICT_HASH_MISMATCH)
    if envelope.non_strict_canonical_digests != mirror.non_strict_canonical_digests:
        reasons.append(ReasonCode.NON_STRICT_DIGEST_MISMATCH)
    if envelope.feature_flag_name != mirror.feature_flag_name:
        reasons.append(ReasonCode.FEATURE_FLAG_MISMATCH)
    if set(envelope.allowed_packet_classes) != set(mirror.allowed_packet_classes):
        reasons.append(ReasonCode.PACKET_CLASS_UNSUPPORTED)
    return (not reasons, reasons)


def manifest_file_matches_envelope(
    envelope: PromotionEnvelope,
    manifest_path: Path,
) -> tuple[bool, list[str]]:
    """Verify the file-on-disk hash matches the envelope's wave_manifest_hash."""
    reasons: list[str] = []
    if not manifest_path.exists():
        return False, [ReasonCode.MANIFEST_HASH_MISSING]
    actual = _sha256(manifest_path)
    if actual != envelope.wave_manifest_hash:
        reasons.append(ReasonCode.SOURCE_HASH_DRIFT)
    return (not reasons, reasons)


def classify_runtime(
    envelope: PromotionEnvelope,
    packet_class: str,
    runtime: RuntimePromotionEvidence,
) -> CompatibilityVerdict:
    """Classify a single runtime execution against admitted PACT truth."""
    reasons: list[str] = []

    if packet_class not in envelope.allowed_packet_classes:
        reasons.append(ReasonCode.PACKET_CLASS_UNSUPPORTED)

    if runtime.serialization_profile_requested not in envelope.supported_requested_profiles:
        reasons.append(ReasonCode.REQUESTED_PROFILE_UNSUPPORTED)

    if runtime.serialization_profile_used not in envelope.supported_used_profiles:
        reasons.append(ReasonCode.USED_PROFILE_UNSUPPORTED)

    if (
        runtime.fallback_used
        and runtime.fallback_reason not in envelope.fallback_reason_codes
    ):
        reasons.append(ReasonCode.FALLBACK_REASON_UNSUPPORTED)

    is_strict_shape = (
        not runtime.fallback_used
        and runtime.artifact_kind == "toon_segment"
        and runtime.serialization_profile_used == "plain_text_with_toon_segment"
    )
    if is_strict_shape:
        if runtime.strict_success_hash is None:
            reasons.append(ReasonCode.STRICT_HASH_MISSING)
        elif runtime.strict_success_hash != envelope.strict_success_hash:
            reasons.append(ReasonCode.STRICT_HASH_MISMATCH)

    is_non_strict_shape = not is_strict_shape and (
        runtime.artifact_kind == "plain_text"
        or runtime.fallback_used
    )
    if is_non_strict_shape:
        if runtime.non_strict_canonical_digest is None:
            reasons.append(ReasonCode.NON_STRICT_DIGEST_MISSING)
        else:
            expected = (
                envelope.non_strict_canonical_digests.get(runtime.non_strict_canonical_case)
                if runtime.non_strict_canonical_case
                else None
            )
            if expected is None or expected != runtime.non_strict_canonical_digest:
                reasons.append(ReasonCode.NON_STRICT_DIGEST_MISMATCH)

    if reasons:
        return CompatibilityVerdict(
            admission_class=AdmissionClass.NOT_ADMITTED,
            reason_codes=tuple(reasons),
            posture="promotion_blocked",
        )

    if is_strict_shape:
        return CompatibilityVerdict(
            admission_class=AdmissionClass.STRICT_ADMITTED,
            reason_codes=(),
            posture="promotion_compatible",
        )
    return CompatibilityVerdict(
        admission_class=AdmissionClass.NON_STRICT_ADMITTED,
        reason_codes=(),
        posture="promotion_compatible",
    )


def derive_admission(
    envelope: Optional[PromotionEnvelope],
    mirror: Optional[PromotionEnvelope],
    packet_class: str,
    runtime: Optional[RuntimePromotionEvidence],
    manifest_file: Optional[Path] = None,
) -> CompatibilityVerdict:
    """High-level admission derivation used by the run logger.

    Honours the Canvas 02 boundary: missing envelope => ``not_promoted``,
    mismatch => ``not_admitted`` with explicit reason codes.
    """
    if envelope is None:
        return CompatibilityVerdict(
            admission_class=AdmissionClass.NOT_PROMOTED,
            reason_codes=(),
            posture="not_promoted",
        )

    reasons: list[str] = []
    if mirror is not None:
        ok, mirror_reasons = envelope_matches_local_mirror(envelope, mirror)
        if not ok:
            reasons.extend(mirror_reasons)

    if manifest_file is not None:
        ok, manifest_reasons = manifest_file_matches_envelope(envelope, manifest_file)
        if not ok:
            reasons.extend(manifest_reasons)

    if reasons:
        return CompatibilityVerdict(
            admission_class=AdmissionClass.NOT_ADMITTED,
            reason_codes=tuple(reasons),
            posture="promotion_blocked",
        )

    if runtime is None:
        return CompatibilityVerdict(
            admission_class=AdmissionClass.NOT_ADMITTED,
            reason_codes=(ReasonCode.STRICT_HASH_MISSING,),
            posture="promotion_blocked",
        )

    return classify_runtime(envelope, packet_class, runtime)
