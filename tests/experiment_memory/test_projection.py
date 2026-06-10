"""Projection tests (plan 09): deterministic rebuild, quarantine, replay, provenance."""

import hashlib
import json
import shutil

from nlo_experiment_memory.projection.backends import InMemoryGraphStore
from nlo_experiment_memory.projection.projector import prove_rebuild, rebuild


def _dir_digest(path):
    digest = hashlib.sha256()
    for file in sorted(path.rglob("*.json")):
        digest.update(file.name.encode())
        digest.update(file.read_bytes())
    return digest.hexdigest()


def test_two_clean_rebuilds_are_provenance_equal(records_dir):
    proof = prove_rebuild(records_dir)
    assert proof["provenance_equal"] is True
    assert proof["fingerprint_a"] == proof["fingerprint_b"]
    assert proof["duplicate_canonical_identities"] == 0


def test_fingerprint_matches_frozen_value(records_dir, golden_dir):
    """Mapping-mutation guard: changing the mapping, identity rules, or the
    fixture set changes this fingerprint and must be a deliberate, reviewed
    update of golden/fingerprint.txt."""
    frozen = (golden_dir / "fingerprint.txt").read_text(encoding="utf-8").strip()
    result = rebuild(records_dir)
    assert result.report["fingerprint"] == frozen


def test_rebuild_never_touches_canonical_records(records_dir):
    before = _dir_digest(records_dir)
    rebuild(records_dir)
    assert _dir_digest(records_dir) == before


def test_duplicate_replay_is_idempotent(records_dir):
    backend = InMemoryGraphStore()
    first = rebuild(records_dir, backend=backend)
    nodes_after_first = len(backend.nodes)
    edges_after_first = len(backend.edges)
    second = rebuild(records_dir, backend=backend)  # replay into same backend
    assert len(backend.nodes) == nodes_after_first
    assert len(backend.edges) == edges_after_first
    assert first.report["fingerprint"] == second.report["fingerprint"]


def test_every_node_and_edge_preserves_source_references(records_dir):
    result = rebuild(records_dir)
    record_ids = set()
    from nlo_experiment_memory.stores.fixture_store import FixtureStore

    record_ids = set(FixtureStore(records_dir).records)
    required = ("source_record_id", "source_record_type", "source_schema_version",
                "source_content_hash", "source_store", "recorded_at")
    for item in result.export["nodes"] + result.export["edges"]:
        provenance = item["provenance"]
        for field in required:
            assert provenance.get(field), (item, field)
        assert provenance["source_record_id"] in record_ids


def test_unsupported_schema_version_quarantined(records_dir, invalid_dir, tmp_path):
    workdir = tmp_path / "records"
    shutil.copytree(records_dir, workdir)
    shutil.copy(invalid_dir / "run-unsupported-schema.json", workdir)
    result = rebuild(workdir)
    assert result.report["projection_status"] == "partial"
    reasons = [reason for entry in result.report["quarantined"] for reason in entry["reasons"]]
    assert any("unsupported schema version" in reason for reason in reasons)


def test_invalid_record_quarantined_and_sources_unchanged(records_dir, invalid_dir, tmp_path):
    workdir = tmp_path / "records"
    shutil.copytree(records_dir, workdir)
    shutil.copy(invalid_dir / "run-bad-hash.json", workdir)
    before = _dir_digest(workdir)
    result = rebuild(workdir)
    assert result.report["projection_status"] == "partial"
    quarantined_ids = {entry["record"] for entry in result.report["quarantined"]}
    assert "run-invalid-bad-hash" in quarantined_ids
    # quarantine must not leak into the graph
    run_ids = {
        node["properties"]["run_id"]
        for node in result.export["nodes"]
        if node["entity_type"] == "Run"
    }
    assert "run-invalid-bad-hash" not in run_ids
    assert _dir_digest(workdir) == before


def test_prohibited_content_quarantined(records_dir, invalid_dir, tmp_path):
    workdir = tmp_path / "records"
    shutil.copytree(records_dir, workdir)
    shutil.copy(invalid_dir / "failure-prohibited-content.json", workdir)
    result = rebuild(workdir)
    quarantined = {entry["record"]: entry["reasons"] for entry in result.report["quarantined"]}
    assert "failure-invalid-prohibited-content" in quarantined
    assert any("prohibited content" in reason
               for reason in quarantined["failure-invalid-prohibited-content"])


def test_quarantine_cascades_to_dependents(records_dir, tmp_path):
    """Breaking the baseline run quarantines it plus every record referencing it."""
    workdir = tmp_path / "records"
    shutil.copytree(records_dir, workdir)
    run_path = workdir / "run-2026-03-13-005.run.json"
    record = json.loads(run_path.read_text(encoding="utf-8"))
    record["prompt_content_hash"] = "0" * 64
    run_path.write_text(json.dumps(record), encoding="utf-8")
    result = rebuild(workdir)
    quarantined_ids = {entry["record"] for entry in result.report["quarantined"]}
    assert "run-2026-03-13-005" in quarantined_ids
    assert "eval-run-2026-03-13-005-review-01" in quarantined_ids
    assert "decision-2026-03-13-lore-safe-baseline-001" in quarantined_ids
    assert "exp-2026-03-13-005-review-01" in quarantined_ids
