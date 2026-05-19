# Offline Evaluation Results

This document defines the public boundary for offline evaluation material.

The repository does not publish current domain-performance metrics. It only
states that future metrics must be released through a clean aggregate evidence
packet with provenance, split definition, sample count, baseline definition,
reproducibility metadata, and explicit non-claim flags.

## Current Public Evidence Status

| Evidence area | Public status |
| --- | --- |
| Synthetic AOS benchmark | public and reproducible |
| Public Lean proof surface | public and bounded |
| Radiology performance metrics | not published as current public evidence |
| Patient data, images, masks, model weights, checkpoints | not included |
| Clinical validation, regulatory approval, production readiness | not claimed |

## Required Evidence Before Domain Metrics

Updated domain metrics should be published only when an aggregate-only evidence
packet is available with:

- dataset name and version;
- source and access date;
- terms or license status;
- train/validation/test or external split definition;
- sample count;
- metric definitions;
- baseline definition;
- run date and reproducibility metadata;
- explicit flags that no clinical, medical-device, compliance, certification,
  or production-readiness claim is being made.

## Interpretation Boundary

The correct interpretation is:

```text
model output quality metric != AOS control decision
AOS control decision != human domain decision
human domain decision != public clinical or regulatory claim
```

See the machine-readable summaries:

- [`evidence/radiology_offline_evaluation.json`](../evidence/radiology_offline_evaluation.json)
- [`evidence/radiology_evidence_review.json`](../evidence/radiology_evidence_review.json)
