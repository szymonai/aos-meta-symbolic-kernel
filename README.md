# AOS Limited Public Demonstrator

AI Runtime Assurance / AI Control Layer.

TL;DR:

```text
AI output -> simple gate -> PASS / WARN / BLOCK -> demo audit record
```

This repository is a **limited proof-of-capability demonstrator**. It is not the
full proprietary AOS Core and is not a production SDK.

AOS is not another AI model. AOS is a control layer around AI model outputs.
The goal is to help convert uncertain model output into auditable decisions:
allow, warn, block, or escalate.

## What Is Public Here

This repository contains only:

- a simplified `PASS` / `WARN` / `BLOCK` interval gate
- synthetic demonstration examples
- a basic audit concept
- a small Lean proof surface for abstract verdict logic
- basic tests and CI
- high-level positioning material

## What Is Not Public

This repository does not contain:

- full AOS Core
- full audit contract
- policy semantics
- adapter protocol
- validation stack
- specialist systems
- real thresholds or calibration logic
- private formal proof stack
- private benchmark evidence
- CUDA/PTX/C++/assembler optimization code
- commercial SDK/API
- the private data -> calibration -> policy -> workflow -> validation path

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

The public repository now includes a sanitized evidence review for selected
private radiology artifacts. It records which values were locally confirmed,
which values belong to a small validation fold, which values belong to an
internal cohort report, and which claims remain withheld.

The review does not publish a clinical performance claim. It also does not
claim SOTA, medical-device status, MDR/AI Act compliance, SIL equivalence,
production readiness, or external validation.

BraTS 2025 current results remain marked as `not available in current public
evidence` until a clean, aggregate-only evidence packet is prepared. The
verified local validation artifact currently referenced in the public evidence
review is a Dataset832/BraTS2024-labelled fold summary, not a confirmed BraTS
2025 aggregate package.

No patient data, images, masks, DICOM/NIfTI files, checkpoints, local paths,
private thresholds, or per-case records are redistributed.

## Customer Value

The customer value is not a better segmentation model claim. The value is a
control layer around model outputs: explainable gating, audit evidence, human
review triggers, escalation support, and a clearer separation between model
behavior and workflow decisions.

## Regulatory Readiness, Not Compliance

This repository may help organize evidence for future regulatory work, but it
does not claim EU AI Act compliance, MDR/MDSW compliance, CE marking, ISO
certification, production readiness, or clinical evaluation completion.

## Data Redistribution Disclaimer

This public repository redistributes no medical datasets, patient files, scans,
segmentations, masks, DICOM/NIfTI files, model checkpoints, or private audit
records. Dataset provenance fields are included only when supported by current
local evidence; otherwise they are marked as `not available in current evidence`.

## Boundary Claims

This public demonstrator:

- has no external validation
- has no clinical or specialist consultation claim
- has no medical-device claim
- has no clinical validation claim
- does not contain the full AOS Core
- does not prove that a model is correct
- does not eliminate LLM or agent hallucinations
- does not control agents or execute operational control for them

The public Lean file covers only abstract verdict logic. It does not prove the
Python implementation, HMAC construction, JSON serialization, floating-point
runtime behavior, production policy logic, domain adapters, or clinical safety.

Operational control remains with the operator, developer, workflow owner, or
supervising system.

## Commercial Direction

The commercial system is intended to be developed privately as proprietary
enterprise software. Specialist systems built on the private AOS Core are the
main commercialization path.

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

Private/commercial variants may support multi-level runtime optimization across
Python, C++, CUDA/PTX, assembler-level, or other low-level execution layers.
No optimization code, benchmark, or implementation detail is published here.

## Calibration And Optimization

In the private system, calibration and optimization are part of the specialist
profile lifecycle: model output quality, uncertainty, control thresholds,
latency, throughput, and deployment envelope can be tuned per domain. The
public demonstrator only describes this capability at a high level. It does not
publish calibration curves, real clinical thresholds, benchmark traces,
deployment settings, or low-level optimization code.

## Radiology Note

Radiology is referenced only as a domain-adapter example. It is not a product in
this public repository and is not a medical-device or clinical-validation claim.

## Public Boundary

See:

- [Public boundary](docs/PUBLIC_BOUNDARY.md)
- [Commercialization direction](docs/COMMERCIALIZATION.md)
- [Development transparency](docs/DEVELOPMENT_TRANSPARENCY.md)
- [Clean-room test](docs/CLEAN_ROOM_TEST.md)
- [Radiology reference system](docs/RADIOLOGY_REFERENCE_SYSTEM.md)
- [Offline evaluation results](docs/OFFLINE_EVALUATION_RESULTS.md)
- [Radiology evidence review](docs/RADIOLOGY_EVIDENCE_REVIEW.md)
- [Dataset provenance](docs/DATASET_PROVENANCE.md)
- [Customer value](docs/CUSTOMER_VALUE.md)
- [Regulatory readiness](docs/REGULATORY_READINESS.md)
- [Calibration and optimization](docs/CALIBRATION_AND_OPTIMIZATION.md)

## Technical Advantage Evidence

The public evidence layer compares the AOS demo gate with simple guardrail
baselines on synthetic scenarios. It shows how a deterministic interval gate can
block uncertainty-crossing cases that threshold-only, schema-only, or prompt-only
guards may pass.

See:

- [Technical advantage](docs/TECHNICAL_ADVANTAGE.md)
- [Benchmark summary](benchmarks/results/summary.md)
- [Lean proof surface](lean/AOSPublicCore.lean)
- [Radiology offline evidence JSON](evidence/radiology_offline_evaluation.json)
- [Radiology evidence review JSON](evidence/radiology_evidence_review.json)

## Development Transparency

AOS is an author-led system architecture developed with support from
AI-assisted coding environments such as VS Code, Codex, Kilo Code and Google
Antigravity. These tools assist implementation, refactoring and verification
workflows, but do not define the system architecture, IP strategy, product
direction or technical ownership.

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
