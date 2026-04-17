"""Shared Phase 0 test fixtures.

Adds the repo root to ``sys.path`` so the ``prompt_assembly`` package is
importable without requiring an editable install. Phase 0 deliberately
ships no setup.py / pyproject; tests must remain self-contained.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
