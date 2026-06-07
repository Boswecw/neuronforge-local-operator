#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VALID_MODEL_OUTPUT = {
    "schema_version": "1.0",
    "lane_id": "continuity-progression-reasoning",
    "analysis_scope_type": "adjacent_scene",
    "analysis_scope_bounds": {"scene_ids": ["cp001-sc-a", "cp001-sc-b"]},
    "input_unit_ids": ["cp001-sc-a", "cp001-sc-b"],
    "candidate_findings": [
        {
            "finding_id": "cpf-001",
            "finding_label": "Careful Grip Not Acknowledged",
            "finding_type": "state_carry_forward_issue",
            "claim": "Scene A suggests the injured hand is limiting Rawn's grip, while Scene B shows that hand used normally without any bridge or acknowledgement.",
            "scope_type": "adjacent_scene",
            "scope_bounds": {"scene_ids": ["cp001-sc-a", "cp001-sc-b"]},
            "evidence_spans": [
                {
                    "scene_id": "cp001-sc-a",
                    "span_text": "his grip on the lantern had become careful rather than easy.",
                    "span_role": "carry_forward"
                },
                {
                    "scene_id": "cp001-sc-b",
                    "span_text": "He drew the gate bolt with his left hand and held it open for Amicae without slowing.",
                    "span_role": "mismatch_signal"
                }
            ],
            "confidence": "moderate",
            "uncertainty_note": "A skipped beat between scenes could explain the change, but the packet itself does not provide that bridge.",
            "review_note": "Review whether an intervening recovery beat should be added or whether the action in Scene B should show continued caution.",
            "candidate_state": "candidate_unreviewed"
        }
    ],
    "overall_run_note": "Potential continuity issue identified around the injured hand carry-forward.",
    "run_posture": "candidate_only"
}

INVALID_MODEL_OUTPUT = "this is not valid json\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def run(cmd, cwd: Path, env: dict, expect_ok: bool):
    completed = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, text=True)
    if expect_ok and completed.returncode != 0:
      raise AssertionError(f"command failed: {' '.join(cmd)}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}")
    if not expect_ok and completed.returncode == 0:
      raise AssertionError(f"command unexpectedly passed: {' '.join(cmd)}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}")
    return completed


def load_single_envelope(output_dir: Path) -> dict:
    envelope_files = sorted(output_dir.glob("*.envelope.json"))
    if len(envelope_files) != 1:
        raise AssertionError(f"expected exactly one envelope in {output_dir}, found {len(envelope_files)}")
    return json.loads(envelope_files[0].read_text(encoding="utf-8"))


