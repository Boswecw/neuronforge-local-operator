"""Schema and registry loading plus strict record validation.

Schemas are the JSON Schema files in schemas/experiment_memory/ (authority: Git).
Records are dispatched on their declared schema_version; unsupported versions
raise UnsupportedSchemaVersion so the projector can quarantine them.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import jsonschema

REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMAS_DIR = REPO_ROOT / "schemas" / "experiment_memory"
REGISTRIES_DIR = SCHEMAS_DIR / "registries"


class UnsupportedSchemaVersion(ValueError):
    pass


def _load_json(path: Path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


class SchemaRegistry:
    """Loads record-type registry and exposes per-schema-version validators."""

    def __init__(self, schemas_dir: Path = SCHEMAS_DIR):
        self.schemas_dir = schemas_dir
        self.registries_dir = schemas_dir / "registries"
        self.record_types = _load_json(self.registries_dir / "experiment-record-type.v1.json")
        self.failure_taxonomy = _load_json(self.registries_dir / "failure-taxonomy.v1.json")
        self.experiment_status = _load_json(self.registries_dir / "experiment-status.v1.json")
        self.graph_entity_types = _load_json(self.registries_dir / "graph-entity-type.v1.json")
        self.graph_relationship_types = _load_json(
            self.registries_dir / "graph-relationship-type.v1.json"
        )
        self.projection_status = _load_json(self.registries_dir / "projection-status.v1.json")
        self.graph_health_status = _load_json(self.registries_dir / "graph-health-status.v1.json")

        self._by_schema_version = {}
        self._validators = {}
        for entry in self.record_types["entries"]:
            schema = _load_json(schemas_dir / entry["schema_file"])
            validator = jsonschema.Draft202012Validator(schema)
            self._by_schema_version[entry["schema_version"]] = entry
            self._validators[entry["schema_version"]] = validator

    @property
    def supported_schema_versions(self):
        return set(self._by_schema_version)

    def record_type_entry(self, schema_version: str) -> dict:
        try:
            return self._by_schema_version[schema_version]
        except KeyError:
            raise UnsupportedSchemaVersion(
                f"unsupported schema version: {schema_version!r}"
            ) from None

    def record_id(self, record: dict) -> str:
        entry = self.record_type_entry(record.get("schema_version"))
        return record[entry["id_field"]]

    def record_type(self, record: dict) -> str:
        return self.record_type_entry(record.get("schema_version"))["record_type"]

    def validate(self, record: dict) -> list[str]:
        """Return a list of schema-validation error messages (empty when valid)."""
        schema_version = record.get("schema_version")
        if schema_version not in self._validators:
            raise UnsupportedSchemaVersion(
                f"unsupported schema version: {schema_version!r}"
            )
        validator = self._validators[schema_version]
        errors = []
        for error in sorted(validator.iter_errors(record), key=lambda e: list(e.absolute_path)):
            location = "/".join(str(part) for part in error.absolute_path) or "<root>"
            errors.append(f"{location}: {error.message}")
        return errors

    def taxonomy_classes(self, taxonomy_version: str) -> set[str]:
        if taxonomy_version != self.failure_taxonomy["taxonomy_version"]:
            raise UnsupportedSchemaVersion(
                f"unsupported failure taxonomy version: {taxonomy_version!r}"
            )
        return set(self.failure_taxonomy["classes"])


@lru_cache(maxsize=1)
def registry() -> SchemaRegistry:
    return SchemaRegistry()


RECORD_TYPE_BY_SCHEMA_VERSION = {
    "nlo-run-record-v1": "run",
    "nlo-evaluation-record-v1": "evaluation",
    "nlo-failure-observation-v1": "failure_observation",
    "nlo-operator-decision-v1": "operator_decision",
    "nlo-hardware-profile-v1": "hardware_profile",
    "nlo-experiment-event-v1": "experiment_event",
}


def validate_record(record: dict) -> list[str]:
    return registry().validate(record)
