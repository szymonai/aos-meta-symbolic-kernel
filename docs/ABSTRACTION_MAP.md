# AOS Public Abstraction Map

AOS is built as a layered assurance system. This public repository exposes the
smallest useful slice of that architecture: enough to show the control pattern,
not enough to disclose the proprietary core.

## Public Layer Stack

| Layer | Public object | Purpose | Private counterpart withheld |
| --- | --- | --- | --- |
| L0 | Model-output signal | Input value plus uncertainty proxy | Domain adapters, feature contracts, calibration sources |
| L1 | Interval gate | Deterministic PASS/WARN/BLOCK verdict | Policy engine, threshold lifecycle, control envelopes |
| L2 | Demo audit digest | Reproducible evidence that a decision was made | Full audit contract, signatures, evidence store, key management |
| L3 | Synthetic scenarios | Bounded behavioral examples | Private benchmark corpus, deployment traces, specialist evaluations |
| L4 | Lean verdict logic | Abstract proof surface for verdict invariants | Private proof stack, refinement claims, domain safety proofs |
| L5 | Evidence summaries | Aggregate and bounded evidence inventory | Raw data, case-level records, models, manifests, certificates |
| L6 | Public boundary docs | Claim discipline and publication safety | Commercial SDK/API, specialist products, optimization layers |

## Core Control Shape

```text
model output or metadata
  -> uncertainty / quality / risk signal
  -> deterministic control envelope
  -> PASS / WARN / BLOCK
  -> audit evidence
  -> human review, escalation, or workflow hold
```

The public implementation demonstrates this shape with a single interval gate:

```text
upper_bound = value + uncertainty

upper_bound > limit                 -> BLOCK
upper_bound > limit - warn_margin   -> WARN
otherwise                           -> PASS
```

This simplification is intentional. It preserves the core assurance idea while
withholding private calibration, policy semantics, adapter contracts, and domain
validation methods.

## What The Public Repo Proves

The public repo can show that:

- the demonstrator gate is deterministic;
- synthetic unsafe interval-crossing cases are blocked by the AOS adapter;
- demo audit digests are reproducible and tamper-sensitive;
- the Lean file proves abstract verdict invariants for the simplified model;
- public evidence files preserve explicit claim boundaries.

## What The Public Repo Does Not Prove

The public repo does not prove:

- model correctness;
- Python-to-Lean refinement;
- production audit security;
- clinical validity;
- regulatory compliance;
- SOTA performance;
- autonomous operational control;
- safety of any private specialist profile.

## Information-Dense Reading Path

For a fast technical review, read in this order:

1. `README.md` for project thesis and public boundary.
2. `core/aos_public_core.py` for the executable control primitive.
3. `benchmarks/results/summary.md` for the synthetic comparison.
4. `lean/AOSPublicCore.lean` for the proof surface.
5. `evidence/demonstrator_manifest.json` for machine-readable claim limits.
6. `evidence/radiology_evidence_review.json` for bounded evidence context.
7. `docs/IP_PROTECTION.md` before publishing or reusing any material.
