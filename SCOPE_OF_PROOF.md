# Scope Of Proof

This repository is a public demonstrator of the AOS runtime assurance pattern.
Its proof surface is useful, but intentionally narrow.

For claim-level interpretation, see
[Formal Claims Boundary](docs/FORMAL_CLAIMS_BOUNDARY.md).

## Proven

- deterministic abstract verdict logic in the public Lean proof surface
- explicit policy evaluation in the public interval-gate demonstrator
- audit digest generation for demonstrator decisions
- reproducible JSON evidence for the current synthetic benchmark set

## Numeric Model Boundary

The public Lean proof surface uses integer arithmetic for abstract interval
verdict logic. The Python reference implementation accepts finite numeric
inputs and evaluates floating-point values at runtime.

No full proof is published here that converts the Python floating-point
execution path into the Lean integer model. The repository includes bounded
runtime correspondence tests for integer-like values, but the Lean result should
still be read as a proof over the abstract verdict structure, not as a proof of
Python runtime semantics, JSON number parsing, floating-point rounding, or a
model-output conversion layer.

## Demonstrated

- model-output signal to `PASS` / `WARN` / `BLOCK` decision flow
- SHA-256-linked audit trace in the public demonstrator
- domain-neutral control-layer shape
- clean-room repeatability using only the public repository contents

## Not Claimed

- Python-to-Lean refinement
- full Python numeric runtime behavior
- full Int/Float correspondence between code and proof artifacts
- production SDK completeness
- production security or deployment readiness
- domain validation or regulated-use approval
- regulatory approval or safety approval
- external validation or independent assessment
- product performance in deployment environments
- production-system completeness
- production calibration, load performance, domain-adapter quality, deployment
  economics, or operational readiness
- materials outside this public demonstrator

The public repository should be read as a technical credibility signal and
repeatable runtime assurance demonstrator.
