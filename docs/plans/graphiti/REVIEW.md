# Plan-Set Review — Graphiti Experiment-Memory Pilot

Review of the imported plan set (`README.md`, `01`–`14`) against the actual state of
`neuronforge-local-operator` before implementation. Reviewed 2026-06-10.

## Verdict

The plan set is internally coherent and consistent with repo doctrine (operator-only
promotion, reproducible records, lore-safe focus, bounded experiments). It is approved
for implementation with the resolutions recorded below. Nothing in the plan set
contradicts `NLOSYSTEM.md` authority boundaries.

## Confirmed Alignment

- The governing rule (Graphiti may explain and suggest, never approve/promote/mutate)
  matches the repo's promotion doctrine (`docs/current-baseline.md`, `docs/adr/ADR-001`).
- The plan's anchors are real repo history: `run-2026-03-13-005` (accepted baseline,
  `qwen2.5:14b` + `prompts/lore-safe-proofread-003.md`), rejected challengers
  (`run-2026-03-13-016` …), and the documented Ollama memory failure boundary
  (`docs/operational-workflow.md`: model requires more system memory (3.3 GiB) than is
  available (2.5 GiB)) which maps to taxonomy class `OUT_OF_MEMORY`.
- `analyze.style.scene.v1` (used in plan examples) is a real task contract
  (candidate_baseline). The lore-safe lane's contract id is `proofread.lore_safe.v1`
  (declared in `doc/system/01-task-contract-taxonomy.md` §3.3).
- The plan's failure taxonomy covers every failure mode recorded in
  `registry/runs.md` and `evals/run-*.md` reviews.

## Discrepancies Found and Resolutions

1. **DataForge Local does not exist in this repo.** DataForge is the NeuronForge
   ecosystem's cloud data service; no local instance or client is present. Today the
   canonical experiment records live in Git (`registry/*.md`, `evals/*.md`,
   `docs/current-baseline.md`).
   **Resolution:** for the first pilot, Git is the authority for all artifact types in
   the authority matrix; normalized canonical records are committed fixtures converted
   from the markdown registries. The DataForge Local adapter ships as an interface only
   (per G-07), unimplemented. The authority matrix is unchanged for the day DataForge
   Local arrives. (Resolves open decision: "whether DataForge Local adapter is
   available in the first pilot" → interface only, not available.)

2. **The `04-TEMPORAL-SEMANTICS.md` baseline example is illustrative, not history.**
   It shows "run-022 replaced run-005 on 2026-06-10". In real history
   `run-2026-03-13-022` (olmo2:13b) was a *rejected* challenger and `run-2026-03-13-005`
   has never been superseded.
   **Resolution:** the example is kept verbatim as a doctrine illustration; fixtures
   and golden query results encode only real history (run-005 baseline current,
   `superseded_at: null`).

3. **`01-PILOT-ARCHITECTURE.md` scope says "four operator evidence queries";
   `08-OPERATOR-QUERY-CONTRACTS.md` lists five commands.**
   **Resolution:** implement all five (current-baseline, baseline-history,
   recurring-failures, compare-runs, explain-candidate).

4. **No `nlo` CLI exists in the repo.**
   **Resolution (resolves open decision "final operator CLI naming"):** the query
   surface is `python3 -m nlo_experiment_memory.cli …` with a thin operator wrapper
   `scripts/graph/nlo-graph` exposing the exact subcommand names from plan 08.

5. **No `src/` layout exists** (repo packages are top-level: `service/`,
   `prompt_assembly/`).
   **Resolution:** follow plan 07 as written (`src/nlo_experiment_memory/`); tests and
   the wrapper script add `src/` to `PYTHONPATH` themselves, so no global config is
   required and decommission stays one bounded change set.

6. **Registry timestamps are date-only.** `registry/runs.md` records dates, not times.
   **Resolution:** converted fixture records use the real date (2026-03-13) with
   time-of-day placeholders chosen only to satisfy temporal ordering (run < review <
   decision), following the plan's own example times (19:00Z for the run-005 baseline
   decision). The fixture README declares this explicitly.

7. **The documented OOM failure is not tied to a run id** in `registry/runs.md`
   (failed runs are intentionally not logged as successful runs).
   **Resolution:** the OOM/hardware path uses an explicitly fixture-namespaced run id
   (`run-fixture-oom-001`) carrying the exact documented error string, with
   `converted_from` pointing at `docs/operational-workflow.md`. It cannot be confused
   with a registry run.

## Locked Decisions (resolving plan 14 "Open Decisions")

