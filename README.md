# AOS Meta-Symbolic Kernel

[![AOS Limited Demonstrator CI](https://github.com/szymonhetnar/aos-meta-symbolic-kernel/actions/workflows/aos-core-ci.yml/badge.svg)](https://github.com/szymonhetnar/aos-meta-symbolic-kernel/actions/workflows/aos-core-ci.yml)

Public demonstrator version: `0.1.0`

AOS is a meta-symbolic kernel for AI systems: a compact control core that
verifies, gates, routes, and records bounded AI-output signals under explicit
policies. Its public demonstrator includes a formal integrity proof surface for
selected properties of the abstract verdict model, returning auditable
`PASS` / `WARN` / `BLOCK` decisions independently of application domain.

AOS is not another AI application or a neural-symbolic model architecture. It
does not replace the model, expert, operator, or final decision-maker. It sits
between an AI output and downstream workflow use.

```text
AI output -> quality / uncertainty / risk signal -> explicit policy
  -> AOS gate -> PASS / WARN / BLOCK -> replayable audit evidence
```

This repository is a limited public demonstrator of that control pattern. It is
not a production SDK, regulated-use product, or production implementation.

Current public evidence status: bounded demonstrator evidence plus one
production-relevant offline replay. The strongest empirical artifact is the
operational control replay over public frozen time-series traces. It is not a
production deployment proof, external validation, or a general effectiveness
claim for all AOS applications.

## Why Meta-Symbolic Kernel?

`Meta-symbolic kernel` is the preferred public description because it captures
the relevant properties of AOS without implying that this repository publishes a
full neural-symbolic research stack:

- `meta`: AOS operates above model internals, supervising AI outputs before they
  affect downstream workflow state;
- `symbolic`: AOS uses explicit policies, deterministic verdict logic,
  reproducible evidence, and a small Lean proof surface;
- `kernel`: AOS is the compact control core that turns bounded signals and
  policy rules into deterministic workflow verdicts.

Verification is one function of the kernel, alongside gating, routing, audit
evidence generation, and policy-boundary enforcement.

The public Lean surface verifies selected integrity properties of the abstract
verdict model. This is sufficient for the narrow claim that the published
verdict contract has selected formal invariants. It is not sufficient for model
correctness, production runtime correctness, Python-to-Lean refinement,
effectiveness, or regulated-use safety.

This repository does not publish model internals, training pipelines, production
domain adapters, or a full neural-symbolic research stack.

## What AOS Does

- gates AI outputs before they affect a workflow;
- converts bounded uncertainty or quality signals into `PASS`, `WARN`, or
  `BLOCK`;
- records reproducible evidence for demonstrator decisions;
- separates model output, AOS verdict, human decision, and external claim;
- provides a reusable assurance pattern for multiple application profiles.

## Why It Matters

AI systems can produce many plausible outputs, but downstream workflows often
need a clearer decision boundary: proceed, review, or stop.

AOS is designed to support selective progression:

- policy-compliant outputs can move forward with audit evidence;
- uncertain outputs can be escalated for review;
- policy-violating outputs can be blocked before they trigger costly downstream
  work.

This can support cost discipline in research, operations, and industrial
workflows by making expensive review, compute, experimentation, or escalation
more selective. The public repository demonstrates the control pattern only; it
does not make domain-validation, regulatory, or production-readiness claims.

See [Plain-language overview](docs/PLAIN_LANGUAGE_OVERVIEW.md) and
[AI problems addressed](docs/AI_PROBLEMS_ADDRESSED.md).

## How Decisions Are Evaluated

AOS does not guess whether a model is correct. It evaluates whether a bounded
model-output signal may move forward under an explicit policy.

The public demonstrator reports control-layer metrics:

- `false_pass`: an unsafe synthetic case was allowed through;
- `false_block` / false alarm: a safe or reviewable case was blocked;
- `unsafe_block_rate`: expected `BLOCK` cases that were blocked;
- `warning_preservation_rate`: expected `WARN` cases that remained `WARN`;
- `audit_coverage_rate`: decisions carrying an audit digest;
- `deterministic_replay`: same public input and policy reproduce the same
  verdict.

The API-shaped examples include local SHA-256 audit digests for replay checks
in the demo. They are not a distributed trust model, production signature
scheme, key-management design, or security recommendation.

## Quickstart

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest tests -q
python tools/verify_public_integrity.py
python benchmarks/run_benchmarks.py --check
python benchmarks/run_llm_assurance_benchmark.py --check
python benchmarks/run_llm_hard_case_benchmark.py --check
python benchmarks/run_operational_control_replay.py --check
python benchmarks/run_controlled_study.py --help
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
| Evidence | JSON evidence and local demonstrator audit digests |
| Benchmarks | Synthetic scenarios with reproducible metrics |
| Formal surface | Lean proof surface for selected abstract verdict invariants |
| Runtime substrates | Python/Lean public substrate boundary and optional native/GPU backend roles |
| Boundaries | Machine-readable claim flags and publication checks |

## Evidence And Verification

| Claim type | Public source |
| --- | --- |
| Synthetic benchmark behavior | [Benchmark summary](benchmarks/results/summary.md), [metrics JSON](benchmarks/results/metrics.json) |
| LLM and agent assurance profile | [LLM assurance benchmark](benchmarks/results/llm_assurance_summary.md), [LLM assurance metrics](benchmarks/results/llm_assurance_metrics.json), [hard-case summary](benchmarks/results/llm_hard_case_summary.md), [controlled-study runner](benchmarks/run_controlled_study.py), [evaluation standard](docs/LLM_ASSURANCE_EVALUATION.md) |
| Operational control replay | [Operational replay summary](benchmarks/results/operational_control_replay_summary.md), [operational replay metrics](benchmarks/results/operational_control_replay_metrics.json), [replay profile](docs/OPERATIONAL_CONTROL_REPLAY.md) |
| Public assessment | [Usefulness, scalability, and evidence assessment](docs/PUBLIC_ASSESSMENT.md) |
| Technical diligence boundary | [Technical diligence](docs/TECHNICAL_DILIGENCE.md) |
| Metric interpretation | [Value metrics](docs/VALUE_METRICS.md), [Demonstrator comparison](docs/DEMONSTRATOR_COMPARISON.md) |
| Public evidence boundaries | [Demonstrator manifest](evidence/demonstrator_manifest.json), [Integrity manifest](evidence/integrity_manifest.json) |
| Formal verdict scope | [Scope of Proof](SCOPE_OF_PROOF.md), [Formal Claims Boundary](docs/FORMAL_CLAIMS_BOUNDARY.md), [Lean proof surface](lean/AOSPublicCore.lean) |
| API-shaped replay | [API gate example](examples/api-gate) |

Current evidence status is summarized in [Evidence status](docs/EVIDENCE_STATUS.md).

Formal proof status:

- `lake build AOSPublicCore` verifies the public Lean target;
- the public integrity checker rejects incomplete Lean proof placeholders;
- the result is an abstract verdict-integrity proof, not an effectiveness proof
  or full-system verification claim.

The controlled-study runner separates protocol evidence from effectiveness
evidence. Frozen outputs and replayable metrics can satisfy the protocol gate;
an effectiveness claim additionally requires independent signal extraction,
normalization audit, matched baselines, and reported failures/trade-offs.

At the current public stage, the smoke and hard-case benchmark results should
be read as implementation and measurement checks. They are not sufficient
public effectiveness evidence.

## Application Profiles

The same public control pattern can be evaluated in neutral, non-production
workflows such as:

- LLM output and agent action gating;
- RAG, document AI, and enterprise copilot review;
- cybersecurity automation review;
- industrial and physical-system quality review;
- robotics and edge-signal review;
- financial workflow review.

These are potential adaptation profiles, not released products or deployment
claims. See [Application profiles](docs/APPLICATION_PROFILES.md).

## Public Boundary

This repository does not contain:

- production-system code or deployment material;
- model weights, checkpoints, domain datasets, regulated records, or local paths;
- production security design, production signing infrastructure, or delivery
  material;
- domain validation, regulatory approval, safety approval, or unrelated
  mathematical claims.

The Lean file covers abstract verdict logic only. It does not prove model
correctness, production audit security, Python-to-Lean refinement, Python
numeric runtime behavior, Int/Float correspondence, domain adapter behavior, or
regulated-use safety.

See [Public boundary](docs/PUBLIC_BOUNDARY.md), [SDK boundary](docs/SDK_BOUNDARY.md),
and [Formal Claims Boundary](docs/FORMAL_CLAIMS_BOUNDARY.md).

## Documentation Map

- [Public architecture](docs/architecture.md)
- [Control spec](docs/CONTROL_SPEC.md)
- [Public surfaces](docs/PUBLIC_SURFACES.md)
- [Runtime substrates](docs/RUNTIME_SUBSTRATES.md)
- [Scope of Proof](SCOPE_OF_PROOF.md)
- [Formal Claims Boundary](docs/FORMAL_CLAIMS_BOUNDARY.md)
- [Demonstrator comparison](docs/DEMONSTRATOR_COMPARISON.md)
- [Value metrics](docs/VALUE_METRICS.md)
- [Evidence status](docs/EVIDENCE_STATUS.md)
- [Public assessment](docs/PUBLIC_ASSESSMENT.md)
- [Technical diligence](docs/TECHNICAL_DILIGENCE.md)
- [LLM assurance evaluation](docs/LLM_ASSURANCE_EVALUATION.md)
- [Operational control replay](docs/OPERATIONAL_CONTROL_REPLAY.md)
- [Controlled-study dataset profile](docs/CONTROLLED_STUDY_DATASETS.md)
- [Integrity anchors](docs/INTEGRITY_ANCHORS.md)
- [Dataset provenance](docs/DATASET_PROVENANCE.md)
- [Clean-room test](docs/CLEAN_ROOM_TEST.md)
- [Performance and evaluation boundary](docs/CALIBRATION_AND_OPTIMIZATION.md)
- [Hello-world example](examples/hello-world)

## License

This repository is published under a proprietary demonstrator notice. Viewing
the repository does not grant rights to copy, modify, distribute, commercialize,
or create derivative works without written permission.

See [LICENSE](LICENSE).
