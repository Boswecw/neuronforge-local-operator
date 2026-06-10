"""Canonical record contracts: schema loading, validation, integrity, ingestion filter."""

from .loader import (
    RECORD_TYPE_BY_SCHEMA_VERSION,
    SchemaRegistry,
    UnsupportedSchemaVersion,
    registry,
    validate_record,
)
from .integrity import IntegrityChecker, ingestion_filter_violations

__all__ = [
    "RECORD_TYPE_BY_SCHEMA_VERSION",
    "SchemaRegistry",
    "UnsupportedSchemaVersion",
    "registry",
    "validate_record",
    "IntegrityChecker",
    "ingestion_filter_violations",
]
