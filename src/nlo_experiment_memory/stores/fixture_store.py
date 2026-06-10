"""Read-only store over committed canonical record fixtures (JSON files).

This is the pilot's canonical record source (authority: Git) until DataForge
Local exists. The store never writes; rebuild recovery needs only these files,
the deterministic mapping code, and the pinned graph schema version (plan 02).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from ..contracts.loader import SchemaRegistry, UnsupportedSchemaVersion, registry
from ..identity.normalize import normalize_timestamp

# Envelopes are excluded from watermarks: they are projection inputs,
# not authoritative domain records (plan 06).
AUTHORITATIVE_RECORD_TYPES = frozenset(
    {"run", "evaluation", "failure_observation", "operator_decision", "hardware_profile"}
)


class DuplicateRecordId(ValueError):
    pass


@dataclass(frozen=True)
class LoadedRecord:
    record_id: str
    record_type: str
    source_path: str
    record: dict


@dataclass(frozen=True)
class UnclassifiedRecord:
    """A file whose schema_version is unsupported; quarantined by the projector."""

    source_path: str
    schema_version: str | None
    record: dict


class FixtureStore:
    def __init__(self, records_dir: Path | str, schema_registry: SchemaRegistry | None = None):
        self.records_dir = Path(records_dir)
        self.registry = schema_registry or registry()
        self.records: dict[str, LoadedRecord] = {}
        self.unclassified: list[UnclassifiedRecord] = []
        self._load()

    def _load(self):
        if not self.records_dir.is_dir():
            raise FileNotFoundError(f"records directory not found: {self.records_dir}")
        for path in sorted(self.records_dir.rglob("*.json")):
            with open(path, encoding="utf-8") as handle:
                record = json.load(handle)
            relative = str(path.relative_to(self.records_dir))
            try:
                record_id = self.registry.record_id(record)
                record_type = self.registry.record_type(record)
            except UnsupportedSchemaVersion:
                self.unclassified.append(
                    UnclassifiedRecord(relative, record.get("schema_version"), record)
                )
                continue
            if record_id in self.records:
                raise DuplicateRecordId(
                    f"duplicate record id {record_id!r} "
                    f"({self.records[record_id].source_path} and {relative})"
                )
            self.records[record_id] = LoadedRecord(record_id, record_type, relative, record)

    def by_type(self, record_type: str) -> dict[str, dict]:
        return {
            loaded.record_id: loaded.record
            for loaded in self.records.values()
            if loaded.record_type == record_type
        }

    def as_plain_dict(self) -> dict[str, dict]:
        return {loaded.record_id: loaded.record for loaded in self.records.values()}

    def source_high_watermark(self) -> str | None:
        """Max recorded_at across authoritative records (quarantined-or-not)."""
        latest: datetime | None = None
        latest_text: str | None = None
        for loaded in self.records.values():
            if loaded.record_type not in AUTHORITATIVE_RECORD_TYPES:
                continue
            text = normalize_timestamp(loaded.record["recorded_at"])
            value = datetime.fromisoformat(text.replace("Z", "+00:00"))
            if latest is None or value > latest:
                latest, latest_text = value, text
        return latest_text
