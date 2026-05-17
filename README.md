# AOS Neurosymbolic AI

AOS is a domain-neutral runtime assurance layer for AI systems. It turns
uncertain model outputs into deterministic, auditable `PASS` / `WARN` /
`BLOCK` decisions.

AOS does not replace AI models. It controls the effects of their outputs before
they enter a workflow.

```text
AI model output -> explicit policy -> AOS gate
  -> PASS / WARN / BLOCK -> explanation -> audit evidence
```

This repository is a **limited public demonstrator** for the AOS control-layer
pattern. It is not a production SDK, regulated product, or full production
system.

For SDK positioning, see [SDK boundary](docs/SDK_BOUNDARY.md).

## In Plain Terms

AOS checks AI outputs before they affect a workflow. It does not decide what is
true and it does not replace human review. It decides whether an output should
`PASS`, require review with `WARN`, or be held with `BLOCK`, then records audit
evidence for that decision.

See [Plain-language overview](docs/PLAIN_LANGUAGE_OVERVIEW.md).

## What AOS Does

- evaluates model-output metadata against explicit control rules
- converts uncertain outputs into deterministic workflow decisions
- creates audit evidence for each public demonstrator decision
- separates model output, control decision, human decision, and external claim
- acts as a decision firewall between AI output and downstream effects

## AI Problems Addressed

| Current AI problem | AOS public response |
| --- | --- |
| Probabilistic outputs enter deterministic workflows | `PASS` / `WARN` / `BLOCK` control decisions |
| Uncertainty is lost after inference | Explicit uncertainty or quality-signal evaluation |
| Review triggers are unclear | Deterministic escalation signals |
| Audit trails are hard to reconstruct | SHA-256-linked public audit evidence |
| Governance claims get mixed together | Separate model output, AOS verdict, human decision, and external claim |

See [AI problems addressed](docs/AI_PROBLEMS_ADDRESSED.md).

## Anatomy Of A Verdict

| Field | Public demonstrator meaning |
| --- | --- |
| `input` | A bounded model-output or workflow signal |
| `policy` | A public rule used by the demonstrator |
| `verdict` | `PASS`, `WARN`, or `BLOCK` |
| `reason` | Human-readable explanation for the public example |
| `audit_id` | SHA-256-linked evidence identifier; signed evidence packets may add Ed25519 provenance metadata |

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

## What This Repository Shows

- a simplified `PASS` / `WARN` / `BLOCK` interval gate
- synthetic benchmark scenarios with reproducible public metrics
- SHA-256-linked demo audit evidence
- a small Lean proof surface for abstract verdict logic
- clean-room repeatability checks
- public documentation for scope, value metrics, and publication boundaries

## What This Repository Does Not Contain

- production-system code
- customer data, deployment material, or controlled evidence packages
- medical datasets, patient files, model weights, checkpoints, or local paths
- production security, deployment, or commercial delivery material
- clinical validation, regulatory approval, or unrelated mathematical claims

## Scope Of Proof

The public proof surface is intentionally narrow. It supports deterministic
verdict logic and bounded audit evidence for the demonstrator only.

See [Scope of Proof](SCOPE_OF_PROOF.md).

## Commercial Use Cases

The same public control pattern can be evaluated in neutral, non-certified
workflows such as:

- LLM output control
- agent action gating
- document AI review
- fintech risk review
- cybersecurity automation gates
- industrial quality review
- healthcare R&D audit support

These are use-case directions, not production deployment claims.

## Universal Control Kernel

The public positioning is:

```text
one domain-neutral control kernel -> many specialist profiles
```

AOS is domain-neutral by design and can be adapted to different AI workflows,
including enterprise automation, governance, cybersecurity, industrial systems,
research pipelines, and regulated domains. A specialist profile can adapt the
same control pattern to a domain:

```text
model output -> uncertainty or quality signal -> deterministic gate
  -> audit evidence -> human review, escalation, or workflow hold
```

Radiology is treated here as **Instance 01**: a reference specialist profile for
AI-assisted brain tumor triage. Other profiles could target LLM/RAG workflows,
industrial monitoring, enterprise approvals, cyber-defense, edge systems, or
other regulated decision workflows. This public repository is limited to the
shared public demonstrator pattern.

## Problem

AI is moving from content generation into decisions, actions, tool calls, and
enterprise workflows. Models are probabilistic. Organizations still need a
runtime guardrail before a model output is used in a real process.

