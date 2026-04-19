# ADR-001 — Promotion truth remains upstream-owned by PACT

**Date:** 2026-04-17
**Status:** Accepted

## Context

The wave-1 promotion integration plan (`promotion_integration_plan_set_canvases_2026-04-17`) admits PACT as the upstream serialization authority for TOON wave-1: PACT owns the rendering rules, the strict success hash, the non-strict canonical digests, the promotion packet, and the manifest. neuronforge participates as a bounded local consumer.

## Decision

- The `promotion/` package in this repo carries the PACT-emitted wave-1 promotion envelope verbatim. It does **not** redefine envelope shape, recompute admission truth, or alter fallback semantics.
- The trusted local mirror (`registry/pact_wave1_envelope_mirror.json`) is refreshed only by copying the PACT-owned envelope artifact. We never hand-edit the mirror.
- The compatibility checker (`promotion/compatibility.py`) is fail-closed. Missing strict hash, missing canonical digest, mirror mismatch, manifest drift, unsupported packet class, or unsupported profile all map to `not_admitted` with explicit reason codes.
- The promotion run log (`registry/promotion_runs.jsonl`, written by the seam verifier into `evidence/promotion_seam/`) is a machine-readable record of admission classification per run; it does not replace `registry/runs.md`.
- Behavioural change is deferred. Wave-1 carriage admits no runtime decision conditioned on promotion state. Stage 4 of Canvas 05 is explicitly out of scope here.

## Consequences

- neuronforge cannot silently downgrade a missing strict hash to "good enough"; the seam verification script proves this.
- A new wave (e.g. wave-2) requires a new PACT-emitted envelope. neuronforge will consume — never invent — that envelope.
- ForgeCommand and the cloud lane consume `evidence/promotion_seam/seam_report.json` and `promotion_runs.jsonl` rather than re-deriving truth.

## Verification

Run `python3 scripts/verify_promotion_seam.py`. Expect `verify_promotion_seam: PASS` and a green `all_pass` flag in the seam report.
