# Demonstrator Comparison Evidence

This document describes what the public AOS demonstrator compares. It should be
read as a small reproducibility check, not as a broad performance or superiority
claim.

## Technical Thesis

AOS is demonstrated here as a deterministic runtime assurance pattern:

```text
model output + uncertainty -> explicit gate -> PASS / WARN / BLOCK
  -> audit evidence -> abstract formal invariants
```

The useful signal is the combination of:

- a deterministic gate that evaluates uncertainty before workflow use;
- audit evidence attached to each demo decision;
- explicit claim-boundary fields in machine-readable evidence;
- a small Lean proof surface for abstract verdict logic;
- a repeatable path from one control pattern to multiple application profiles.

## Demonstrator Scope

The public benchmark layer covers 12 synthetic scenarios. It compares the AOS
demo gate against simple baseline guards:

- a threshold-only `if/else` guard;
- a JSON-shape guard;
- a deterministic text heuristic that simulates prompt-only guardrails.

The benchmark records false passes, false positive blocks, exact verdict match,
unsafe block rate, safe pass rate, warning preservation, audit coverage, verdict
counts, and deterministic replay. It is intentionally small and exists to make
the control pattern inspectable.

The current benchmark has limited statistical weight:

- 12 synthetic scenarios total;
- three intentionally simple baselines;
- no external guardrail frameworks in the comparison set;
- no claim of statistical significance, production performance, or domain
  superiority.

The public AOS demo gate performs well in this narrow setup because it evaluates
`value + uncertainty` against the limit and warning band. The simple baselines
do not evaluate that uncertainty envelope.

## Explicit Limits

This repository does not prove:

- broad performance claims;
- domain performance;
- external validation;
- external-framework comparison;
- statistical significance;
- Python-to-Lean refinement;
- equivalence between Python runtime behavior and Lean logic;
- production audit-envelope security;
- suitability for regulated or safety-critical deployment;
- correctness of an upstream AI model.

The Lean proof surface covers abstract verdict ordering and interval logic only.
It uses integer arithmetic and does not prove the floating-point execution path
in the Python reference implementation.

## Radiology Reference Scenario

Radiology is one reference profile for understanding how the control pattern can
organize model output, uncertainty, audit evidence, and review escalation. It is
not a clinical-validity, medical-device, regulatory-compliance, or
production-readiness claim.

Current radiology performance numbers are intentionally not presented as active
README claims. Focused evidence documents keep those values separate from the
first-read project positioning.

## Synthetic Comparison

| Approach | What It Checks | Handles Uncertainty | Audit Evidence | Formal Invariants | Expected Weakness |
| --- | --- | --- | --- | --- | --- |
| Plain `if/else` threshold | `value <= limit` | No | No | No | Can pass cases when uncertainty crosses the limit |
| JSON schema validation | Shape and basic types | No | No | No | Valid structure can still contain unsafe values |
| Prompt-only guardrail | Text cues or policy wording | No deterministic numeric bound | No | No | Can miss unsafe cases when wording is benign or indirect |
| AOS public demo gate | `value + uncertainty` against the limit and warning band | Yes | Demo digest | Abstract Lean verdict invariants | Public demo only |

## Reading The Results

The benchmark is trivalent: expected decisions can be `PASS`, `WARN`, or
`BLOCK`. For the safety-control interpretation, expected `BLOCK` cases are
treated as the positive class:

- `false_pass` is a critical miss: an expected `BLOCK` case was not blocked.
  This corresponds to a safety-control false negative.
- `false_block` or `false_positive_block` is a false alarm: an expected `PASS`
  or `WARN` case was blocked.
- `unsafe_block_rate` is the share of expected `BLOCK` cases that were actually
  blocked.
- `exact_match_rate` measures exact agreement with the expected
  `PASS` / `WARN` / `BLOCK` label.
- `audit_coverage_rate` measures whether decisions include audit evidence.

See:

- [Benchmark summary](../benchmarks/results/summary.md)
- [Benchmark metrics JSON](../benchmarks/results/metrics.json)
- [Value metrics](VALUE_METRICS.md)
- [Radiology evidence review](RADIOLOGY_EVIDENCE_REVIEW.md)
- [Lean proof surface](../lean/AOSPublicCore.lean)