AOS addresses this category as a runtime assurance layer: evaluate an output or
metadata, produce a conservative decision, and create an audit trail.

## Explainable/Verifiable AI Control Layer

The public demonstrator frames AOS as an explainable and verifiable AI control
layer. It separates four different objects that should not be collapsed into
one claim:

- model output
- AOS decision
- human decision
- clinical or operational claim

The public core demonstrates a deterministic `PASS` / `WARN` / `BLOCK` gate,
demo audit evidence, and a small Lean proof surface for abstract verdict logic.
It does not prove model correctness, production audit security, or clinical
validity.

## Radiology Reference Scenario

The reference medical scenario is AI-assisted brain tumor radiology triage:

```text
model output -> uncertainty -> AOS PASS/WARN/BLOCK
  -> audit evidence -> human review or escalation
```

Radiology is referenced only as a domain-adapter example. It is not a product in
this public repository and is not a medical-device or clinical-validation claim.

The specialist radiology system can be understood as an example of how a
domain-specific AOS profile could be built on top of the general control-layer
pattern. In this public repository, it is used only as utility evidence for the
architecture: one core control pattern can support multiple specialist systems.
It is not published here as the full specialist system.

## Offline Evaluation Evidence

The public repository now includes a bounded evidence review for selected
internal radiology summaries. It records which values were locally confirmed,
which values belong to a small validation fold, which values belong to an
internal cohort report, and which claims remain outside the public scope.

Public evidence milestones:

- internal n=484 cohort report: Dice WT `0.8108`, Dice ET `0.8033`, ET recall
  `0.8065`;
- selected Dataset832 fold artifact: label-2 Dice `0.8843`, label-2 recall
  `0.9085`, label-2 precision `0.8665` on 2 validation cases;
- formal-integrity status: Lean/Lake `3292/3292` tasks, root build exit code
  `0`, and public SHA-512 anchor for an internal integrity snapshot.

The review does not publish a clinical performance claim. It also does not
claim SOTA, medical-device status, MDR/AI Act compliance, safety certification,
production readiness, or external validation.

BraTS 2025 current results remain marked as `not available in current public
evidence` until a clean, aggregate-only evidence packet is prepared. The
verified local validation artifact currently referenced in the public evidence
review is a Dataset832/BraTS2024-labelled fold summary, not a confirmed BraTS
2025 aggregate package.

No patient data, images, masks, DICOM/NIfTI files, checkpoints, local paths,
controlled technical artifacts, or per-case records are redistributed.

## Customer Value

The customer value is not a better segmentation model claim. The value is a
control layer around model outputs: explainable gating, audit evidence, human
review triggers, escalation support, and a clearer separation between model
behavior and workflow decisions.

The broader commercial signal is scalability: one control kernel can support
many specialist profiles. The public demonstrator shows the repeatable public
shape of the control layer while keeping production-system material outside
the repository.

## Regulatory Readiness, Not Compliance

This repository may help organize evidence for future regulatory work, but it
does not claim EU AI Act compliance, MDR/MDSW compliance, CE marking, ISO
certification, production readiness, or clinical evaluation completion.

## Data Redistribution Disclaimer

This public repository redistributes no medical datasets, patient files, scans,
segmentations, masks, DICOM/NIfTI files, model checkpoints, or internal audit
records. Dataset provenance fields are included only when supported by current
local evidence; otherwise they are marked as `not available in current evidence`.

## Boundary Claims

This public demonstrator:

- has no external validation
- has no clinical or specialist consultation claim
- has no medical-device claim
- has no clinical validation claim
- does not contain production-system code
- does not prove that a model is correct
- does not guarantee that model outputs are correct
- does not execute downstream operational control

The public Lean file covers only abstract verdict logic. It does not prove the
Python implementation, HMAC construction, JSON serialization, floating-point
runtime behavior, production decision behavior, domain adapters, or clinical
safety.

Operational control remains with the operator, developer, workflow owner, or
supervising system.

## Commercial Direction

Commercial products are intended to be developed as proprietary enterprise
software. Specialist systems are the main commercialization path.

Lower-risk entry points include:

- LLM agents
- RAG systems
- enterprise copilots
- company chatbots
- tool-call review support
- human-review triggers
- workflow approvals

Possible product segmentation:

- **AOS Lite**: chatbot/LLM guard for microbusinesses and SMBs
- **AOS Business**: RAG audit and workflow approval
- **AOS Enterprise**: evidence store, integrations, governance
- **AOS Critical**: formal stack, on-prem/VPC, domain validation

