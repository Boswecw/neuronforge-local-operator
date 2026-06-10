"""Canonical record stores: committed file fixtures and the DataForge Local interface."""

from .fixture_store import DuplicateRecordId, FixtureStore, LoadedRecord
from .dataforge_local import DataForgeLocalAdapter

__all__ = ["FixtureStore", "LoadedRecord", "DuplicateRecordId", "DataForgeLocalAdapter"]
