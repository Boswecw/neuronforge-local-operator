#!/usr/bin/env python3
"""Emit first-slice SMITH-governed SkillOpt foundation records."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nlo_skillopt.continuity_cases import main


if __name__ == "__main__":
    raise SystemExit(main())
