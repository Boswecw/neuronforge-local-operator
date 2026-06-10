"""Identity tests (plan 09): stable ids, NFC, order independence, collisions."""

import pytest

from nlo_experiment_memory.identity import (
    canonical_json,
    edge_id,
    node_id,
    normalize_timestamp,
)
from nlo_experiment_memory.projection.backends import InMemoryGraphStore, NodeCollision


def test_node_id_stable_across_calls():
    first = node_id("Run", "run-2026-03-13-005")
    second = node_id("Run", "run-2026-03-13-005")
    assert first == second
    assert len(first) == 64


def test_node_id_distinct_for_distinct_keys():
    assert node_id("Run", "run-2026-03-13-005") != node_id("Run", "run-2026-03-13-016")
    assert node_id("Run", "run-2026-03-13-005") != node_id("Evaluation", "run-2026-03-13-005")


def test_unicode_nfc_normalization():
    composed = "café"          # é as one codepoint
    decomposed = "café"       # e + combining acute
    assert composed != decomposed
    assert node_id("ModelVersion", composed) == node_id("ModelVersion", decomposed)
    assert canonical_json({"name": composed}) == canonical_json({"name": decomposed})


def test_property_order_independence():
    a = {"model_id": "qwen2.5:14b", "run_id": "run-x", "status": "succeeded"}
    b = {"status": "succeeded", "run_id": "run-x", "model_id": "qwen2.5:14b"}
    assert canonical_json(a) == canonical_json(b)


def test_set_like_arrays_sorted():
    a = {"evidence_record_ids": ["b", "a", "c"]}
    b = {"evidence_record_ids": ["c", "a", "b"]}
    assert canonical_json(a) == canonical_json(b)


def test_ordered_arrays_preserved():
    a = {"findings": ["first", "second"]}
    b = {"findings": ["second", "first"]}
    assert canonical_json(a) != canonical_json(b)


def test_timestamp_normalization():
    assert normalize_timestamp("2026-03-13T19:00:00Z") == "2026-03-13T19:00:00Z"
    assert normalize_timestamp("2026-03-13T20:00:00+01:00") == "2026-03-13T19:00:00Z"
    assert normalize_timestamp("2026-03-13T19:00:00+00:00") == "2026-03-13T19:00:00Z"
    assert normalize_timestamp("2026-03-13T19:00:00.500000Z") == "2026-03-13T19:00:00.5Z"
    assert canonical_json({"occurred_at": "2026-03-13T20:00:00+01:00"}) == canonical_json(
        {"occurred_at": "2026-03-13T19:00:00Z"}
    )


def test_edge_id_uniqueness():
    run_node = node_id("Run", "run-2026-03-13-005")
    contract_node = node_id("TaskContractVersion", "proofread.lore_safe.v1")
    base = edge_id("BECAME_BASELINE_FOR", run_node, contract_node,
                   "decision-001", "2026-03-13T19:00:00Z")
    assert base == edge_id("BECAME_BASELINE_FOR", run_node, contract_node,
                           "decision-001", "2026-03-13T20:00:00+01:00")
    assert base != edge_id("BECAME_BASELINE_FOR", run_node, contract_node,
                           "decision-002", "2026-03-13T19:00:00Z")
    assert base != edge_id("BECAME_BASELINE_FOR", run_node, contract_node,
                           "decision-001", "2026-06-10T15:30:00Z")
    assert base != edge_id("SUPERSEDED", run_node, contract_node,
                           "decision-001", "2026-03-13T19:00:00Z")


def test_collision_detection():
    store = InMemoryGraphStore()
    node = {"node_id": "abc", "entity_type": "Run", "business_key": "run-x",
            "properties": {"run_id": "run-x"}, "provenance": {"source_record_id": "run-x"}}
    store.upsert_nodes([node])
    store.upsert_nodes([node])  # identical replay is idempotent
    mutated = dict(node, properties={"run_id": "run-y"})
    with pytest.raises(NodeCollision):
        store.upsert_nodes([mutated])
