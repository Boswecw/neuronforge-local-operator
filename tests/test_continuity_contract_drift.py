"""Cross-surface contract-drift gate for the continuity-progression candidate contract.

This repo (neuronforge-local-operator) holds copies of the continuity-progression
artifacts that MUST stay aligned with the canonical pact contract:

  - scripts/validate-continuity-candidate.py   (VALID_* enum sets, now IMPORTED
    from pact_contracts; this gate proves the consumed values == the vendored schema)
  - prompts/continuity-adjacent-scene-{v1,v2,v3}.md  (operator prompt enum blocks)
  - docs/continuity-progression-candidate-schema.md   (human schema doc)

The single source of truth (SSOT) is pact's continuity_findings_packet.schema.json,
vendored in-repo at schemas/_vendor/ (committed; NOT loaded via a brittle ../../ path).

Gate quality rules enforced here:
  * FAIL CLOSED: every parse/extraction asserts NON-EMPTY before comparing, so a
    regex that silently matches nothing can never trivially "pass".
  * Enums compared as SETS (order-independent) -- the VALUES are the contract.
  * Canonical loaded from the vendored copy, not from the live pact repo.

Run:
  python3 -m pytest tests/test_continuity_contract_drift.py -v
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# The validator now CONSUMES pact_contracts (see scripts/validate-continuity-candidate.py).
# Make the colocated PACT consumable importable so this gate is self-sufficient
# within the Forge tree; a standalone checkout instead pip-installs pact_contracts
# (requirements path-dep / git-dep) and this lookup simply no-ops.
_PACT_CONTRACTS = REPO_ROOT.parent.parent / "pact" / "contracts_py"
if _PACT_CONTRACTS.is_dir() and str(_PACT_CONTRACTS) not in sys.path:
    sys.path.insert(0, str(_PACT_CONTRACTS))

VENDOR_SCHEMA = REPO_ROOT / "schemas" / "_vendor" / "continuity_findings_packet.schema.json"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate-continuity-candidate.py"
SCHEMA_DOC = REPO_ROOT / "docs" / "continuity-progression-candidate-schema.md"
PROMPTS = {
    "v1": REPO_ROOT / "prompts" / "continuity-adjacent-scene-v1.md",
    "v2": REPO_ROOT / "prompts" / "continuity-adjacent-scene-v2.md",
    "v3": REPO_ROOT / "prompts" / "continuity-adjacent-scene-v3.md",
}


# ---------------------------------------------------------------------------
# Canonical enum sets, extracted from the VENDORED pact schema (the SSOT).
# ---------------------------------------------------------------------------


def _load_canonical_enums() -> dict[str, set[str]]:
    """Pull the contract enums out of the vendored continuity_findings_packet schema.

    The packet schema nests the per-finding properties under
    allOf[1].properties.candidate_findings.items.properties.<field>.enum.
    We walk to the candidate_findings item schema and read each enum.
    """
    assert VENDOR_SCHEMA.exists(), f"vendored schema missing: {VENDOR_SCHEMA}"
    schema = json.loads(VENDOR_SCHEMA.read_text())

    # Locate the object-shaped allOf branch that carries `properties`.
    branch = None
    for sub in schema.get("allOf", []):
        if isinstance(sub, dict) and "properties" in sub:
            branch = sub
            break
    assert branch is not None, "could not find properties branch in vendored schema allOf"

    finding_props = (
        branch["properties"]["candidate_findings"]["items"]["properties"]
    )

    enums: dict[str, set[str]] = {}
    for field in (
        "finding_type",
        "scope_type",
        "confidence",
        "candidate_state",
        "severity_hint",
    ):
        enum = finding_props[field]["enum"]
        assert enum, f"canonical enum for {field!r} is empty in vendored schema"
        enums[field] = set(enum)

    # span_role lives one level deeper, inside evidence_spans items.
    span_role = finding_props["evidence_spans"]["items"]["properties"]["span_role"]["enum"]
    assert span_role, "canonical span_role enum is empty in vendored schema"
    enums["span_role"] = set(span_role)

    return enums


CANON = _load_canonical_enums()


# ---------------------------------------------------------------------------
# Surface 1: the validator script's VALID_* enum sets. These are now IMPORTED
# from pact_contracts (not hand-mirrored), so this surface proves the consumed
# package values still equal the vendored canonical schema — loading the
# validator module exercises that import (it fails closed if pact_contracts is
# unavailable, rather than silently passing).
# ---------------------------------------------------------------------------


def _load_validator_module():
    spec = importlib.util.spec_from_file_location(
        "validate_continuity_candidate", VALIDATOR_PATH
    )
    assert spec and spec.loader, f"cannot load validator: {VALIDATOR_PATH}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Map canonical field -> validator constant name.
VALIDATOR_CONST_MAP = {
    "finding_type": "VALID_FINDING_TYPES",
    "scope_type": "VALID_SCOPE_TYPES",
    "confidence": "VALID_CONFIDENCE",
    "candidate_state": "VALID_CANDIDATE_STATES",
    "severity_hint": "VALID_SEVERITY_HINTS",
    "span_role": "VALID_SPAN_ROLES",
}


@pytest.mark.parametrize("field,const_name", sorted(VALIDATOR_CONST_MAP.items()))
def test_validator_constants_match_canonical(field, const_name):
    mod = _load_validator_module()
    assert hasattr(mod, const_name), f"validator missing constant {const_name}"
    local = getattr(mod, const_name)
    # Imported from pact_contracts as a frozenset; accept either set kind.
    assert isinstance(local, (set, frozenset)), f"{const_name} expected to be a set/frozenset"
    assert local, f"{const_name} is EMPTY -- fail-closed"
    assert set(local) == CANON[field], (
        f"DRIFT in validator {const_name} for {field}:\n"
        f"  canonical: {sorted(CANON[field])}\n"
        f"  local:     {sorted(local)}\n"
        f"  missing:   {sorted(CANON[field] - local)}\n"
        f"  extra:     {sorted(local - CANON[field])}"
    )


# ---------------------------------------------------------------------------
# Surface 2: the operator prompts (v1/v2/v3) enum blocks.
#
# Each prompt declares two full bulleted enum lists:
#   "## Approved finding_type values" -> "- value" bullets
#   "Approved span_role values:"      -> "- value" bullets
# and an inline confidence triple: '"low", "moderate", "high"'.
# Only these three are stated as complete enumerations in the prompt body, so
# the prompt gate covers exactly those (the others are partial/example-only).
# ---------------------------------------------------------------------------


def _parse_prompt_bullet_block(text: str, header_pat: str) -> set[str]:
    """Collect '- token' bullets that follow a header line matching header_pat,
    stopping at the next blank-line-separated non-bullet or a '---' rule."""
    lines = text.splitlines()
    start = None
    header_re = re.compile(header_pat)
    for i, line in enumerate(lines):
        if header_re.search(line):
            start = i + 1
            break
    if start is None:
        return set()
    values: set[str] = set()
    bullet_re = re.compile(r"^-\s+([a-z][a-z0-9_]*)\s*$")
    seen_bullet = False
    for line in lines[start:]:
        m = bullet_re.match(line.strip())
        if m:
            values.add(m.group(1))
            seen_bullet = True
            continue
        if line.strip() == "":
            # blank line: allowed before bullets start; ends block once started.
            if seen_bullet:
                break
            continue
        if line.strip() == "---":
            break
        # any other non-bullet content ends the block once bullets began
        if seen_bullet:
            break
    return values


def _parse_prompt_inline_confidence(text: str) -> set[str]:
    """Extract the confidence triple from the inline declaration line, e.g.
    'confidence: one of "low", "moderate", "high"'."""
    m = re.search(r"confidence:\s*one of\s*(.+)", text)
    if not m:
        return set()
    return set(re.findall(r'"([a-z]+)"', m.group(1)))


@pytest.mark.parametrize("version", sorted(PROMPTS))
def test_prompt_finding_type_block_matches_canonical(version):
    path = PROMPTS[version]
    assert path.exists(), f"prompt missing: {path}"
    text = path.read_text()
    found = _parse_prompt_bullet_block(text, r"Approved\s+finding_type\s+values")
    assert found, f"{version}: parsed EMPTY finding_type block -- fail-closed"
    assert found == CANON["finding_type"], (
        f"DRIFT in prompt {version} finding_type block:\n"
        f"  canonical: {sorted(CANON['finding_type'])}\n"
        f"  prompt:    {sorted(found)}"
    )


@pytest.mark.parametrize("version", sorted(PROMPTS))
def test_prompt_span_role_block_matches_canonical(version):
    path = PROMPTS[version]
    text = path.read_text()
    found = _parse_prompt_bullet_block(text, r"Approved\s+span_role\s+values")
    assert found, f"{version}: parsed EMPTY span_role block -- fail-closed"
    assert found == CANON["span_role"], (
        f"DRIFT in prompt {version} span_role block:\n"
        f"  canonical: {sorted(CANON['span_role'])}\n"
        f"  prompt:    {sorted(found)}"
    )


@pytest.mark.parametrize("version", sorted(PROMPTS))
def test_prompt_confidence_inline_matches_canonical(version):
    path = PROMPTS[version]
    text = path.read_text()
    found = _parse_prompt_inline_confidence(text)
    assert found, f"{version}: parsed EMPTY confidence triple -- fail-closed"
    assert found == CANON["confidence"], (
        f"DRIFT in prompt {version} confidence values:\n"
        f"  canonical: {sorted(CANON['confidence'])}\n"
        f"  prompt:    {sorted(found)}"
    )


# ---------------------------------------------------------------------------
# Surface 3: the schema doc (continuity-progression-candidate-schema.md).
#
# Each enum field is documented as:
#   ### `<field>`
#   **Type:** enum string
#   ...
#   - `value`
#   - `value`
# Collect ALL backtick-bullets between the field header and the next
# section boundary ('###' or '---'); dedup into a set. (candidate_state
# intentionally repeats `candidate_unreviewed`; set-dedup handles it.)
# ---------------------------------------------------------------------------


def _parse_schema_doc_enum(text: str, field: str) -> set[str]:
    """Collect '- `value`' bullets under the field's definition header.

    Field definitions appear as either '### `field`' (top-level fields) or
    '#### `field`' (fields nested under an object schema, e.g. span_role under
    the Evidence object). Collect backtick-bullets until the next markdown
    header (any '#'-prefixed line) or a '---' rule. Set-dedup absorbs the
    intentional repeat of `candidate_unreviewed`.
    """
    lines = text.splitlines()
    header_re = re.compile(r"^#{3,4}\s+`" + re.escape(field) + r"`\s*$")
    start = None
    for i, line in enumerate(lines):
        if header_re.match(line):
            start = i + 1
            break
    if start is None:
        return set()
    values: set[str] = set()
    bullet_re = re.compile(r"^-\s+`([a-z][a-z0-9_]*)`\s*$")
    for line in lines[start:]:
        s = line.strip()
        if s.startswith("#") or s == "---":
            break
        m = bullet_re.match(s)
        if m:
            values.add(m.group(1))
    return values


@pytest.mark.parametrize(
    "field",
    sorted(["finding_type", "scope_type", "confidence", "candidate_state",
            "severity_hint", "span_role"]),
)
def test_schema_doc_enum_matches_canonical(field):
    assert SCHEMA_DOC.exists(), f"schema doc missing: {SCHEMA_DOC}"
    text = SCHEMA_DOC.read_text()
    found = _parse_schema_doc_enum(text, field)
    assert found, f"schema doc {field}: parsed EMPTY enum -- fail-closed"
    assert found == CANON[field], (
        f"DRIFT in schema doc {field}:\n"
        f"  canonical: {sorted(CANON[field])}\n"
        f"  doc:       {sorted(found)}\n"
        f"  missing:   {sorted(CANON[field] - found)}\n"
        f"  extra:     {sorted(found - CANON[field])}"
    )


# ---------------------------------------------------------------------------
# Sanity: confirm the canonical sets themselves are the expected values, so a
# silently-corrupted vendored copy can't make the whole gate vacuous.
# ---------------------------------------------------------------------------


def test_canonical_sets_are_well_formed():
    expected = {
        "finding_type": {
            "continuity_tension", "progression_break", "transition_gap",
            "descriptive_mismatch", "repeated_movement", "escalation_mismatch",
            "state_carry_forward_issue", "causal_link_unclear",
        },
        "scope_type": {"scene_local", "adjacent_scene", "scene_window", "chapter_window"},
        "span_role": {
            "setup", "contrast", "carry_forward", "mismatch_signal",
            "transition_signal", "progression_signal",
        },
        "confidence": {"low", "moderate", "high"},
        "candidate_state": {
            "candidate_unreviewed", "candidate_review_in_progress",
            "candidate_retained", "candidate_rejected", "candidate_promoted",
        },
        "severity_hint": {"minor", "moderate", "major"},
    }
    for field, exp in expected.items():
        assert CANON[field] == exp, (
            f"vendored canonical {field} unexpected: {sorted(CANON[field])}"
        )