Commercial variants may include deployment-specific engineering and performance
work. Implementation material outside the demonstrator and unreleased
performance evidence are outside this public repository.

## Performance And Evaluation Boundary

The public demonstrator reports only bounded, reproducible public evidence.
Customer-specific evaluation, deployment engineering, and unreleased performance
evidence remain outside this repository unless separately prepared for public
release.

## Shadow Benchmarking

Shadow benchmarking means evaluating model outputs and workflow decisions
against AOS control envelopes without claiming autonomous clinical or regulated
operation. In the public repository, this is represented by synthetic benchmark
comparisons, evidence JSON, and a public SHA-512 integrity anchor.

The current public SHA-512 integrity anchor is:

```text
c4124f59cec5d587a41563b7780a4e6b878a559b669ec293958ab04418899e1b580c1396905f3a731ac5009dab46220ccefce0699c93e65316a9b96133b89133
```

This hash is a public integrity anchor for an internal evidence snapshot. It is
not the evidence packet, not a model weight hash, not a clinical validation
claim, and not a production signature scheme.

## Radiology Note

Radiology is referenced only as a domain-adapter example. It is not a product in
this public repository and is not a medical-device or clinical-validation claim.

## Public Boundary

See:

- [Public boundary](docs/PUBLIC_BOUNDARY.md)
- [Plain-language overview](docs/PLAIN_LANGUAGE_OVERVIEW.md)
- [SDK boundary](docs/SDK_BOUNDARY.md)
- [Repository best practices](docs/REPOSITORY_BEST_PRACTICES.md)
- [Public architecture](docs/architecture.md)
- [Scope of Proof](SCOPE_OF_PROOF.md)
- [AI problems addressed](docs/AI_PROBLEMS_ADDRESSED.md)
- [Integrity anchors](docs/INTEGRITY_ANCHORS.md)
- [Universal kernel positioning](docs/UNIVERSAL_KERNEL_POSITIONING.md)
- [Commercialization direction](docs/COMMERCIALIZATION.md)
- [Development transparency](docs/DEVELOPMENT_TRANSPARENCY.md)
- [Clean-room test](docs/CLEAN_ROOM_TEST.md)
- [Hello-world example](examples/hello-world)
- [Radiology reference system](docs/RADIOLOGY_REFERENCE_SYSTEM.md)
- [Offline evaluation results](docs/OFFLINE_EVALUATION_RESULTS.md)
- [Radiology evidence review](docs/RADIOLOGY_EVIDENCE_REVIEW.md)
- [Dataset provenance](docs/DATASET_PROVENANCE.md)
- [Customer value](docs/CUSTOMER_VALUE.md)
- [Value metrics](docs/VALUE_METRICS.md)
- [Regulatory readiness](docs/REGULATORY_READINESS.md)
- [Performance and evaluation boundary](docs/CALIBRATION_AND_OPTIMIZATION.md)

## Technical Advantage Evidence

The public evidence layer compares the AOS demo gate with simple guardrail
baselines on synthetic scenarios. It shows how a deterministic interval gate can
block uncertainty-crossing cases that threshold-only, schema-only, or prompt-only
guards may pass.

See:

- [Technical advantage](docs/TECHNICAL_ADVANTAGE.md)
- [Universal kernel positioning](docs/UNIVERSAL_KERNEL_POSITIONING.md)
- [Benchmark summary](benchmarks/results/summary.md)
- [Lean proof surface](lean/AOSPublicCore.lean)
- [Radiology offline evidence JSON](evidence/radiology_offline_evaluation.json)
- [Radiology evidence review JSON](evidence/radiology_evidence_review.json)

## Development Note

AOS is an author-led system architecture. Technical ownership, publication
boundaries, IP strategy, and product direction remain with the maintainer.

## Run The Demonstrator

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest tests -q
python benchmarks/run_benchmarks.py
python -m json.tool benchmarks/results/metrics.json
python -m json.tool evidence/radiology_offline_evaluation.json
python -m json.tool evidence/radiology_evidence_review.json
lake build AOSPublicCore
python -m json.tool evidence/demonstrator_manifest.json
```

## License

This repository is published under a proprietary demonstrator notice. Viewing
the repository does not grant rights to copy, modify, distribute, commercialize,
or create derivative works without written permission.

See [LICENSE](LICENSE).
