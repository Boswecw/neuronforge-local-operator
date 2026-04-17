"""Phase 0 JSON Schema validity and fixture-conformance tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from prompt_assembly.tests.fixtures import builders

CONTRACTS_DIR = Path(__file__).resolve().parents[1] / "contracts"

SCHEMA_FILES = (
    "common_enums.schema.json",
    "long_context.schema.json",
    "constraint_surface.schema.json",
    "prompt_assembly_input.schema.json",
    "prompt_assembly_manifest.schema.json",
    "compiled_bundle.schema.json",
    "redaction_policy.schema.json",
)


def _load(name: str) -> dict:
    with (CONTRACTS_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture(scope="module")
def schemas() -> dict[str, dict]:
    return {name: _load(name) for name in SCHEMA_FILES}


@pytest.fixture(scope="module")
def registry(schemas: dict[str, dict]) -> Registry:
    """Build a referencing Registry that resolves cross-file $ref by relative URI."""
    resources = []
    for schema in schemas.values():
        resources.append((schema["$id"], Resource(contents=schema, specification=DRAFT202012)))
    return Registry().with_resources(resources)


# Backwards-compatible fixture name used by existing tests below.
@pytest.fixture(scope="module")
def store(registry: Registry) -> Registry:
    return registry


def _validator(schema: dict, store: Registry) -> Draft202012Validator:
    return Draft202012Validator(schema, registry=store)


@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_files_are_valid_jsonschema(name: str, schemas: dict[str, dict]) -> None:
    Draft202012Validator.check_schema(schemas[name])


def test_long_context_fixture_is_valid(schemas, store) -> None:
    validator = _validator(schemas["long_context.schema.json"], store)
    validator.validate(builders.long_context())


def test_constraint_surface_fixture_is_valid(schemas, store) -> None:
    validator = _validator(schemas["constraint_surface.schema.json"], store)
    validator.validate(builders.constraint_surface())


def test_prompt_assembly_input_fixture_is_valid(schemas, store) -> None:
    validator = _validator(schemas["prompt_assembly_input.schema.json"], store)
    validator.validate(builders.prompt_assembly_input())


def test_prompt_assembly_manifest_fixture_is_valid(schemas, store) -> None:
    validator = _validator(schemas["prompt_assembly_manifest.schema.json"], store)
    validator.validate(builders.prompt_assembly_manifest())


def test_compiled_bundle_fixture_is_valid(schemas, store) -> None:
    validator = _validator(schemas["compiled_bundle.schema.json"], store)
    validator.validate(builders.compiled_bundle())


def test_redaction_policy_fixture_is_valid(schemas, store) -> None:
    validator = _validator(schemas["redaction_policy.schema.json"], store)
    validator.validate(builders.redaction_policy())


# --- Negative cases ---------------------------------------------------------


def test_long_context_rejects_unsupported_lane(schemas, store) -> None:
    validator = _validator(schemas["long_context.schema.json"], store)
    bad = builders.long_context()
    bad["lane"] = "LC-5"  # reserved but unsupported in V1.1
    assert not validator.is_valid(bad)


def test_long_context_rejects_unknown_lane(schemas, store) -> None:
    validator = _validator(schemas["long_context.schema.json"], store)
    bad = builders.long_context()
    bad["lane"] = "LC-99"
    assert not validator.is_valid(bad)


def test_long_context_requires_all_locked_fields(schemas, store) -> None:
    validator = _validator(schemas["long_context.schema.json"], store)
    required = (
        "lane",
        "reason_codes",
        "summary_allowed",
        "sliding_window_allowed",
        "full_trace_required",
        "governance_no_amnesia",
        "partitioned_execution",
        "degraded",
        "contract_version",
    )
    for field in required:
        bad = builders.long_context()
        del bad[field]
        assert not validator.is_valid(bad), f"missing {field} should fail"


def test_constraint_surface_rejects_unknown_trust_level(schemas, store) -> None:
    validator = _validator(schemas["constraint_surface.schema.json"], store)
    bad = builders.constraint_surface()
    bad["trust_level"] = "rumored"
    assert not validator.is_valid(bad)


def test_constraint_surface_rejects_unknown_constraint_type(schemas, store) -> None:
    validator = _validator(schemas["constraint_surface.schema.json"], store)
    bad = builders.constraint_surface()
    bad["constraint_type"] = "vibe_alignment"
    assert not validator.is_valid(bad)


def test_constraint_surface_requires_all_locked_fields(schemas, store) -> None:
    validator = _validator(schemas["constraint_surface.schema.json"], store)
    required = (
        "constraint_surface_id",
        "schema_version",
        "authoritative",
        "constraint_type",
        "items",
        "source_refs",
        "trust_level",
        "created_at",
        "hash",
        "hash_algorithm",
        "serialization_format",
    )
    for field in required:
        bad = builders.constraint_surface()
        del bad[field]
        assert not validator.is_valid(bad), f"missing {field} should fail"


def test_constraint_surface_rejects_untrusted_authoritative(schemas, store) -> None:
    validator = _validator(schemas["constraint_surface.schema.json"], store)
    bad = builders.constraint_surface()
    bad["trust_level"] = "untrusted"
    bad["authoritative"] = True
    assert not validator.is_valid(bad)


def test_compiled_bundle_rejects_bad_semver(schemas, store) -> None:
    validator = _validator(schemas["compiled_bundle.schema.json"], store)
    bad = builders.compiled_bundle()
    bad["bundle_version"] = "v0.1"
    assert not validator.is_valid(bad)


def test_compiled_bundle_requires_signature_block(schemas, store) -> None:
    validator = _validator(schemas["compiled_bundle.schema.json"], store)
    bad = builders.compiled_bundle()
    del bad["signature"]
    assert not validator.is_valid(bad)
