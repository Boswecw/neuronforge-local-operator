        # NeuronForge Local Operator - Compiled System Reference

        **Designation:** NLO
        **Document role:** Canonical compiled technical reference for the NeuronForge Local Operator control surface
        **Source:** `doc/system/`
        **Build command:** `bash doc/system/BUILD.sh`
        **Document version:** 2.0 (2026-06-22) - canonical compliance migration
        **Protocol:** BDS Documentation Protocol v2.0; BDS Repo Documentation System Canonical Compliance Standard

        > **Generated artifact warning:** `doc/NLOSYSTEM.md` is assembled output. Edit
        > the source modules under `doc/system/` and rebuild. Hand edits to the
        > compiled artifact are overwritten by the next build.

        Assembly contract:

        - Command: `bash doc/system/BUILD.sh`
        - Validation: `bash doc/system/validate_snapshots.sh` runs during assembly
        - Primary output: `doc/NLOSYSTEM.md`

        This `doc/system/` tree is the canonical source of truth for NeuronForge Local Operator. It uses
        explicit **truth classes**: canonical facts define repo role, authority
        boundaries, contract behavior, runtime behavior, and verification doctrine;
        snapshot facts are dated, audit-derived counts and current implementation
        inventory that may drift between audits.

        | Part | File | Contents |
        | --- | --- | --- |
        | §1 | `00_overview/00-overview.md` | Overview |
| §2 | `10_service-contract/01-task-contract-taxonomy.md` | NeuronForge Local Task Contract Taxonomy |
| §3 | `10_service-contract/04-anvil-bloom-reasoning-contracts.md` | ANVIL and Bloom Reasoning Contract Requirements |
| §4 | `10_service-contract/20-analyze-continuity-adjacent-scene-v1.md` | Task Contract: analyze.continuity.adjacent_scene.v1 |
| §5 | `10_service-contract/21-analyze-style-scene-v1.md` | Task Contract: analyze.style.scene.v1 |
| §6 | `20_runtime/02-routing-and-model-profile-plan.md` | NeuronForge Local Routing and Model Profile Plan |
| §7 | `20_runtime/05-scene-beat-extraction-lane-plan.md` | Scene-Aware Beat Candidate Extraction Lane Plan |
| §8 | `20_runtime/06-continuity-progression-reasoning-lane-plan.md` | Continuity / Progression Reasoning Lane Plan |
| §9 | `20_runtime/07-experiment-memory-graphiti-pilot.md` | Experiment-Memory (Graphiti) Pilot |
| §10 | `30_dependencies/30-dependencies.md` | Dependencies |
| §11 | `40_governance/03-candidate-artifact-doctrine.md` | Candidate Artifact Doctrine for AuthorForge |
| §12 | `50_operations/50-operations.md` | Operations |
| §13 | `99_appendices/90-appendices.md` | Appendices |

        ## Quick Assembly

        ```bash
        bash doc/system/BUILD.sh
        ```
