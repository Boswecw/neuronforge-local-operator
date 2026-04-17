# NeuronForge Local — Prompt Assembly Subsystem

**Status:** Phase 0 — contract lock only.
**Scope target:** NeuronForge Local Prompt Assembly V1.1.
**This is an internal business system, not an MVP.**

This subsystem governs how NeuronForge Local turns a caller-provided
profile, lane request, constraint surfaces, and inputs into a deterministic,
hashed, signature-ready bundle that can be handed to a model executor.

Phase 0 ships only the **contract foundation**: locked JSON schemas, mirrored
Pydantic v2 runtime models, controlled enums, the stable error taxonomy, and
the CLI/config posture. None of the assembly behavior is implemented yet.

---

## What is locked in Phase 0

| Surface | What is locked |
|---|---|
| `contracts/long_context.schema.json` | Required field set, lane allow list (LC-1, LC-2, LC-4), reason-code vocabulary |
| `contracts/constraint_surface.schema.json` | Field set, allowed `constraint_type` values, trust/authority coherence rule |
| `contracts/prompt_assembly_input.schema.json` | Caller request envelope shape |
| `contracts/prompt_assembly_manifest.schema.json` | Runtime-truth manifest field set |
| `contracts/compiled_bundle.schema.json` | Format contract: canonical JSON posture, semver, signature metadata block, compatibility block |
| `contracts/redaction_policy.schema.json` | Manifest-visible / debug-visible / masked / reference-only field categories and trust-level overrides |
| `contracts/common_enums.schema.json` | Single source of truth for lane ids, trust levels, constraint types, hash algs, serialization formats, error codes, tokenizer ids, contract version |
| `runtime/models.py` | Pydantic v2 mirror of every contract |
| `runtime/errors.py` | Stable error code enum + per-error exception classes + `ErrorEnvelope` |
| `config/defaults.yaml` | Default profile registry, tokenizer pins, baseline algorithms, CLI surface posture |
| `tools/validate_registry.py` | Backs `nf-local prompt-assembly registry validate` |

### Locked baselines

- **Hash algorithm:** BLAKE3
- **Bundle signing baseline:** Ed25519 (metadata only — signing is **not active** in Phase 0)
- **Structured-content hashing:** canonical JSON
- **Tokenizer pinning:** every active profile must declare both `tokenizer_id` and `tokenizer_version`

### Supported lanes (V1.1, local)

| Lane | Status |
|---|---|
| LC-1 | supported (local) |
| LC-2 | supported (local) |
| LC-3 | reserved, **not supported locally** in V1.1 |
| LC-4 | supported (local) |
| LC-5 | reserved, **not supported locally** in V1.1 |

Any caller request for LC-3 or LC-5 must surface as
`ERR_LANE_UNSUPPORTED_LOCAL`.

---

## What Phase 0 deliberately does **not** ship

Phase 0 is contract surface only. The following are **deferred by design**
and have no honest implementation in this directory:

- Resolver / input fetcher / staleness detection
- Policy admit/reject engine
- Compaction engine (summary, sliding window, partitioned execution)
- Tokenizer integration (no model is loaded; counts are not produced)
- Bundle assembly, canonical-JSON serializer, content hashing
- Ed25519 key management, signing, signature verification
- Bundle/version compatibility enforcement
- CLI runtime entry point (`nf-local prompt-assembly run`) — only the
  *contract surface* of the CLI is locked in `config/defaults.yaml`
- Audit log persistence and debug-render output
- Token forecasting and budget arithmetic

If you find a function that pretends to do any of the above, that is a Phase
0 violation — fail closed and log it.

---

## CLI / config posture (locked, not implemented)

Default config path: `prompt_assembly/config/defaults.yaml`
Default config format: YAML 1.2
Default artifact root: `./.nf_local/prompt_assembly/`

Zero-config conceptual command:

```bash
nf-local prompt-assembly run \
  --profile nf_local_editing_lore_safe_v1 \
  --input <path>
```

Phase 0 surface commands (locked names; behavior deferred):

| Command | Purpose |
|---|---|
| `nf-local prompt-assembly registry validate` | Validate contracts and config (the only command actually wired in Phase 0, via `tools/validate_registry.py`) |
| `nf-local prompt-assembly bundle build` | Build a compiled bundle from an input — deferred |
| `nf-local prompt-assembly bundle verify` | Verify bundle signature and compatibility — deferred |
| `nf-local prompt-assembly health` | Local health check — deferred |
| `nf-local prompt-assembly debug-render` | Generate a redaction-respecting debug render — deferred |

---

## Running Phase 0 verification

```bash
# JSON Schema + model + error + alignment + integration tests
python3 -m pytest prompt_assembly/tests -q

# Standalone registry validation
python3 -m prompt_assembly.tools.validate_registry
```

Both commands must exit zero before claiming Phase 0 is intact.

---

## Later phases depend on this lock

| Later phase | Depends on (Phase 0 lock) |
|---|---|
| Resolver / staleness | `LongContextModel`, `ResolverEnvelopeModel`, `RequiredStaleInputError` |
| Policy engine | `PolicyDecisionModel`, error codes for admit/reject failure |
| Compaction | `CompactionEventModel`, `LongContextModel.summary_allowed` / `sliding_window_allowed` / `governance_no_amnesia` |
| Tokenizer integration | `TokenizerId`, `tokenizer_version` field on manifest, profile pins in `defaults.yaml` |
| Bundle signing | `CompiledBundleModel.signature` block, `SignatureAlgorithm.ED25519` baseline |
| Redaction enforcement | `RedactionPolicyModel`, manifest field categories |
| Registry validation surface | `tools/validate_registry.py` (already shipped) |

If a later phase needs to widen any of these contracts, it must do so via a
new contract version (e.g. `1.2.0-...`), not by editing the Phase 0 lock.

---

## Truth statements

- **This subsystem does not assemble prompts in Phase 0.** It defines the
  contracts an assembler will be required to honor.
- **No model is contacted, no input is resolved, no token is counted.**
  Tokenizer ids exist only as locked vocabulary.
- **Bundles are not signed in Phase 0.** The signature block is structurally
  required; the `signed` flag is always `false` until signing is wired up.
- **Validation here is contract validation, not behavior validation.** The
  registry tool proves the contracts and the config are coherent, nothing
  more.
