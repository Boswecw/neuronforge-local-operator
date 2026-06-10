"""Operator CLI. Output order per plan 08: projection status, freshness,
supporting records, contradicting records, timeline, derived interpretation.

Subcommand names match docs/plans/graphiti/08-OPERATOR-QUERY-CONTRACTS.md.
The wrapper scripts/graph/nlo-graph forwards here with PYTHONPATH set.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from ..contracts.integrity import IntegrityChecker
from ..contracts.loader import registry
from ..projection.projector import prove_rebuild, rebuild
from ..queries.evidence import QueryRefusedError, compute_graph_status, open_queries
from ..queries.narrative import build_narrative
from ..stores.fixture_store import FixtureStore

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RECORDS_DIR = REPO_ROOT / "tests" / "fixtures" / "experiment_memory" / "records"
DEFAULT_RUNTIME_DIR = REPO_ROOT / "runtime" / "graph"


def _max_lag() -> float:
    return float(os.environ.get("NLO_GRAPH_MAX_PROJECTION_LAG_SECONDS", "0"))


def _print_evidence(evidence: dict, as_json: bool):
    if as_json:
        print(json.dumps(evidence, indent=2, ensure_ascii=False, sort_keys=True))
        return
    print(f"projection status : {evidence['graph_status']}")
    print(
        "freshness         : "
        f"source={evidence['source_high_watermark']} "
        f"projected={evidence['projected_high_watermark']} "
        f"lag={evidence['projection_lag_seconds']}s"
    )
    print(f"supporting records: {evidence['supporting_record_ids'] or '[]'}")
    print(f"contradicting     : {evidence['contradicting_record_ids'] or '[]'}")
    print("timeline          :")
    for event in evidence["timeline_events"]:
        print(f"  {event['at']}  {event['event']:<20} {event['record_id']} ({event['subject']})")
    print("interpretation    :")
    for line in build_narrative(evidence).splitlines():
        print(f"  {line}")


def cmd_validate(args) -> int:
    store = FixtureStore(args.records_dir)
    schema_registry = registry()
    problems = 0
    schema_valid = {}
    for record_id, loaded in sorted(store.records.items()):
        errors = schema_registry.validate(loaded.record)
        if errors:
            problems += 1
            print(f"INVALID {record_id} ({loaded.source_path})")
            for error in errors:
                print(f"  - {error}")
        else:
            schema_valid[record_id] = loaded.record
    for unclassified in store.unclassified:
        problems += 1
        print(f"QUARANTINE {unclassified.source_path}: unsupported schema version "
              f"{unclassified.schema_version!r}")
    integrity = IntegrityChecker(schema_valid, schema_registry).check()
    for record_id in sorted(integrity):
        problems += 1
        print(f"INTEGRITY {record_id}")
        for error in integrity[record_id]:
            print(f"  - {error}")
    total = len(store.records) + len(store.unclassified)
    if problems:
        print(f"{problems} problem record(s) out of {total}")
        return 1
    print(f"all {total} canonical records validate (schema + integrity)")
    return 0


def cmd_rebuild(args) -> int:
    result = rebuild(args.records_dir, runtime_dir=args.runtime_dir)
    report = result.report
    print(f"projection status : {report['projection_status']}")
    print(f"records           : seen={report['records_seen']} "
          f"projected={report['records_projected']} "
          f"quarantined={len(report['quarantined'])}")
    print(f"graph             : nodes={report['node_count']} edges={report['edge_count']}")
    print(f"fingerprint       : {report['fingerprint']}")
    print(f"artifacts         : {args.runtime_dir}")
    for entry in report["quarantined"]:
        print(f"  quarantined {entry['record']}: {'; '.join(entry['reasons'])}")
    if args.prove:
        proof = prove_rebuild(args.records_dir)
        print(f"rebuild proof     : fingerprint A {proof['fingerprint_a']}")
        print(f"                    fingerprint B {proof['fingerprint_b']}")
        print(f"provenance equal  : {proof['provenance_equal']}")
        if not proof["provenance_equal"]:
            return 1
    return 0 if report["projection_status"] == "complete" else 1


def cmd_status(args) -> int:
    export = report = None
    export_path = Path(args.runtime_dir) / "export.json"
    report_path = Path(args.runtime_dir) / "report.json"
    if export_path.is_file() and report_path.is_file():
        export = json.loads(export_path.read_text(encoding="utf-8"))
        report = json.loads(report_path.read_text(encoding="utf-8"))
    source_wm = None
    if Path(args.records_dir).is_dir():
        source_wm = FixtureStore(args.records_dir).source_high_watermark()
    status = compute_graph_status(export, report, source_wm, _max_lag())
    print(f"graph status      : {status.status}")
    print(f"freshness         : source={status.source_high_watermark} "
          f"projected={status.projected_high_watermark} "
          f"lag={status.projection_lag_seconds}s")
    if report is not None:
        print(f"fingerprint       : {report.get('fingerprint')}")
        print(f"last projected_at : {report.get('projected_at')}")
    for reason in status.reasons:
        print(f"  - {reason}")
    return 0 if status.status == "healthy" else 1


def _query_command(args, runner) -> int:
    try:
        queries = open_queries(args.records_dir, args.runtime_dir, _max_lag())
        evidence = runner(queries)
    except QueryRefusedError as refusal:
        print(f"REFUSED (fail closed): graph status {refusal.graph_status}")
        for reason in refusal.reasons:
            print(f"  - {reason}")
        return 1
    _print_evidence(evidence, args.json)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nlo-graph",
        description="NLO experiment-memory pilot: advisory, non-authoritative queries.",
    )
    parser.add_argument("--records-dir", default=str(DEFAULT_RECORDS_DIR),
                        help="canonical record fixtures directory")
    parser.add_argument("--runtime-dir", default=str(DEFAULT_RUNTIME_DIR),
                        help="projection artifact directory (gitignored)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="validate canonical records (schema + integrity)")
    rebuild_parser = sub.add_parser("rebuild", help="clean rebuild of the projection")
    rebuild_parser.add_argument("--prove", action="store_true",
                                help="run two rebuilds and require provenance equality")
    sub.add_parser("status", help="projection health and freshness")

    for name, help_text in [
        ("current-baseline", "current baseline for a task contract"),
        ("baseline-history", "baseline decision history for a task contract"),
        ("recurring-failures", "failure classes grouped across runs of a contract"),
    ]:
        query_parser = sub.add_parser(name, help=help_text)
        query_parser.add_argument("contract")
        query_parser.add_argument("--json", action="store_true")
        if name == "recurring-failures":
            query_parser.add_argument(
                "--include-fixtures",
                action="store_true",
                help="include fixture_modeled and synthetic_test records in trend analytics",
            )

    compare_parser = sub.add_parser("compare-runs", help="compare two runs")
    compare_parser.add_argument("run_a")
    compare_parser.add_argument("run_b")
    compare_parser.add_argument("--json", action="store_true")

    explain_parser = sub.add_parser("explain-candidate",
                                    help="evidence behind a candidate run's disposition")
    explain_parser.add_argument("candidate_id")
    explain_parser.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "validate":
        return cmd_validate(args)
    if args.command == "rebuild":
        return cmd_rebuild(args)
    if args.command == "status":
        return cmd_status(args)
    if args.command == "current-baseline":
        return _query_command(args, lambda q: q.current_baseline(args.contract))
    if args.command == "baseline-history":
        return _query_command(args, lambda q: q.baseline_history(args.contract))
    if args.command == "recurring-failures":
        return _query_command(
            args,
            lambda q: q.recurring_failures(
                args.contract, include_fixtures=args.include_fixtures
            ),
        )
    if args.command == "compare-runs":
        return _query_command(args, lambda q: q.compare_runs(args.run_a, args.run_b))
    if args.command == "explain-candidate":
        return _query_command(args, lambda q: q.explain_candidate(args.candidate_id))
    parser.error(f"unknown command {args.command!r}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