| Open decision | Resolution |
| --- | --- |
| Final backend choice | Neo4j Community, pinned `neo4j:5.26.0-community` in Docker, loopback only |
| Acceptable projection lag for advisory queries | 0 seconds (any unprojected canonical record fails advisory queries closed); tunable via `NLO_GRAPH_MAX_PROJECTION_LAG_SECONDS` |
| DataForge Local adapter in first pilot | Interface only; fixture store is the pilot record source |
| Optional semantic enrichment tested | No. Module exists as a disabled boundary that refuses to run |
| Final operator CLI naming | `scripts/graph/nlo-graph <subcommand>` → `python3 -m nlo_experiment_memory.cli` |

## Graphiti Installation Gate (honored, then lifted 2026-06-10)

Per the plan README, Graphiti was **not** installed before G-01–G-05 passed. The
deterministic projector, rebuild proof, and evidence queries were implemented and tested
against an in-memory graph store (a test double, not a second production backend — see
plan 14 anti-patterns).

G-01–G-05 were operator-accepted by merge, and G-06 verified the pinned backend live,
so the gate is lifted: `graphiti-core==0.29.2` and `neo4j==6.2.0` are pinned **optional**
dependencies (`requirements-graphiti.txt`) used only by the live adapter
(`src/nlo_experiment_memory/projection/live_backend.py`). The adapter is strictly
deterministic (our ids as uuids, `effective_at→valid_at`, `superseded_at→invalid_at`,
canonical payload carried losslessly per node/edge; no LLM extraction, no embeddings),
imports its dependencies lazily so every core module works without them, refuses
non-loopback URIs, and never appears on the NLO run path.

## Slice Status

| Slice | Status |
| --- | --- |
| G-01 Governance and authority | Complete (plan set imported; this review resolves authority questions; no Graphiti dependency installed) |
| G-02 Identity and temporal semantics | Complete (`src/nlo_experiment_memory/identity/`, tested without Graphiti) |
| G-03 Core schemas and validation | Complete (`schemas/experiment_memory/`, strict, valid/invalid examples tested) |
| G-04 Historical fixtures and hardware provenance | Complete (4 historical runs: 002, 003, 005, 016; 1 fixture-modeled OOM event excluded from default trend analytics; `scripts/graph/capture-hardware-profile.sh`) |
| G-05 Deterministic mapping specification | Complete (`MAPPING-SPEC.md`; no LLM extraction for core facts) |
| G-06 Local backend pilot | **Verified on operator hardware 2026-06-10** (Ubuntu 24.04, Docker 29.1.3, Compose plugin 2.40.3): `neo4j:5.26.0-community` pulled and started via `graph-up.sh`, health check reported healthy, bindings confirmed loopback-only (`127.0.0.1:7474`, `127.0.0.1:7687`), and the projection fingerprint matched the frozen golden value in `graph-doctor.sh`. Memory/CPU limits are applied by the compose file (`mem_limit: 1536m`, `cpus: 2.0`; confirm anytime with `docker inspect -f '{{.HostConfig.Memory}} {{.HostConfig.NanoCpus}}' nlo-graphiti-pilot-neo4j` → `1610612736 2000000000`). Lifecycle scripts detect `docker compose`/legacy `docker-compose` and source `.env.graphiti` (Ubuntu's `docker.io` alone lacks the plugin: `sudo apt install docker-compose-v2`). Note: the backend runs empty until a live Graphiti adapter proof writes the projection to it — currently gated behind G-10 |
| G-07 Deterministic projector and rebuild | Complete against in-memory store; two-rebuild provenance-equality proof in tests and `nlo-graph rebuild --prove` |
| G-08 Operator evidence queries | Complete (five queries, golden evidence tests, fail-closed gates) |
| G-09 Comparative evaluation | Complete (`G-09-COMPARATIVE-EVALUATION.md`; real Graphiti adapter remains unscored until the live proof below passes) |
| Live adapter proof (pre-G-10) | **PASSED in the implementation environment 2026-06-10** against a real Neo4j Community 5.26.0 (tarball, same pinned version as the compose file): 26 nodes / 34 edges written via the graphiti driver, read back via graphiti's models, file = backend = report fingerprint (`857c29e5…`), all five golden evidence queries MATCH from the backend, idempotent double-write confirmed by the opt-in integration test. First live contact surfaced and fixed two defects: (1) graphiti-core 0.29.2's `EntityNode.save`/`EntityEdge.save` unconditionally call Neo4j vector procedures and fail without embeddings — which plan 05 forbids — so writes use graphiti-schema-shaped Cypher through the graphiti driver (a real Graphiti-fit finding for G-10); (2) the adapter now owns one event loop for the driver's lifetime. **Operator confirmation 2026-06-10**: `nlo-graph verify-live` PASSED on the operator's Ubuntu 24.04 host against the Docker-composed pinned backend — 26 nodes / 34 edges, file = backend = report fingerprint (`857c29e5…`), provenance equal, all five golden evidence queries MATCH from the backend read-back. The live proof is closed; Graphiti may now be scored in the G-09 doc |
| G-10 Keep/revise/remove decision | Not started (operator decision after the live proof settles Graphiti's score) |
