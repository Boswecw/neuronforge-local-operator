"""DataForge Local adapter — interface only in this pilot.

DataForge Local does not exist in this repository today (see
docs/plans/graphiti/REVIEW.md, resolution 1). When it arrives it becomes the
designated authority for run receipts, evaluations, failure observations,
hardware profiles, and decision receipts per the authority matrix (plan 02).
Until then the FixtureStore is the canonical record source and this interface
defines the exact read surface a future adapter must provide.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class DataForgeLocalAdapter(ABC):
    """Read-only canonical record access. Projection never writes to sources."""

    @abstractmethod
    def records(self) -> dict[str, dict]:
        """Return all canonical records keyed by record id."""

    @abstractmethod
    def by_type(self, record_type: str) -> dict[str, dict]:
        """Return canonical records of one type keyed by record id."""

    @abstractmethod
    def source_high_watermark(self) -> str | None:
        """Return the max recorded_at across authoritative records."""
