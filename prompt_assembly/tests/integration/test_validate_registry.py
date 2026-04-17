"""End-to-end test for the validate_registry tool.

Phase 0 only ships the registry-validation surface; this test exercises it
against the shipped contracts and config to prove the tool returns success.
"""

from __future__ import annotations

import io
from contextlib import redirect_stderr, redirect_stdout

from prompt_assembly.tools import validate_registry


def test_validate_registry_passes_on_shipped_phase0_state() -> None:
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = validate_registry.main([])
    assert rc == 0, err.getvalue()
    assert "Phase 0 contract lock" in out.getvalue()
