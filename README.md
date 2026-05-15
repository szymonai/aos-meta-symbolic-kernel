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

## Radiology Note

Radiology is referenced only as a domain-adapter example. It is not a product in
this public repository and is not a medical-device or clinical-validation claim.

## Public Boundary

See:

- [Public boundary](docs/PUBLIC_BOUNDARY.md)
- [Commercialization direction](docs/COMMERCIALIZATION.md)
- [Development transparency](docs/DEVELOPMENT_TRANSPARENCY.md)
- [Clean-room test](docs/CLEAN_ROOM_TEST.md)

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
lake build AOSPublicCore
python -m json.tool evidence/demonstrator_manifest.json
```

## License

This repository is published under a proprietary demonstrator notice. Viewing
the repository does not grant rights to copy, modify, distribute, commercialize,
or create derivative works without written permission.

See [LICENSE](LICENSE).
