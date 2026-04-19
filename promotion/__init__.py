"""neuronforge promotion seam.

This package carries PACT-owned wave-1 promotion truth into the local
operator surface. It does not redefine TOON wave-1 serialization,
fallback, or admission rules — PACT is the upstream authority. The
modules here only:

- carry the promotion envelope,
- classify intake compatibility,
- log admission posture against neuronforge runs.
"""

from .compatibility import (
    CompatibilityVerdict,
    ReasonCode,
    classify_runtime,
    derive_admission,
    envelope_matches_local_mirror,
    load_envelope,
    manifest_file_matches_envelope,
)
from .models import (
    AdmissionClass,
    LineageIdentifiers,
    PromotionEnvelope,
    PromotionRunRecord,
    RuntimePromotionEvidence,
)
from .run_log import (
    DEFAULT_LOG_PATH,
    append_run,
    iter_runs,
    record_for_run,
    summarize,
)

__all__ = [
    "AdmissionClass",
    "CompatibilityVerdict",
    "DEFAULT_LOG_PATH",
    "LineageIdentifiers",
    "PromotionEnvelope",
    "PromotionRunRecord",
    "ReasonCode",
    "RuntimePromotionEvidence",
    "append_run",
    "classify_runtime",
    "derive_admission",
    "envelope_matches_local_mirror",
    "iter_runs",
    "load_envelope",
    "manifest_file_matches_envelope",
    "record_for_run",
    "summarize",
]
