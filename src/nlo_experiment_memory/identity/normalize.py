"""Property normalization for hashing, per plan 03.

Rules implemented:
- UTF-8 / Unicode NFC normalization for all strings;
- object keys sorted;
- set-like arrays sorted (declared by field name below);
- ordered arrays preserved where order is semantic;
- timestamps normalized to UTC RFC3339 with Z;
- absent optional fields are omission (semantic nulls such as
  superseded_at: null are preserved, never invented);
- backend-generated ids and projection runtime timestamps never enter
  semantic fingerprints (enforced by the projector, which simply does not
  include them).
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from datetime import datetime, timezone


class NormalizationError(ValueError):
    pass


# Arrays whose order is NOT semantic. Everything else keeps author order.
SET_LIKE_FIELDS = frozenset(
    {
        "failure_observation_ids",
        "evidence_record_ids",
        "unsupported_metrics",
        "supporting_record_ids",
        "contradicting_record_ids",
    }
)


def nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def normalize_timestamp(value: str) -> str:
    """Normalize an RFC3339 timestamp to UTC with Z and no insignificant zeros."""
    text = nfc(value).strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise NormalizationError(f"unparseable timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    parsed = parsed.astimezone(timezone.utc)
    base = parsed.strftime("%Y-%m-%dT%H:%M:%S")
    if parsed.microsecond:
        fraction = f".{parsed.microsecond:06d}".rstrip("0")
        return f"{base}{fraction}Z"
    return f"{base}Z"


def canonicalize(value, field_name: str | None = None):
    """Recursively normalize a JSON-compatible value for canonical serialization."""
    if isinstance(value, dict):
        return {key: canonicalize(value[key], key) for key in sorted(value)}
    if isinstance(value, list):
        items = [canonicalize(item, field_name) for item in value]
        if field_name in SET_LIKE_FIELDS:
            return sorted(items, key=lambda item: json.dumps(item, sort_keys=True))
        return items
    if isinstance(value, str):
        if field_name is not None and field_name.endswith("_at"):
            return normalize_timestamp(value)
        return nfc(value)
    return value


def canonical_json(value) -> str:
    """Deterministic compact JSON for hashing and equality comparison."""
    return json.dumps(
        canonicalize(value), sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
