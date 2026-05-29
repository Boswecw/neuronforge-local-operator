# NeuronForge — Local Operator

> Working training repository for **NeuronForge**, the public-facing applications support platform.

`neuronforge-local-operator` is the **local development and training environment** for NeuronForge. This is where local LLMs are trained, evaluated, and refined against applications-support tasks before the best-performing models are **promoted** to the public-facing NeuronForge applications-support deployment.

---

## What this repo is

- **A training repo.** It holds the data, configs, scripts, and tooling used to train and fine-tune **local LLMs**.
- **An operator's workspace.** It runs locally (on your own hardware or a private box) so you can iterate quickly and privately before anything ships.
- **A promotion pipeline.** Models that meet the quality bar here are pushed up to the **public-facing NeuronForge applications-support version**.

> [!NOTE]
> This repository is a *working* repo. Structure and tooling will evolve as the training workflow matures. Treat the layout below as the target shape, not a frozen spec.

---

## The workflow: local → public

```
┌──────────────────────────┐      train / fine-tune      ┌──────────────────────────┐
│  neuronforge-local-       │  ─────────────────────────▶ │   Local LLM (candidate)   │
│  operator  (this repo)    │                             │                           │
└──────────────────────────┘                             └─────────────┬────────────┘
            ▲                                                           │
            │  iterate on data, configs, prompts                       │ evaluate
            │                                                           ▼
            │                                              ┌──────────────────────────┐
            │                                  promote ◀── │   Passes quality gate?    │
            │                                              └─────────────┬────────────┘
            │                                                            │ yes
            ▼                                                            ▼
   (refine & re-train)                                  ┌──────────────────────────────┐
                                                        │  NeuronForge — public-facing  │
                                                        │  applications support         │
                                                        └──────────────────────────────┘
```

1. **Train locally.** Run training / fine-tuning jobs against your datasets and configs.
2. **Evaluate.** Score the candidate model on applications-support tasks.
3. **Gate.** Only models that clear the quality bar are eligible.
4. **Promote.** Publish the approved model to the public-facing NeuronForge applications-support version.
5. **Iterate.** Feed learnings back into data and configs, then repeat.

---

## Repository layout

```
neuronforge-local-operator/
├── data/            # Training & evaluation datasets (raw, processed, splits)
├── configs/         # Training, fine-tuning, and eval configurations
├── models/          # Local model checkpoints & candidate artifacts (git-ignored)
├── scripts/         # Train / evaluate / promote scripts
├── eval/            # Evaluation harness, benchmarks, and quality gates
├── notebooks/       # Exploration and analysis
└── README.md
```

> Directories are created as the workflow is built out. Large artifacts (checkpoints, datasets) should be tracked outside git (e.g. Git LFS or an artifact store), not committed directly.

---

## Getting started

```bash
# 1. Clone
git clone https://github.com/Boswecw/neuronforge-local-operator.git
cd neuronforge-local-operator

# 2. Set up your environment
#    (Python venv shown — adjust to the toolchain this repo standardizes on)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # once dependencies are defined

# 3. Configure
#    Copy and edit the example config / env for your local setup
cp .env.example .env              # if/when provided
```

### Typical operator loop

```bash
# Train or fine-tune a local model
scripts/train.sh --config configs/train.yaml

# Evaluate the candidate against the quality gate
scripts/evaluate.sh --model models/candidate

# Promote a passing model to public-facing NeuronForge
scripts/promote.sh --model models/candidate
```

*(Script names above are placeholders for the intended commands — wire them to the real entry points as they land.)*

---

## Promotion criteria

A candidate model is promoted to the public-facing applications-support version only when it:

- [ ] Passes the evaluation harness in `eval/` at or above the target thresholds
- [ ] Shows no regression against the current production model
- [ ] Has reproducible training config committed under `configs/`
- [ ] Has been reviewed and approved by an operator

---

## Relationship to NeuronForge

| | **neuronforge-local-operator** (this repo) | **NeuronForge** (public-facing) |
|---|---|---|
| Purpose | Train & refine local LLMs | Serve applications support to users |
| Audience | Operators / developers | End users |
| Models | Candidates & checkpoints | Promoted, production-approved models |
| Direction | Source of truth for training | Receives promoted models |

---

## Contributing

This is an active working repo. When contributing:

- Keep training configs reproducible and committed.
- Don't commit large model/data artifacts — use the designated artifact store.
- Run the evaluation harness before proposing a promotion.

---

## License

_TBD — add a license file before this repository is shared publicly._
