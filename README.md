# AOS Neurosymbolic AI

[![AOS Limited Demonstrator CI](https://github.com/szymonai/aos-neurosymbolic-ai/actions/workflows/aos-core-ci.yml/badge.svg)](https://github.com/szymonai/aos-neurosymbolic-ai/actions/workflows/aos-core-ci.yml)

Public demonstrator version: `0.1.0`

AOS is a domain-neutral runtime assurance layer for AI systems. It evaluates
bounded model-output signals against explicit policies and returns deterministic,
auditable `PASS` / `WARN` / `BLOCK` decisions.

AOS does not replace the model, expert, operator, or final decision-maker. It
sits between an AI output and downstream workflow use.

```text
AI output -> quality / uncertainty / risk signal -> explicit policy
  -> AOS gate -> PASS / WARN / BLOCK -> replayable audit evidence
```

This repository is a limited public demonstrator of that control pattern. It is
not a production SDK, regulated product, clinical system, or full commercial
implementation.

## Why Neurosymbolic?

The repository name reflects the intended boundary between neural model outputs
and symbolic control logic. In this public demonstrator:

- the neural side is represented by bounded output metadata such as uncertainty,
  confidence, quality, or risk signals;
- the symbolic side is represented by explicit policies, deterministic verdict
  logic, replayable evidence, and a small Lean proof surface.

This repository does not publish model internals, training pipelines, production
domain adapters, or a full neural-symbolic research stack.

## What AOS Does

- gates AI outputs before they affect a workflow;
- converts bounded uncertainty or quality signals into `PASS`, `WARN`, or
  `BLOCK`;
- records reproducible evidence for demonstrator decisions;
- separates model output, AOS verdict, human decision, and external claim;
- provides a reusable assurance pattern for multiple application profiles.

See [Plain-language overview](docs/PLAIN_LANGUAGE_OVERVIEW.md) and
[AI problems addressed](docs/AI_PROBLEMS_ADDRESSED.md).

## Quickstart

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest tests -q
python benchmarks/run_benchmarks.py
python -m json.tool benchmarks/results/metrics.json
lake build AOSPublicCore
```

Minimal example:

```bash
cd examples/hello-world
docker compose up
```

API-shaped evidence replay example:

```bash
python examples/api-gate/aos_api_gate.py evaluate \
  --input examples/api-gate/sample_input.json
python examples/api-gate/aos_api_gate.py replay \
  --evidence examples/api-gate/sample_evidence.json
```

## What This Repository Shows

| Area | Public content |
| --- | --- |
| Gate logic | Simplified interval gate returning `PASS` / `WARN` / `BLOCK` |
| API shape | Neutral `/v1/evaluate` and `/v1/replay` demonstrator |
| Evidence | SHA-256-linked public audit identifiers and JSON evidence |
| Benchmarks | Synthetic scenarios with reproducible metrics |
| Formal surface | Lean proof surface for abstract verdict logic |
| Boundaries | Machine-readable claim flags and publication checks |

## Evidence And Verification

| Claim type | Public source |
| --- | --- |
| Synthetic benchmark behavior | [Benchmark summary](benchmarks/results/summary.md), [metrics JSON](benchmarks/results/metrics.json) |
| Metric interpretation | [Value metrics](docs/VALUE_METRICS.md), [Demonstrator comparison](docs/DEMONSTRATOR_COMPARISON.md) |
| Public evidence boundaries | [Demonstrator manifest](evidence/demonstrator_manifest.json) |
| Formal verdict scope | [Scope of Proof](SCOPE_OF_PROOF.md), [Formal Claims Boundary](docs/FORMAL_CLAIMS_BOUNDARY.md), [Lean proof surface](lean/AOSPublicCore.lean) |
| API-shaped replay | [API gate example](examples/api-gate) |
| Radiology reference evidence | [Offline evaluation results](docs/OFFLINE_EVALUATION_RESULTS.md), [radiology evidence JSON](evidence/radiology_offline_evaluation.json), [radiology evidence review JSON](evidence/radiology_evidence_review.json) |

Radiology is included as one reference profile for understanding the assurance
pattern. Detailed radiology metrics are kept in focused evidence documents, not
in the README, to avoid presenting them as broad product or clinical claims.

## Application Profiles

The same public control pattern can be evaluated in neutral, non-certified
workflows such as:

- LLM output and agent action gating;
- RAG, document AI, and enterprise copilot review;
- cybersecurity automation review;
- industrial and physical-system quality review;
- robotics and edge-signal review;
- healthcare R&D audit support;
- financial workflow review.

These are potential adaptation profiles, not released products or deployment
claims. See [Application profiles](docs/APPLICATION_PROFILES.md) and
[Universal kernel positioning](docs/UNIVERSAL_KERNEL_POSITIONING.md).

## Public Boundary

This repository does not contain:

- production-system code or customer deployment material;
- model weights, checkpoints, medical datasets, patient files, DICOM/NIfTI
  files, masks, or local paths;
- production security design, production signing infrastructure, or commercial
  delivery material;
- clinical validation, regulatory approval, safety certification, or unrelated
  mathematical claims.

The Lean file covers abstract verdict logic only. It does not prove model
correctness, production audit security, Python-to-Lean refinement, Python
numeric runtime behavior, Int/Float correspondence, domain adapter behavior, or
clinical safety.

See [Public boundary](docs/PUBLIC_BOUNDARY.md), [SDK boundary](docs/SDK_BOUNDARY.md),
[Regulatory readiness](docs/REGULATORY_READINESS.md), and
[Repository best practices](docs/REPOSITORY_BEST_PRACTICES.md).

## Documentation Map

- [Public architecture](docs/architecture.md)
- [Scope of Proof](SCOPE_OF_PROOF.md)
- [Formal Claims Boundary](docs/FORMAL_CLAIMS_BOUNDARY.md)
- [Demonstrator comparison](docs/DEMONSTRATOR_COMPARISON.md)
- [Customer value](docs/CUSTOMER_VALUE.md)
- [Value metrics](docs/VALUE_METRICS.md)
- [Commercialization direction](docs/COMMERCIALIZATION.md)
- [Integrity anchors](docs/INTEGRITY_ANCHORS.md)
- [Dataset provenance](docs/DATASET_PROVENANCE.md)
- [Radiology reference system](docs/RADIOLOGY_REFERENCE_SYSTEM.md)
- [Radiology evidence review](docs/RADIOLOGY_EVIDENCE_REVIEW.md)
- [Development transparency](docs/DEVELOPMENT_TRANSPARENCY.md)
- [Clean-room test](docs/CLEAN_ROOM_TEST.md)
- [Performance and evaluation boundary](docs/CALIBRATION_AND_OPTIMIZATION.md)
- [Hello-world example](examples/hello-world)

## License

This repository is published under a proprietary demonstrator notice. Viewing
the repository does not grant rights to copy, modify, distribute, commercialize,
or create derivative works without written permission.

See [LICENSE](LICENSE).
