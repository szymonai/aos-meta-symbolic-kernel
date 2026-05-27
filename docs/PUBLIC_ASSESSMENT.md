# Public Assessment

This document is the current public assessment of AOS usefulness, scalability,
and evidence quality. It summarizes existing artifacts only; it does not add a
production, clinical, regulated-use, external-validation, or general
effectiveness claim.

## Assessment Matrix

| Axis | Current evidence | Current conclusion |
| --- | --- | --- |
| Usefulness | Operational replay, synthetic control checks, audit/replay records | Useful as a deterministic control and review-routing layer over bounded signals |
| Scalability | 362,774 evaluated public records across 58 source series | Shows offline replay at hundreds-of-thousands-of-records scale, not service capacity |
| Evidence quality | Public frozen traces, fixed policy, artifact hashes, Lean verdict surface | Strong enough for a bounded production-relevant replay claim; insufficient for production effectiveness |

## Usefulness

AOS is useful when the workflow already has a bounded signal that can be routed
under an explicit policy:

```text
bounded signal -> PASS / WARN / BLOCK -> audit record -> replay
```

The current public evidence supports these use cases:

- review routing before downstream workflow action;
- silent-pass-through measurement for risky records or windows;
- deterministic replay of public demonstrator decisions;
- explicit measurement of false blocks and intervention load;
- separation of model output, policy verdict, audit record, and final decision.

The current public evidence does not establish domain utility, clinical utility,
business ROI, deployment safety, or user acceptance.

## Scalability

The public runtime contract is constant-time per already-normalized signal:

```text
value + uncertainty -> compare with limit and warning margin -> verdict
```

The operational replay adds a deterministic rolling signal extractor before the
gate. With a fixed rolling window, the replay behaves as a linear pass over the
input records for practical public-review purposes. The current committed
replay artifacts report:

| Metric | Value |
| --- | ---: |
| Source series | 58 |
| Evaluated records | 362,774 |
| Labeled anomaly windows | 116 |
| AOS audit coverage | 100.00% |
| AOS replay success | 100.00% |

This is scalability evidence for reproducible offline replay and audit volume.
It is not evidence for distributed throughput, production latency, availability,
capacity planning, GPU acceleration, or service-level objectives.

The committed metrics encode this as a `scalability_profile`, including the
scale unit, evaluated record count, gate complexity, extractor complexity, and
unsupported production-capacity claims.

## Evidence

| Evidence layer | Strength | What it supports | What it does not support |
| --- | --- | --- | --- |
| Lean 4 verdict surface | High for narrow abstract invariants | Selected verdict-contract properties | Runtime equivalence, signal extraction, effectiveness |
| Operational control replay | Medium to high for public control behavior | Offline control behavior on public frozen traces | Production deployment or universal effectiveness |
| Synthetic benchmark | Low to medium | Regression checks and baseline comparison | Real-world effectiveness |
| Controlled-study runner | Protocol evidence | Study completeness checks | Effectiveness without real frozen outputs and audit |
| Integrity manifest | Repository consistency evidence | Selected artifact hash checks | Release signing, external validation |

Current strongest empirical result:

| Metric | AOS value |
| --- | ---: |
| Anomaly-window review/block rate | 96.55% |
| Anomaly-window silent pass rate | 3.45% |
| Record-level anomaly review/block rate | 14.68% |
| False block rate | 8.69% |
| Nominal intervention rate | 12.76% |
| Audit coverage | 100.00% |
| Replay success | 100.00% |

The result is useful because it reports both detection-side behavior and review
load. It is bounded because it is offline, uses a fixed public policy, and does
not prove that the signal extractor is optimal.

The committed metrics also include:

- `production_relevance_profile`;
- `auditability_profile`;
- `falsification_profile`.

These profiles make the replay falsifiable: artifact drift, audit replay
failure, label leakage into AOS input signals, or changed claim-boundary flags
invalidate the public claim.

## Decision Boundary

The public repository can support this technical claim:

> AOS demonstrates a deterministic, replayable control pattern for bounded
> signals, with production-relevant offline replay evidence over public
> operational traces and a narrow formal verdict surface.

The public repository cannot yet support these stronger claims:

- AOS is production ready;
- AOS is clinically ready;
- AOS has general effectiveness across AI systems;
- AOS reduces hallucinations in live LLM or agent deployments;
- AOS meets production latency or availability requirements;
- native, GPU, or hardware backends are verified.

## Upgrade Path

A stronger public evidence package would require:

- frozen outputs or traces from named public datasets;
- independent signal extraction that does not use labels as AOS input signals;
- held-out manual audit or external review;
- matched comparator inputs;
- reported false blocks, silent passes, and intervention load;
- reproducible commands and artifact hashes;
- explicit separation between protocol evidence, control evidence, and
  production evidence.
