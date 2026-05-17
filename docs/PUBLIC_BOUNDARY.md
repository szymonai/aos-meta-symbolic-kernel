# Public Boundary

This repository is a limited public demonstrator.

The public goal is high information density: enough structure, code, tests,
proof surface, and evidence context for a serious reviewer to understand the
AOS control thesis while avoiding unsupported claims.

See also:

- [AOS Public Abstraction Map](ABSTRACTION_MAP.md)
- [Information Architecture](INFORMATION_ARCHITECTURE.md)
- [IP Protection Policy](IP_PROTECTION.md)
- [Publication Safety Checklist](PUBLICATION_CHECKLIST.md)

## Public

- simplified PASS/WARN/BLOCK gate
- synthetic examples only
- basic audit concept
- abstract Lean verdict logic
- basic tests and CI
- bounded evidence summaries and claim-boundary manifests
- high-level positioning material

## Outside This Public Repository

- full proprietary system
- production security, deployment, or commercial delivery materials
- customer, partner, patient, model, or dataset artifacts

Do not treat this public repository as a blueprint for the production system.

## Evaluation Boundaries

The public repository does not establish production calibration, production
security architecture, Python-to-Lean runtime refinement, load performance,
domain-adapter quality, enterprise deployment economics, or customer-specific
operational readiness.

Those areas require separate evaluation artifacts and are outside the limited
public demonstrator.

## Claims Not Made

- no external validation
- no medical-device claim
- no clinical validation claim
- no autonomous operational-control claim
- no claim that AOS guarantees model correctness
- no claim that AOS eliminates hallucinations
- no production-readiness claim
- no regulatory-compliance claim
- no SOTA claim

Control remains with the operator, developer, workflow owner, or supervising
system.
