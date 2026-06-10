"""G-04: the hardware capture script emits a schema-valid NLOHardwareProfile.v1
with graceful unsupported-metric behavior (absent metrics are declared, not guessed)."""

import json
import subprocess

from nlo_experiment_memory.contracts.loader import registry


def test_capture_script_emits_valid_profile(repo_root):
    completed = subprocess.run(
        ["bash", str(repo_root / "scripts" / "graph" / "capture-hardware-profile.sh")],
        capture_output=True, text=True, timeout=60, check=True,
    )
    profile = json.loads(completed.stdout)
    assert profile["schema_version"] == "nlo-hardware-profile-v1"
    assert registry().validate(profile) == []
    declared = set(profile.get("unsupported_metrics", []))
    # every capturable metric is either present or declared unsupported — never both
    for metric in ("os", "kernel", "cpu_model", "cpu_cores", "mem_total_gb",
                   "mem_available_gb", "gpu"):
        assert (metric in profile) != (metric in declared), metric
