# Radiology Evidence Review

This document records a bounded review of selected internal radiology evidence
summaries. It is intended to prevent stale or overbroad public claims while
keeping the public interpretation evidence-led.

Radiology remains a domain-adapter example. It is not a product in this public
repository and is not a medical-device, clinical-validation, MDR compliance,
SOTA, safety-certification, or production-readiness claim.

## Public Milestones

The public repository can safely disclose selected milestones when they remain
bounded as internal/offline evidence:

- Internal n=484 cohort report: Dice WT `0.8108`, Dice ET `0.8033`, ET recall
  `0.8065`.
- Selected Dataset832 fold artifact: label-2 Dice `0.8843`, label-2 recall
  `0.9085`, label-2 precision `0.8665` on 2 validation cases.
- Formal-integrity status: Lean/Lake `3292/3292` tasks, root build exit code
  `0`, signed SHA-512/Ed25519 manifest metadata.

The `0.8843` fold value is not relabeled here as Whole Tumor cohort
performance. The n=484 report milestone for Whole Tumor is `0.8108`.

## Verified Internal Artifacts

| Artifact class | Locally confirmed values | Public interpretation |
| --- | --- | --- |
| Dataset832/BraTS2024-labelled fold validation summary | sample count: 2 validation cases; label 2 is mapped as SNFH in local dataset metadata; label-2 Dice 0.8843; label-2 recall 0.9085; label-2 precision 0.8665 | Selected small-fold model-output evidence only. This is not a cohort-level result and is not published as Whole Tumor or BraTS 2025 performance. |
| Internal cohort report | n=484 offline cohort; Dice WT 0.8108; Dice ET 0.8033; ET recall 0.8065; 36 ET outliers below Dice 0.5 were listed for review | Internal offline report only. Certification or compliance wording is not carried into this public repository. |
| Formal verification status | 3292/3292 Lean tasks completed; Lake root build exit code 0; signed SHA-512/Ed25519 manifest; no sorry/admit/axiom/unsafe in audited core Lean sources | Internal formal-integrity status. It does not prove Python-to-Lean refinement, segmentation correctness, clinical safety, or production audit security. |

## Not Confirmed For Public Claiming

The following items were not accepted as public claims:

- Detection rate 92.56 percent as a cohort-level radiology metric.
- Recall 0.9085 as the n=484 cohort sensitivity result.
- BraTS 2025 current performance metrics.
- SOTA or broad comparative performance-superiority language.
- Safety-certification language.
- MDR, AI Act, CE, ISO, or medical-device compliance.
- Trust-index or revenue-ledger values as independent market validation.
- Domain-specific audit examples as production-grade public signatures.

## Integrity Anchor

The formal-integrity status references a SHA-512 payload hash for the latest
reviewed integrity snapshot:

```text
c4124f59cec5d587a41563b7780a4e6b878a559b669ec293958ab04418899e1b580c1396905f3a731ac5009dab46220ccefce0699c93e65316a9b96133b89133
```

This is a public anchor only. It does not expose weights, data, controlled
technical material, or the manifest body.

For future public evidence packets, the recommended anchor set is SHA-256 for
quick verification, SHA-512 for audit-grade verification, and Ed25519 signature
metadata for authenticity and provenance.

## Shadow Benchmarking

Shadow benchmarking means evaluating model outputs and workflow decisions
against AOS control envelopes before any claim of deployment readiness. It is
useful because AOS is a control layer over model use rather than a model-only
benchmark.

In this public repository, shadow benchmarking is represented only by synthetic
benchmarks, evidence JSON, and the integrity anchor above.

## Performance And Evaluation Boundary

The public repository reports only bounded, aggregate public evidence. It does
not include customer-specific deployment details, unreleased performance traces,
or production deployment material.

## Safe Public Summary

The defensible public statement is:

```text
Selected internal evidence summaries include promising radiology model-output
metrics and a successful formal-integrity build, but this repository does not
publish clinical validation, production readiness, regulatory compliance, or
SOTA claims. AOS is presented here as an explainable/verifiable control layer
around model outputs, not as a validated radiology product.
```

Machine-readable summary:
[`evidence/radiology_evidence_review.json`](../evidence/radiology_evidence_review.json).
