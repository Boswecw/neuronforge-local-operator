"""Cross-record integrity, temporal sanity, hash verification, ingestion filter.

Covers the referential-integrity and clock-skew rules in plans 04 and 06 and
the ingestion filter in plan 05. Anything JSON Schema cannot express lives here.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path

from ..identity.normalize import normalize_timestamp
from .loader import REPO_ROOT, SchemaRegistry, registry

# Plan 05 ingestion filter: reject episodes containing secrets, auth material,
# token-bearing URLs, or bulk content that smells like manuscript ingestion.
_SECRET_PATTERNS = [
    re.compile(r"(?i)\bauthorization\s*:\s*bearer\b"),
    re.compile(r"(?i)\bapi[_-]?key\b\s*[:=]"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)[?&](token|access_token|api_key|key)=[A-Za-z0-9._-]{8,}"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
]
# Longest legitimate free-text field allowed by the schemas is 2000 chars;
# anything larger indicates bulk content (e.g. manuscript text) being smuggled in.
_MAX_STRING_LENGTH = 2000


def _iter_strings(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from _iter_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_strings(child)
    elif isinstance(value, str):
        yield value


def ingestion_filter_violations(record: dict) -> list[str]:
    violations = []
    for text in _iter_strings(record):
        if len(text) > _MAX_STRING_LENGTH:
            violations.append(
                f"string value exceeds {_MAX_STRING_LENGTH} chars (possible bulk/manuscript content)"
            )
            continue
        for pattern in _SECRET_PATTERNS:
            if pattern.search(text):
                violations.append(f"prohibited content matches {pattern.pattern!r}")
    return violations


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(normalize_timestamp(ts).replace("Z", "+00:00"))


class IntegrityChecker:
    """Validates referential integrity and temporal order across a record set.

    `records` maps record_id -> record (already schema-valid). Returns a dict
    record_id -> list of error strings; offending records are quarantined by
    the projector, sources stay unchanged.
    """

    def __init__(self, records: dict[str, dict], schema_registry: SchemaRegistry | None = None,
                 repo_root: Path = REPO_ROOT, verify_artifact_hashes: bool = True):
        self.records = records
        self.registry = schema_registry or registry()
        self.repo_root = repo_root
        self.verify_artifact_hashes = verify_artifact_hashes
        self.by_type: dict[str, dict[str, dict]] = {}
        for record_id, record in records.items():
            record_type = self.registry.record_type(record)
            self.by_type.setdefault(record_type, {})[record_id] = record

    def _runs(self):
        return self.by_type.get("run", {})

    def check(self) -> dict[str, list[str]]:
        problems: dict[str, list[str]] = {}

        def add(record_id: str, message: str):
            problems.setdefault(record_id, []).append(message)

        for record_id, record in self.records.items():
            record_type = self.registry.record_type(record)
            checker = getattr(self, f"_check_{record_type}", None)
            if checker is not None:
                for message in checker(record):
                    add(record_id, message)
            for message in ingestion_filter_violations(record):
                add(record_id, message)
        return problems

    # --- per-type checks ---------------------------------------------------

    def _check_run(self, run: dict):
        errors = []
        if _parse(run["recorded_at"]) < _parse(run["occurred_at"]):
            errors.append("recorded_at precedes occurred_at")
        hardware_id = run.get("hardware_profile_id")
        if hardware_id and hardware_id not in self.by_type.get("hardware_profile", {}):
            errors.append(f"hardware_profile_id does not resolve: {hardware_id}")
        errors.extend(self._verify_hash(run, "prompt_path", "prompt_content_hash"))
        errors.extend(self._verify_hash(run, "input_path", "input_content_hash"))
        errors.extend(self._verify_hash(run, "output_path", "output_content_hash"))
        return errors

    def _check_evaluation(self, evaluation: dict):
        errors = []
        run = self._runs().get(evaluation["run_id"])
        if run is None:
            errors.append(f"run_id does not resolve: {evaluation['run_id']}")
        else:
            if _parse(evaluation["reviewed_at"]) < _parse(run["occurred_at"]):
                errors.append("reviewed_at precedes the run's occurred_at")
        if _parse(evaluation["recorded_at"]) < _parse(evaluation["reviewed_at"]):
            errors.append("recorded_at precedes reviewed_at")
        return errors

    def _check_failure_observation(self, failure: dict):
        errors = []
        try:
            classes = self.registry.taxonomy_classes(failure["taxonomy_version"])
        except Exception as exc:
            return [str(exc)]
        if failure["failure_class"] not in classes:
            errors.append(
                f"failure_class {failure['failure_class']!r} not in "
                f"{failure['taxonomy_version']}"
            )
        run_id = failure.get("run_id")
        evaluation_id = failure.get("evaluation_id")
        run = self._runs().get(run_id) if run_id else None
        if run_id and run is None:
            errors.append(f"run_id does not resolve: {run_id}")
        if evaluation_id and evaluation_id not in self.by_type.get("evaluation", {}):
            errors.append(f"evaluation_id does not resolve: {evaluation_id}")
        if run is not None and _parse(failure["observed_at"]) < _parse(run["occurred_at"]):
            errors.append("observed_at precedes the run's occurred_at")
        if _parse(failure["recorded_at"]) < _parse(failure["observed_at"]):
            errors.append("recorded_at precedes observed_at")
        return errors

    def _check_operator_decision(self, decision: dict):
        errors = []
        run = self._runs().get(decision["target_run_id"])
        if run is None:
            errors.append(f"target_run_id does not resolve: {decision['target_run_id']}")
        elif _parse(decision["effective_at"]) < _parse(run["occurred_at"]):
            errors.append("decision references a future run (effective_at precedes occurred_at)")
        supersedes = decision.get("supersedes_run_id")
        if supersedes:
            if supersedes == decision["target_run_id"]:
                errors.append("baseline supersedes itself")
            elif supersedes not in self._runs():
                errors.append(f"supersedes_run_id does not resolve: {supersedes}")
        superseded_at = decision.get("superseded_at")
        if superseded_at is not None and _parse(superseded_at) <= _parse(decision["effective_at"]):
            errors.append("superseded_at does not follow effective_at")
        for evidence_id in decision["evidence_record_ids"]:
            if evidence_id not in self.records:
                errors.append(f"evidence record does not resolve: {evidence_id}")
        return errors

    def _check_hardware_profile(self, profile: dict):
        errors = []
        if _parse(profile["recorded_at"]) < _parse(profile["captured_at"]):
            errors.append("recorded_at precedes captured_at")
        return errors

    def _check_experiment_event(self, event: dict):
        errors = []
        references = {
            "run_record_id": "run",
            "evaluation_record_id": "evaluation",
            "decision_record_id": "operator_decision",
            "hardware_profile_id": "hardware_profile",
        }
        for field, record_type in references.items():
            value = event.get(field)
            if value and value not in self.by_type.get(record_type, {}):
                errors.append(f"{field} does not resolve: {value}")
        for failure_id in event["failure_observation_ids"]:
            if failure_id not in self.by_type.get("failure_observation", {}):
                errors.append(f"failure observation does not resolve: {failure_id}")
        run = self._runs().get(event["run_record_id"])
        if run is not None and _parse(event["observed_at"]) < _parse(run["occurred_at"]):
            errors.append("observed_at precedes the run's occurred_at")
        return errors

    # --- helpers -----------------------------------------------------------

    def _verify_hash(self, record: dict, path_field: str, hash_field: str):
        """Verify an artifact hash against the repo file when the file exists.

        Missing files are not an error here (canonical artifacts may live on
        the operator host); wrong hashes against present files always are.
        """
        if not self.verify_artifact_hashes:
            return []
        path_value = record.get(path_field)
        hash_value = record.get(hash_field)
        if not path_value or not hash_value:
            return []
        artifact = self.repo_root / path_value
        if not artifact.is_file():
            return []
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        if digest != hash_value:
            return [
                f"{hash_field} does not match canonical content of {path_value} "
                f"(expected {digest})"
            ]
        return []
