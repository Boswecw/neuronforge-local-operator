from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schemas" / "skill_optimization"


class SchemaValidationError(ValueError):
    """Raised when a skill-optimization record fails schema validation."""

    def __init__(self, schema_name: str, errors: list[str]) -> None:
        self.schema_name = schema_name
        self.errors = errors
        super().__init__(f"{schema_name} validation failed: {'; '.join(errors)}")


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / schema_name
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def validation_errors(instance: dict[str, Any], schema_name: str) -> list[str]:
    errors = sorted(validator(schema_name).iter_errors(instance), key=lambda e: list(e.path))
    return [format_error(error) for error in errors]


def validate_instance(instance: dict[str, Any], schema_name: str) -> None:
    errors = validation_errors(instance, schema_name)
    if errors:
        raise SchemaValidationError(schema_name, errors)


def format_error(error: Any) -> str:
    path = ".".join(str(part) for part in error.path)
    if path:
        return f"{path}: {error.message}"
    return error.message
