# Radiology Evidence Review

This document records a sanitized review of selected private radiology
artifacts. It is intended to prevent stale or overbroad public claims while
still showing that internal evidence exists.

Radiology remains a domain-adapter example. It is not a product in this public
repository and is not a medical-device, clinical-validation, MDR compliance,
SIL, SOTA, or production-readiness claim.

## Verified Internal Artifacts

| Artifact class | Locally confirmed values | Public interpretation |
| --- | --- | --- |
| Dataset832/BraTS2024-labelled fold validation summary | sample count: 2 validation cases; label 2 is mapped as SNFH in local dataset metadata; label-2 Dice 0.8843; label-2 recall 0.9085; label-2 precision 0.8665 | Selected small-fold model-output evidence only. This is not a cohort-level result and is not published as Whole Tumor or BraTS 2025 performance. |
| Internal cohort report | n=484 in-silico cohort; Dice WT 0.8108; Dice ET 0.8033; ET recall 0.8065; 36 ET outliers below Dice 0.5 were listed for review | Internal offline report only. Certification or compliance wording from private drafts is not carried into this public repository. |
| Formal verification status | 3292/3292 Lean tasks completed; Lake root build exit code 0; signed SHA-512/Ed25519 manifest; no sorry/admit/axiom/unsafe in audited core Lean sources | Private formal-integrity evidence. It does not prove Python-to-Lean refinement, segmentation correctness, clinical safety, or production audit security. |

## Not Confirmed For Public Claiming

The following items were not accepted as public claims:

- Detection rate 92.56 percent as a cohort-level radiology metric.
- Recall 0.9085 as the n=484 cohort sensitivity result.
- BraTS 2025 current performance metrics.
- SOTA or broad comparative performance-superiority language.
- SIL-equivalent safety language.
- MDR, AI Act, CE, ISO, or medical-device compliance.
- Trust-index or revenue-ledger values as independent market validation.
- Domain-specific private audit examples as production-grade public signatures.

## Calibration And Optimization Boundary

Calibration and optimization are important to the private specialist lifecycle:
uncertainty quality, thresholds, latency, throughput, memory envelope, and
deployment settings may be tuned per domain. The public repository only states
that this capability exists at a high level.

The public repository does not include calibration curves, real clinical
thresholds, per-case records, private policy logic, CUDA/PTX/C++/assembler
implementation details, benchmark traces, or data-to-policy workflow material.

## Safe Public Summary

The defensible public statement is:

```text
Private internal artifacts include selected promising radiology model-output
metrics and a successful formal-integrity build, but this repository does not
publish clinical validation, production readiness, regulatory compliance, or
SOTA claims. AOS is presented here as an explainable/verifiable control layer
around model outputs, not as a validated radiology product.
```

Machine-readable summary:
[`evidence/radiology_evidence_review.json`](../evidence/radiology_evidence_review.json).
