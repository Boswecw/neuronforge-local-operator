# NeuronForge System Documentation

**Document version:** 1.1 (2026-03-22) — analyze.style.scene.v1 promoted to candidate_baseline
**Protocol:** Forge Documentation Protocol v1

This `doc/system/` tree defines the NeuronForge Local control surface:
- Task contract taxonomy and contract doctrine
- Routing and model profile plan
- Candidate artifact doctrine
- Module-specific reasoning contract requirements
- Concrete lane plans

Assembly contract:
- Command: `bash doc/system/BUILD.sh`
- Output: `doc/nfSYSTEM.md`

| Part | File | Contents |
|------|------|----------|
| §1 | [01-task-contract-taxonomy.md](01-task-contract-taxonomy.md) | Task families, contract layering, strictness classes, degraded-mode doctrine |
| §2 | [02-routing-and-model-profile-plan.md](02-routing-and-model-profile-plan.md) | Route classes, hardware doctrine, contract-to-route mapping, fallback rules |
| §3 | [03-candidate-artifact-doctrine.md](03-candidate-artifact-doctrine.md) | Candidate artifact classes, evidence/confidence doctrine, review states, promotion rules |
| §4 | [04-anvil-bloom-reasoning-contracts.md](04-anvil-bloom-reasoning-contracts.md) | ANVIL/Bloom consumption rules, required contract posture, scope rules, failure doctrine |
| §5 | [05-scene-beat-extraction-lane-plan.md](05-scene-beat-extraction-lane-plan.md) | First concrete extraction lane: input scope, output doctrine, failure taxonomy, eval design |
| §6 | [06-continuity-progression-reasoning-lane-plan.md](06-continuity-progression-reasoning-lane-plan.md) | Cross-scene reasoning lane: scope doctrine, finding types, risk taxonomy, review rubric direction |

## Task contracts

| Contract                               | Status                              |
| -------------------------------------- | ----------------------------------- |
| `analyze.continuity.adjacent_scene.v1` | live                                |
| `analyze.style.scene.v1`               | **candidate_baseline** (2026-03-22) |

## Quick Assembly

```bash
bash doc/system/BUILD.sh   # Assembles all parts into doc/nfSYSTEM.md
```

*Last updated: 2026-03-22*
