# Technical Diligence Boundary

This repository can support technical diligence. It cannot, by itself, support
an investment decision, production-readiness conclusion, customer-traction
claim, commercial forecast, IP clearance, or regulated-use claim.

## What This Repository Can Support

| Diligence question | Public evidence | Current answer |
| --- | --- | --- |
| Is there a coherent technical primitive? | Python reference runtime, control spec, architecture docs | Yes, within the public demonstrator boundary |
| Is the core behavior reproducible? | Tests, benchmark `--check` commands, integrity manifest | Yes, for committed public artifacts |
| Is there production-relevant evidence? | Operational replay over public frozen traces | Yes, as offline replay evidence, not deployment proof |
| Is the result auditable? | SHA-linked evidence, replay checks, per-run metrics | Yes, as local demonstrator auditability |
| Is there a formal surface? | Lean 4 verdict model | Yes, for selected abstract verdict invariants only |
| Are claim boundaries explicit? | Manifests, publication tests, docs | Yes |

Current public technical claim:

> AOS demonstrates a deterministic, replayable control pattern for bounded
> signals, with production-relevant offline replay evidence over public
> operational traces and a narrow formal verdict surface.

## What This Repository Cannot Support

The public repository does not establish:

- production deployment readiness;
- customer validation;
- paid usage or commercial demand;
- deployment economics;
- defensibility of proprietary implementation details;
- patentability, freedom to operate, or IP ownership conclusion;
- production security posture;
- external validation;
- regulated-use readiness;
- service-level objectives;
- live-model or live-agent effectiveness.

## Investor-Grade Diligence Needs A Separate Data Room

An investor-grade technical and commercial review would normally require
private or controlled materials outside this public demonstrator:

| Area | Required private artifact |
| --- | --- |
| Product architecture | Full system architecture, production boundaries, adapter design |
| Product readiness | Deployment plan, API/runtime status, failure-handling design |
| Validation | External or customer-adjacent replay, pilot protocol, held-out results |
| Commercial evidence | Use-case prioritization, buyer profile, pricing hypothesis, pipeline evidence |
| Security | Threat model, key-management plan, audit-log architecture, abuse cases |
| IP | Counsel-reviewed IP memo, repository provenance, third-party dependency review |
| Operations | Observability, incident response, release process, support boundary |
| Governance | Data handling, privacy boundary, regulated-use exclusion or plan |

These materials should not be placed in this public repository unless cleared
for release.

## Evidence Maturity

| Stage | Evidence | Status |
| --- | --- | --- |
| Public demonstrator | Deterministic gate, replay, Lean surface, bounded docs | Included |
| Public production-relevant replay | Public operational traces, scale, auditability, falsification criteria | Included |
| Multi-dataset operational replay | Additional public operational datasets and matched policies | Not included |
| External replication | Independent run or third-party verification | Not included |
| Pilot shadow mode | Customer or deployment-adjacent workflow replay | Not included |
| Production deployment | Live service, SLA, monitoring, incident process | Not included |

## Practical Investor Reading

The repository is useful for answering:

- whether the technical pattern is coherent;
- whether the public control path is deterministic and replayable;
- whether the strongest current public evidence is falsifiable;
- whether the project avoids claiming more than the evidence supports.

The repository is insufficient for answering:

- whether customers will buy it;
- whether the implementation is production-ready;
- whether the company has a defensible moat;
- whether the technology has passed independent validation;
- whether the system is safe for regulated deployment.

The correct diligence status is:

```text
public technical evidence: credible but bounded
production proof: not established
commercial proof: not established in this repository
investor-grade review: requires private data room
```