def assert_absent(data: dict, key: str) -> None:
    if key in data:
        raise AssertionError(f"expected key {key} to be absent, but found {data[key]!r}")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    with tempfile.TemporaryDirectory(prefix="nf-context-connectivity-") as tmpdir:
        sandbox = Path(tmpdir) / "repo"
        sandbox.mkdir(parents=True, exist_ok=True)

        # Minimal repo layout needed by the executor.
        for rel in [
            "scripts/run-continuity-adjacent-scene.sh",
            "scripts/read-context-intake.py",
            "scripts/validate-continuity-candidate.py",
            "scripts/next-run-id.sh",
            "scripts/log-run.sh",
            "scripts/verify_context_connectivity_slice.py",
            "inputs/case-packets/cp-001.json",
            "inputs/case-packets/cp-001-connected.json",
            "inputs/case-packets/cp-001-connected-with-refs.json",
            "inputs/case-packets/cp-001-partial-lineage.json",
        ]:
            copy_file(repo_root / rel, sandbox / rel)

        write_text(sandbox / "prompts/continuity-adjacent-scene-v3.md", "Return strict JSON only.\n")
        write_text(sandbox / "registry/runs.md", "# Runs\n")

        for rel in [
            "scripts/run-continuity-adjacent-scene.sh",
            "scripts/read-context-intake.py",
            "scripts/validate-continuity-candidate.py",
            "scripts/next-run-id.sh",
            "scripts/log-run.sh",
        ]:
            os.chmod(sandbox / rel, 0o755)

        fake_bin = sandbox / "fake-bin"
        fake_bin.mkdir(parents=True, exist_ok=True)
        fake_ollama = fake_bin / "ollama"
        fake_ollama.write_text(
            """#!/usr/bin/env bash
set -euo pipefail
if [ -n "${NF_OLLAMA_CALLS_FILE:-}" ]; then echo called >> "$NF_OLLAMA_CALLS_FILE"; fi
MODE="${NF_OLLAMA_MODE:-valid}"
case "$MODE" in
  valid) cat "${NF_OLLAMA_VALID_OUTPUT_FILE}" ;;
  invalid_json) cat "${NF_OLLAMA_INVALID_OUTPUT_FILE}" ;;
  fail_exec) echo 'synthetic ollama failure' >&2; exit 1 ;;
  *) echo "unknown mode: $MODE" >&2; exit 2 ;;
esac
""",
            encoding="utf-8",
        )
        os.chmod(fake_ollama, 0o755)

        valid_output_path = sandbox / "synthetic-valid-output.json"
        invalid_output_path = sandbox / "synthetic-invalid-output.txt"
        valid_output_path.write_text(json.dumps(VALID_MODEL_OUTPUT, indent=2), encoding="utf-8")
        invalid_output_path.write_text(INVALID_MODEL_OUTPUT, encoding="utf-8")

        base_env = os.environ.copy()
        base_env["PATH"] = f"{fake_bin}:{base_env.get('PATH', '')}"
        base_env["NF_OLLAMA_VALID_OUTPUT_FILE"] = str(valid_output_path)
        base_env["NF_OLLAMA_INVALID_OUTPUT_FILE"] = str(invalid_output_path)

        cases = []

        # Case 1: legacy packet passes and has no lineage fields.
        output_dir = sandbox / "outputs-case-legacy"
        env = base_env.copy()
        env["NF_OLLAMA_MODE"] = "valid"
        env["NF_OLLAMA_CALLS_FILE"] = str(sandbox / "calls-legacy.log")
        run(
            ["bash", "scripts/run-continuity-adjacent-scene.sh", "phi4:14b", "inputs/case-packets/cp-001.json", str(output_dir)],
            cwd=sandbox,
            env=env,
            expect_ok=True,
        )
        envelope = load_single_envelope(output_dir)
        assert envelope["envelope_status"] == "valid_candidate"
        assert_absent(envelope, "task_intent_id")
        assert_absent(envelope, "context_bundle_id")
        assert_absent(envelope, "context_bundle_hash")
        cases.append("legacy_packet_success")

        # Case 2: connected packet success preserves lineage.
        output_dir = sandbox / "outputs-case-connected"
        env = base_env.copy()
        env["NF_OLLAMA_MODE"] = "valid"
        env["NF_OLLAMA_CALLS_FILE"] = str(sandbox / "calls-connected.log")
        run(
            ["bash", "scripts/run-continuity-adjacent-scene.sh", "phi4:14b", "inputs/case-packets/cp-001-connected.json", str(output_dir)],
            cwd=sandbox,
            env=env,
            expect_ok=True,
        )
        envelope = load_single_envelope(output_dir)
        assert envelope["task_intent_id"] == "ati-proofread-lore-safe-001"
        assert envelope["context_bundle_id"] == "cbm-2026-04-16-001"
        assert envelope["context_bundle_hash"] == "sha256:1111111111111111111111111111111111111111111111111111111111111111"
        cases.append("connected_packet_success")

        # Case 3: connected packet with refs preserves optional provenance refs.
        output_dir = sandbox / "outputs-case-connected-refs"
        env = base_env.copy()
        env["NF_OLLAMA_MODE"] = "valid"
        env["NF_OLLAMA_CALLS_FILE"] = str(sandbox / "calls-connected-refs.log")
        run(
            ["bash", "scripts/run-continuity-adjacent-scene.sh", "phi4:14b", "inputs/case-packets/cp-001-connected-with-refs.json", str(output_dir)],
            cwd=sandbox,
            env=env,
            expect_ok=True,
        )
        envelope = load_single_envelope(output_dir)
        assert envelope["task_intent_id"] == "ati-proofread-lore-safe-002"
        assert envelope["run_metadata"]["context_manifest_ref"] == "target/proof_artifacts/context_bundle_manifest.json"
        assert envelope["run_metadata"]["context_payload_ref"] == "target/proof_artifacts/context_payload.json"
        cases.append("connected_packet_refs_success")

        # Case 4: partial lineage fails before model execution.
        output_dir = sandbox / "outputs-case-partial"
        calls_file = sandbox / "calls-partial.log"
        if calls_file.exists():
            calls_file.unlink()
        env = base_env.copy()
        env["NF_OLLAMA_MODE"] = "valid"
        env["NF_OLLAMA_CALLS_FILE"] = str(calls_file)
        run(
            ["bash", "scripts/run-continuity-adjacent-scene.sh", "phi4:14b", "inputs/case-packets/cp-001-partial-lineage.json", str(output_dir)],
            cwd=sandbox,
            env=env,
            expect_ok=False,
        )
        envelope = load_single_envelope(output_dir)
        assert envelope["envelope_status"] == "fail_closed"
        assert "partially present" in envelope["failure_reason"]
        assert envelope["task_intent_id"] == "ati-proofread-lore-safe-003"
        assert envelope["context_bundle_id"] == "cbm-2026-04-16-003"
        assert_absent(envelope, "context_bundle_hash")
        if calls_file.exists() and calls_file.read_text(encoding="utf-8").strip():
            raise AssertionError("ollama should not have been called for partial-lineage intake failure")
        cases.append("partial_lineage_fail_closed")

        # Case 5: connected packet fail-closed still preserves lineage.
        output_dir = sandbox / "outputs-case-connected-invalid"
        env = base_env.copy()
        env["NF_OLLAMA_MODE"] = "invalid_json"
        env["NF_OLLAMA_CALLS_FILE"] = str(sandbox / "calls-connected-invalid.log")
        run(
            ["bash", "scripts/run-continuity-adjacent-scene.sh", "phi4:14b", "inputs/case-packets/cp-001-connected.json", str(output_dir)],
            cwd=sandbox,
            env=env,
            expect_ok=False,
        )
        envelope = load_single_envelope(output_dir)
        assert envelope["envelope_status"] == "fail_closed"
        assert envelope["task_intent_id"] == "ati-proofread-lore-safe-001"
        assert envelope["context_bundle_id"] == "cbm-2026-04-16-001"
        assert envelope["context_bundle_hash"] == "sha256:1111111111111111111111111111111111111111111111111111111111111111"
        cases.append("connected_packet_fail_closed")

        print(json.dumps({"total_cases": len(cases), "cases": cases}, indent=2))
        return 0


if __name__ == "__main__":
    sys.exit(main())
