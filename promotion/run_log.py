"""Promotion-aware run log.

Writes one JSON line per run to ``registry/promotion_runs.jsonl``
alongside the existing markdown run registry.  The markdown registry
remains the operator-facing audit surface; this JSONL file is the
machine-readable seam that the cloud lane and ForgeCommand consume.

Non-goals:
- this does not replace ``registry/runs.md``
- this does not gate runtime execution; it is carriage + evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

from .compatibility import (
    CompatibilityVerdict,
    derive_admission,
)
from .models import (
    AdmissionClass,
    LineageIdentifiers,
    PromotionEnvelope,
    PromotionRunRecord,
    RuntimePromotionEvidence,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_PATH = REPO_ROOT / "registry" / "promotion_runs.jsonl"


def record_for_run(
    run_id: str,
    packet_class: str,
    envelope: Optional[PromotionEnvelope],
    runtime: RuntimePromotionEvidence,
    lineage: LineageIdentifiers | None = None,
    mirror: Optional[PromotionEnvelope] = None,
    manifest_file: Optional[Path] = None,
    repo_gate_report_path: Optional[str] = None,
) -> PromotionRunRecord:
    """Build a ``PromotionRunRecord`` with admission derived by NF-02."""
    verdict = derive_admission(
        envelope=envelope,
        mirror=mirror,
        packet_class=packet_class,
        runtime=runtime,
        manifest_file=manifest_file,
    )
    if envelope is None:
        raise ValueError(
            "cannot record a promotion run without an envelope; "
            "log non-promoted runs in registry/runs.md instead"
        )
    return PromotionRunRecord(
        run_id=run_id,
        occurred_at=PromotionRunRecord.utcnow_iso(),
        packet_class=packet_class,
        envelope=envelope,
        lineage=lineage or LineageIdentifiers(),
        runtime=runtime,
        admission_class=verdict.admission_class,
        blocked_reason_codes=list(verdict.reason_codes),
        operator_review_state="not_reviewed",
        repo_gate_report_path=repo_gate_report_path,
    )


def append_run(record: PromotionRunRecord, log_path: Path = DEFAULT_LOG_PATH) -> Path:
    """Append a JSON line for ``record``.  Creates parent dirs as needed."""
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(record.model_dump_json() + "\n")
    return log_path


def iter_runs(log_path: Path = DEFAULT_LOG_PATH) -> Iterable[PromotionRunRecord]:
    """Yield validated records from the JSONL log."""
    log_path = Path(log_path)
    if not log_path.exists():
        return
    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        data = json.loads(line)
        yield PromotionRunRecord(**data)


def summarize(log_path: Path = DEFAULT_LOG_PATH) -> dict:
    """Produce a class-count summary, preserving Canvas 01 admission labels."""
    counts: dict[str, int] = {c.value: 0 for c in AdmissionClass}
    reason_counts: dict[str, int] = {}
    total = 0
    for record in iter_runs(log_path):
        counts[record.admission_class.value] += 1
        for code in record.blocked_reason_codes:
            reason_counts[code] = reason_counts.get(code, 0) + 1
        total += 1
    return {
        "log_path": str(log_path),
        "total_runs": total,
        "admission_class_counts": counts,
        "reason_code_counts": reason_counts,
    }
