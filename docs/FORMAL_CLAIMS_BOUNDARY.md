# Formal Claims Boundary

This document defines what the public Lean proof surface can and cannot support.
It is a claim-control document, not a broad formal-verification claim.

## Current Scope

| Layer | Public status |
| --- | --- |
| Lean model | abstract integer interval verdict logic |
| Lean target | `AOSPublicCore` |
| Runtime reference | Python demo gate |
| Runtime bridge | bounded correspondence tests only |
| Full Python-to-Lean refinement | not established |
| Production correctness | not claimed |
| Domain, clinical, regulatory, or safety certification | not claimed |

## Allowed Claims

- Lean verifies selected properties of the abstract `PASS` / `WARN` / `BLOCK`
  verdict model.
- The public Lean model covers integer interval behavior, warning-band behavior,
  deterministic verdict structure, and monotonicity with respect to the modeled
  upper bound.
- Python tests demonstrate that the public reference implementation matches the
  same verdict behavior on a bounded integer-like runtime subset.
- Benchmark metrics demonstrate behavior on the included synthetic scenarios.

## Not Allowed

- full-system verification language;
- Python runtime verification language;
- production correctness language;
- benchmark-as-production-evidence language;
- formal-task-count-as-quality language;
- language that treats `PASS` as truth, final approval, clinical validity,
  regulatory compliance, or deployment safety.

## Formal Claim Inventory

| Claim ID | Lean item | Meaning | Runtime bridge | Risk |
| --- | --- | --- | --- | --- |
| FC-001 | `blockVerdictCorrect` | `upperBound > limit` yields `block` | bounded correspondence tests | LOW |
| FC-002 | `passVerdictCorrect` | pass region yields `pass` | bounded correspondence tests | LOW |
| FC-003 | `warnVerdictCorrect`, `warnVerdictOnlyWithinBand` | warning band yields `warn` and stays inside the modeled band | bounded correspondence tests | LOW |
| FC-004 | `deterministicVerdict` | verdict is one of `pass`, `warn`, `block` | replay tests | LOW |
| FC-005 | `verdictMonotoneWithUpperBound` | increasing modeled upper bound cannot reduce verdict severity | bounded runtime monotonicity tests | MEDIUM |

## Assumptions

| Assumption | Status |
| --- | --- |
| Lean values are integers | explicit |
| Python demo uses finite numeric values converted to `float` | explicit and tested for selected invalid values |
| Runtime tests use integer-like values where Python float preserves exact small integers | explicit |
| JSON parsing, IO, HMAC, keys, persistence, deployment, and concurrency are outside the Lean model | explicit |
| Public benchmark labels are synthetic demo labels, not domain truth | explicit |

## Lean To Runtime Bridge

Current bridge:

```text
Lean intervalVerdict over Int
  -> Python derive_verdict over finite numeric values
  -> bounded integer-like correspondence tests
  -> synthetic benchmark behavior
  -> public evidence JSON
```

This bridge improves confidence in the public demonstrator but is not a full
refinement proof. It does not cover arbitrary floats, JSON number edge cases,
serialization, HMAC security, key lifecycle, policy calibration, IO,
concurrency, deployment, or domain adapters.

## Nontriviality Review

| Proof group | Value | Boundary |
| --- | --- | --- |
| verdict branch correctness | useful | mostly direct from the public definition |
| warning-band reverse property | useful | stronger than a one-way branch check |
| deterministic verdict coverage | modest | confirms trivalent structure, not system correctness |
| monotonicity | useful | meaningful abstract invariant, runtime bridge remains bounded |

## Task Count Boundary

Task counts are build evidence only. They do not measure theorem quality,
specification adequacy, runtime correctness, product readiness, or safety.

Acceptable wording:

> The selected Lean target builds in the declared environment; the scope and
> limits of the formal claims are documented separately.

## Requirement Map

| Requirement | Formal item | Runtime evidence | Residual gap |
| --- | --- | --- | --- |
| unsafe interval crossings block | `blockVerdictCorrect` | unit tests, benchmark | no full runtime refinement |
| safe interval cases pass | `passVerdictCorrect` | unit tests, benchmark | no domain calibration |
| warning-band cases warn | `warnVerdictCorrect` | unit tests, benchmark | workflow response outside scope |
| higher modeled risk cannot reduce severity | `verdictMonotoneWithUpperBound` | bounded monotonicity tests | only integer-like runtime subset |
| decisions can carry demo evidence | outside Lean | digest and replay tests | no production signing proof |

## Stronger Claim Requirements

To support stronger claims, the project would need:

- a source-reviewed formal requirements matrix;
- executable-spec or refinement tests covering the full runtime contract;
- numeric boundary tests for decimal and floating-point behavior;
- evidence schema conformance tests;
- signed evidence packet verification;
- security and key-management review;
- deployment and concurrency review;
- independent domain evaluation for any specialist profile.
