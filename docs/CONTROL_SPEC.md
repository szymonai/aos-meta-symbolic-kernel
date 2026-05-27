# Control Spec

This document is the public contract for the limited AOS demonstrator. It binds
the public core, API-shaped example, benchmark runners, evidence packets, and
Lean proof surface to one small control model.

It is not a production SDK specification, security architecture, regulated-use
specification, or deployment protocol.

## Input Contract

The API-shaped demonstrator accepts one bounded signal object:

| Field | Type | Constraint |
| --- | --- | --- |
| `signal_id` | string | non-empty |
| `score` | integer | `0 <= score <= 10000` |
| `uncertainty` | integer | `0 <= uncertainty <= 10000` |
| `limit` | integer | `0 <= limit <= 10000` |
| `warn_margin` | integer | `0 <= warn_margin < limit` |
| `metadata_complete` | boolean | required |
| `policy_id` | string | optional, non-empty when supplied |
| `policy_version` | string | optional, non-empty when supplied |

The public score space is fixed-point. The value `10000` represents the top of
the public demonstrator scale. The public repository does not claim that these
numbers are calibrated to any production domain.

## Verdict Contract

For a complete input:

```text
upper_bound = score + uncertainty
safe_limit = limit - warn_margin
```

The verdict is:

| Condition | Verdict |
| --- | --- |
| `metadata_complete == false` | `BLOCK` |
| `upper_bound <= safe_limit` | `PASS` |
| `safe_limit < upper_bound <= limit` | `WARN` |
| `upper_bound > limit` | `BLOCK` |

`PASS` means the bounded public signal is inside the public safe envelope.
`WARN` means the bounded public signal enters the review band. `BLOCK` means the
bounded public signal is incomplete or outside the allowed envelope.

The verdict is a control-layer decision. It is not a model-correctness,
domain-safety, production-readiness, or regulated-use decision.

## Evidence Contract

The demonstrator evidence packet contains:

| Field | Meaning |
| --- | --- |
| `schema_version` | public evidence schema identifier |
| `signal_id` | input identifier |
| `verdict` | `PASS`, `WARN`, or `BLOCK` |
| `reason` | deterministic reason string |
| `input_digest` | SHA-256 tag over canonical input JSON |
| `audit_id` | SHA-256 tag over selected evidence material |
| `policy_id` | policy identifier carried by the input |
| `policy_version` | policy version carried by the input |
| `replayable` | public replay flag |
| `claim_boundary` | explicit false flags for non-public claims |
| `input` | replay input material |

Canonical JSON uses sorted keys, compact separators, UTF-8, and rejects NaN.
Replay succeeds only when the evidence fields match the evidence rebuilt from
the included input.

## Repository Correspondence

| Layer | Required correspondence |
| --- | --- |
| `core/` | canonical public parsing, verdict, evidence, and replay logic |
| `examples/api-gate/` | imports and exposes the canonical public core |
| `benchmarks/` | measures public gate behavior and baseline behavior |
| `tests/` | checks runtime boundaries, replay, docs paths, and manifest hashes |
| `lean/` | verifies selected abstract verdict invariants |
| `evidence/` | records claim boundaries and artifact integrity anchors |

Any future public claim must identify the exact layer, artifact, dataset
boundary, metric, and non-claim boundary it depends on.

## Formal Boundary

The Lean proof surface is bound to the verdict contract above, not to the full
Python runtime or any domain model. It is sufficient for selected properties of
the abstract control model:

- complete metadata is required before interval evaluation;
- exceeding the limit returns `BLOCK`;
- the warning band returns `WARN`;
- the safe band returns `PASS`;
- verdict severity is monotone with the upper bound;
- effectiveness evidence cannot be claimed without the protocol and
  effectiveness gates.

It does not prove parser correctness, floating-point behavior, Python-to-Lean
refinement, signal quality, threshold calibration, deployment safety, or domain
validity.
