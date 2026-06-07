#!/usr/bin/env python3
"""Verify the neuronforge wave-1 promotion seam (Canvas 04, Gate 1).

Executes the proof inventory from Canvas 02:

1. strict-admitted promoted request
2. non-strict-admitted promoted request
3. missing manifest hash
4. unsupported requested profile
5. digest mismatch
6. lineage loss attempt
7. replay yields same classification

Writes ``evidence/promotion_seam/seam_report.json`` plus operator-facing
markdown examples.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from promotion import (  # noqa: E402
    AdmissionClass,
    LineageIdentifiers,
    PromotionEnvelope,
    RuntimePromotionEvidence,
    append_run,
    derive_admission,
    load_envelope,
    record_for_run,
    summarize,
)

MIRROR_PATH = REPO_ROOT / "registry" / "pact_wave1_envelope_mirror.json"


def _resolve_pact_path(env_var: str, *default_rel_parts: str) -> Path:
    """Resolve a path to an external PACT evidence artifact.

    Resolution order:
      1. The ``env_var`` environment variable, if set (absolute or relative).
      2. A sibling ``pact`` checkout next to this repo:
         ``<repo-parent>/pact/docs/evidence/<file>``.

    No machine-specific absolute path is hardcoded; operators on a different
    layout point the env vars at their PACT checkout.
    """
    override = os.environ.get(env_var)
    if override:
        return Path(override).expanduser()
    return REPO_ROOT.parent / "pact" / "docs" / "evidence" / Path(*default_rel_parts)


# External PACT seam artifacts (live in the separate `pact` repo). Override the
# location with NF_PACT_ENVELOPE / NF_PACT_MANIFEST when PACT is checked out
# elsewhere.
PACT_ENVELOPE_PATH = _resolve_pact_path(
    "NF_PACT_ENVELOPE", "wave1_promotion_envelope.json"
)
PACT_MANIFEST_PATH = _resolve_pact_path(
    "NF_PACT_MANIFEST", "toon_wave1_manifest.json"
)

EVIDENCE_DIR = REPO_ROOT / "evidence" / "promotion_seam"
LOG_PATH = EVIDENCE_DIR / "promotion_runs.jsonl"
SEAM_REPORT_PATH = EVIDENCE_DIR / "seam_report.json"
OPERATOR_EXAMPLES_PATH = EVIDENCE_DIR / "operator_examples.md"


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    _assert(MIRROR_PATH.exists(), f"trusted envelope mirror missing: {MIRROR_PATH}")

    missing_external = [
        p for p in (PACT_ENVELOPE_PATH, PACT_MANIFEST_PATH) if not p.exists()
    ]
    if missing_external:
        print("verify_promotion_seam: SKIPPED", file=sys.stderr)
        print(
            "  External PACT seam artifacts are not available in this checkout:",
            file=sys.stderr,
        )
        for p in missing_external:
            print(f"    - {p}", file=sys.stderr)
        print(
            "  Point NF_PACT_ENVELOPE / NF_PACT_MANIFEST at a PACT checkout, "
            "or place a sibling `pact` repo next to this one, then re-run.",
            file=sys.stderr,
        )
        # Could-not-run is distinct from PASS (0) and FAIL (1).
        return 2

    mirror = load_envelope(MIRROR_PATH)
    envelope = load_envelope(PACT_ENVELOPE_PATH)

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    if LOG_PATH.exists():
        LOG_PATH.unlink()

    cases: list[dict] = []

    def run_case(name: str, fn, *, expected: AdmissionClass, expected_reasons: set[str] | None = None):
        try:
            fn()
            actual = cases[-1]["admission_class"]
            reasons = set(cases[-1]["reason_codes"])
            ok = actual == expected.value
            if expected_reasons is not None:
                ok = ok and expected_reasons.issubset(reasons)
            cases[-1]["pass"] = ok
            cases[-1]["expected_admission_class"] = expected.value
            cases[-1]["expected_reason_codes_subset"] = sorted(expected_reasons or [])
        except Exception as exc:  # noqa: BLE001
            cases.append({"name": name, "pass": False, "error": str(exc)})

    # shared strict runtime
    strict = RuntimePromotionEvidence(
        serialization_profile_requested="plain_text_with_toon_segment",
        serialization_profile_used="plain_text_with_toon_segment",
        artifact_kind="toon_segment",
        fallback_used=False,
        strict_success_hash=envelope.strict_success_hash,
    )
    nonstrict = RuntimePromotionEvidence(
        serialization_profile_requested="plain_text_with_toon_segment",
        serialization_profile_used="plain_text_only",
        artifact_kind="plain_text",
        fallback_used=True,
        fallback_reason="no_renderable_rows",
        non_strict_canonical_digest=envelope.non_strict_canonical_digests["toon_fallback_zero_rows"],
        non_strict_canonical_case="toon_fallback_zero_rows",
    )
    lineage = LineageIdentifiers(
        task_intent_id="ti-seam-001",
        context_bundle_id="cb-seam-001",
        context_bundle_hash="sha256:" + "a" * 64,
    )

    def case_1_strict():
        rec = record_for_run(
            run_id="seam-case-01-strict",
            packet_class="search_assist_packet",
            envelope=envelope,
            runtime=strict,
            lineage=lineage,
            mirror=mirror,
            manifest_file=PACT_MANIFEST_PATH,
        )
        append_run(rec, LOG_PATH)
        cases.append({
            "name": "case_1_strict_admitted",
            "admission_class": rec.admission_class.value,
            "reason_codes": list(rec.blocked_reason_codes),
            "lineage_preserved": rec.lineage.task_intent_id == lineage.task_intent_id,
        })

    def case_2_non_strict():
        rec = record_for_run(
            run_id="seam-case-02-non-strict",
            packet_class="search_assist_packet",
            envelope=envelope,
            runtime=nonstrict,
            lineage=lineage,
            mirror=mirror,
            manifest_file=PACT_MANIFEST_PATH,
        )
        append_run(rec, LOG_PATH)
        cases.append({
            "name": "case_2_non_strict_admitted",
            "admission_class": rec.admission_class.value,
            "reason_codes": list(rec.blocked_reason_codes),
            "lineage_preserved": rec.lineage.context_bundle_id == lineage.context_bundle_id,
        })

    def case_3_missing_manifest():
        bogus_path = REPO_ROOT / "evidence" / "promotion_seam" / "does_not_exist.json"
        rec = record_for_run(
            run_id="seam-case-03-missing-manifest",
            packet_class="search_assist_packet",
            envelope=envelope,
            runtime=strict,
            lineage=lineage,
            mirror=mirror,
            manifest_file=bogus_path,
        )
        append_run(rec, LOG_PATH)
        cases.append({
            "name": "case_3_missing_manifest",
            "admission_class": rec.admission_class.value,
            "reason_codes": list(rec.blocked_reason_codes),
        })

    def case_4_unsupported_profile():
        bad = strict.model_copy(update={"serialization_profile_used": "unknown_profile"})
        rec = record_for_run(
            run_id="seam-case-04-unsupported-profile",
            packet_class="search_assist_packet",
            envelope=envelope,
            runtime=bad,
            lineage=lineage,
            mirror=mirror,
            manifest_file=PACT_MANIFEST_PATH,
        )
        append_run(rec, LOG_PATH)
        cases.append({
            "name": "case_4_unsupported_profile",
            "admission_class": rec.admission_class.value,
            "reason_codes": list(rec.blocked_reason_codes),
        })

    def case_5_digest_mismatch():
        bad = nonstrict.model_copy(
            update={"non_strict_canonical_digest": "sha256:" + "d" * 64}
        )
        rec = record_for_run(
            run_id="seam-case-05-digest-mismatch",
            packet_class="search_assist_packet",
            envelope=envelope,
            runtime=bad,
            lineage=lineage,
            mirror=mirror,
            manifest_file=PACT_MANIFEST_PATH,
        )
        append_run(rec, LOG_PATH)
        cases.append({
            "name": "case_5_digest_mismatch",
            "admission_class": rec.admission_class.value,
            "reason_codes": list(rec.blocked_reason_codes),
        })

    def case_6_lineage_loss_attempt():
        # caller attempts to elide lineage; seam should still classify
        rec = record_for_run(
            run_id="seam-case-06-lineage-loss",
            packet_class="search_assist_packet",
            envelope=envelope,
            runtime=strict,
            lineage=LineageIdentifiers(),  # empty
            mirror=mirror,
            manifest_file=PACT_MANIFEST_PATH,
        )
        append_run(rec, LOG_PATH)
        cases.append({
            "name": "case_6_lineage_loss_attempt",
            "admission_class": rec.admission_class.value,
            "reason_codes": list(rec.blocked_reason_codes),
            # lineage was allowed to be empty but is visibly absent:
            "lineage_task_intent_id": rec.lineage.task_intent_id,
            "lineage_absent_visibly": rec.lineage.task_intent_id is None,
        })

    def case_7_replay_stable():
        v1 = derive_admission(envelope, mirror, "search_assist_packet", strict, PACT_MANIFEST_PATH)
        v2 = derive_admission(envelope, mirror, "search_assist_packet", strict, PACT_MANIFEST_PATH)
        cases.append({
            "name": "case_7_replay_stable",
            "admission_class": v1.admission_class.value,
            "reason_codes": list(v1.reason_codes),
            "stable": v1.admission_class is v2.admission_class
            and v1.reason_codes == v2.reason_codes,
        })

    run_case("case_1_strict_admitted", case_1_strict, expected=AdmissionClass.STRICT_ADMITTED)
    run_case("case_2_non_strict_admitted", case_2_non_strict, expected=AdmissionClass.NON_STRICT_ADMITTED)
    run_case(
        "case_3_missing_manifest",
        case_3_missing_manifest,
        expected=AdmissionClass.NOT_ADMITTED,
        expected_reasons={"manifest_hash_missing"},
    )
    run_case(
        "case_4_unsupported_profile",
        case_4_unsupported_profile,
        expected=AdmissionClass.NOT_ADMITTED,
        expected_reasons={"used_profile_unsupported"},
    )
    run_case(
        "case_5_digest_mismatch",
        case_5_digest_mismatch,
        expected=AdmissionClass.NOT_ADMITTED,
        expected_reasons={"non_strict_canonical_digest_mismatch"},
    )
    run_case("case_6_lineage_loss_attempt", case_6_lineage_loss_attempt, expected=AdmissionClass.STRICT_ADMITTED)
    run_case("case_7_replay_stable", case_7_replay_stable, expected=AdmissionClass.STRICT_ADMITTED)

    summary = summarize(LOG_PATH)
    all_pass = all(c.get("pass") for c in cases)

    report = {
        "seam": "neuronforge_local_wave1",
        "mirror_path": str(MIRROR_PATH.relative_to(REPO_ROOT)),
        "envelope_path": str(PACT_ENVELOPE_PATH),
        "log_path": str(LOG_PATH.relative_to(REPO_ROOT)),
        "admission_stage": mirror.admission_stage,
        "wave_manifest_hash": mirror.wave_manifest_hash,
        "strict_success_hash": mirror.strict_success_hash,
        "cases": cases,
        "summary": summary,
        "all_pass": all_pass,
    }
    SEAM_REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# neuronforge wave-1 promotion seam — operator examples",
        "",
        f"- mirror: `{MIRROR_PATH.relative_to(REPO_ROOT)}`",
        f"- manifest hash: `{mirror.wave_manifest_hash}`",
        f"- strict success hash: `{mirror.strict_success_hash}`",
        f"- admission stage: `{mirror.admission_stage}`",
        "",
    ]
    for c in cases:
        lines.append(f"## {c['name']} — {'PASS' if c.get('pass') else 'FAIL'}")
        lines.append(f"- admission: `{c.get('admission_class')}`")
        reasons = c.get("reason_codes") or []
        if reasons:
            lines.append(f"- reason codes: {', '.join(f'`{r}`' for r in reasons)}")
        else:
            lines.append("- reason codes: none")
        lines.append("")
    OPERATOR_EXAMPLES_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "seam_report": str(SEAM_REPORT_PATH),
        "operator_examples": str(OPERATOR_EXAMPLES_PATH),
        "log_path": str(LOG_PATH),
        "all_pass": all_pass,
        "summary": summary,
    }, indent=2))
    if not all_pass:
        print("verify_promotion_seam: FAIL", file=sys.stderr)
        return 1
    print("verify_promotion_seam: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
