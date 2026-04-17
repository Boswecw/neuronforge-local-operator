"""Validate the prompt-assembly registry against Phase 0 contract truth.

Phase 0 scope: this tool only proves the registry is *coherent* with the
locked contract surface. It does not assemble bundles, resolve inputs, or
contact any model. It is the script that backs::

    nf-local prompt-assembly registry validate

Checks performed:

1. Every JSON contract in ``prompt_assembly/contracts/`` parses as valid
   JSON Schema (Draft 2020-12).
2. The Phase 0 error-code enum in ``common_enums.schema.json`` exactly
   matches :class:`prompt_assembly.runtime.errors.ErrorCode`.
3. ``config/defaults.yaml`` declares only supported lanes (LC-1, LC-2, LC-4)
   and pins a tokenizer for every active profile.
4. Every active profile's ``supported_lanes`` is a subset of the registry's
   global ``supported_lanes``.

Exit codes:
    0  registry is valid
    1  registry has at least one Phase 0 violation
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from prompt_assembly.runtime.errors import ERROR_CODE_VALUES

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPT_ASSEMBLY_ROOT = REPO_ROOT / "prompt_assembly"
CONTRACTS_DIR = PROMPT_ASSEMBLY_ROOT / "contracts"
DEFAULTS_PATH = PROMPT_ASSEMBLY_ROOT / "config" / "defaults.yaml"

CONTRACT_FILES = (
    "common_enums.schema.json",
    "long_context.schema.json",
    "constraint_surface.schema.json",
    "prompt_assembly_input.schema.json",
    "prompt_assembly_manifest.schema.json",
    "compiled_bundle.schema.json",
    "redaction_policy.schema.json",
)

SUPPORTED_LANES = ("LC-1", "LC-2", "LC-4")
UNSUPPORTED_LOCAL_LANES = ("LC-3", "LC-5")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_contract_files(errors: list[str]) -> dict[str, dict[str, Any]]:
    """Parse and check every contract file. Return loaded schemas by filename."""
    loaded: dict[str, dict[str, Any]] = {}
    for name in CONTRACT_FILES:
        path = CONTRACTS_DIR / name
        if not path.exists():
            errors.append(f"missing contract file: {name}")
            continue
        try:
            schema = _load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{name}: invalid JSON: {exc}")
            continue
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001 — surface meta-schema failure cleanly
            errors.append(f"{name}: invalid JSON Schema: {exc}")
            continue
        loaded[name] = schema
    return loaded


def validate_error_code_parity(
    common_enums: dict[str, Any], errors: list[str]
) -> None:
    enum_values = (
        common_enums.get("$defs", {}).get("error_code", {}).get("enum")
    )
    if not isinstance(enum_values, list):
        errors.append("common_enums.schema.json: missing $defs.error_code.enum")
        return
    schema_set = tuple(enum_values)
    runtime_set = ERROR_CODE_VALUES
    if schema_set != runtime_set:
        only_schema = sorted(set(schema_set) - set(runtime_set))
        only_runtime = sorted(set(runtime_set) - set(schema_set))
        errors.append(
            "error code enum drift: "
            f"only_in_schema={only_schema}, only_in_runtime={only_runtime}"
        )


def validate_defaults(defaults: dict[str, Any], errors: list[str]) -> None:
    declared_lanes = tuple(defaults.get("supported_lanes", ()))
    if declared_lanes != SUPPORTED_LANES:
        errors.append(
            "defaults.yaml supported_lanes drift: "
            f"expected {list(SUPPORTED_LANES)}, got {list(declared_lanes)}"
        )

    unsupported = tuple(defaults.get("unsupported_local_lanes", ()))
    if set(unsupported) != set(UNSUPPORTED_LOCAL_LANES):
        errors.append(
            "defaults.yaml unsupported_local_lanes drift: "
            f"expected {list(UNSUPPORTED_LOCAL_LANES)}, got {list(unsupported)}"
        )

    profiles = defaults.get("profiles", {})
    if not isinstance(profiles, dict) or not profiles:
        errors.append("defaults.yaml: profiles section is missing or empty")
        return

    for profile_id, body in profiles.items():
        if not isinstance(body, dict):
            errors.append(f"profile {profile_id!r}: must be a mapping")
            continue
        if "active" not in body:
            errors.append(f"profile {profile_id!r}: missing 'active'")
            continue
        if not body["active"]:
            continue
        # Active profiles MUST pin lane allow list and tokenizer.
        lanes = body.get("supported_lanes")
        if not isinstance(lanes, list) or not lanes:
            errors.append(
                f"active profile {profile_id!r}: missing or empty supported_lanes"
            )
        else:
            stray = sorted(set(lanes) - set(SUPPORTED_LANES))
            if stray:
                errors.append(
                    f"active profile {profile_id!r}: declares unsupported lanes "
                    f"{stray}"
                )
        if not body.get("tokenizer_id"):
            errors.append(
                f"active profile {profile_id!r}: missing tokenizer_id"
            )
        if not body.get("tokenizer_version"):
            errors.append(
                f"active profile {profile_id!r}: missing tokenizer_version"
            )


def main(argv: list[str] | None = None) -> int:
    errors: list[str] = []
    loaded = validate_contract_files(errors)
    common = loaded.get("common_enums.schema.json")
    if common is not None:
        validate_error_code_parity(common, errors)

    if not DEFAULTS_PATH.exists():
        errors.append("config/defaults.yaml is missing")
    else:
        try:
            defaults = _load_yaml(DEFAULTS_PATH)
        except yaml.YAMLError as exc:
            errors.append(f"defaults.yaml: invalid YAML: {exc}")
            defaults = None
        if isinstance(defaults, dict):
            validate_defaults(defaults, errors)

    if errors:
        print("prompt-assembly registry validation FAILED:", file=sys.stderr)
        for line in errors:
            print(f"  - {line}", file=sys.stderr)
        return 1

    print("prompt-assembly registry: OK (Phase 0 contract lock)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
