# Offline Evaluation Results

This document summarizes local aggregate artifacts that were available during
repository preparation. These are offline evidence records only. They are not
external validation, clinical validation, production-readiness evidence, or a
medical-device claim.

The repository intentionally publishes only aggregate values. It does not
redistribute patient data, images, masks, DICOM/NIfTI files, checkpoints,
per-case records, local paths, private thresholds, or private audit logs.

## Current Public Evidence Status

The current public repository does not publish radiology performance numbers as
active results. Earlier local aggregates found during preparation are treated as
historical, superseded artifacts and are not used as current performance
evidence.

| Evidence item | Current public status | Reason |
| --- | --- | --- |
| BraTS 2025 current results | not available in current public evidence | A clean aggregate artifact with dataset provenance, split, sample count, metrics, calibration method, baselines, and reproducibility metadata is not present in this public repo |
| Older BraTS/TCGA_LGG/Yale aggregate artifacts | historical/superseded, not current result claims | Newer internal runs may exist; publishing stale numbers would misrepresent the current system |
| Calibration and uncertainty evidence | high-level capability only | Private calibration curves, thresholds, and policy logic are not public |
| Optimization and runtime evidence | high-level capability only | Private benchmark traces and low-level implementation details are not public |

## Required Evidence Before Publishing Updated Metrics

Updated radiology metrics should be published only when an aggregate-only
evidence packet is available with:

- dataset name and version
- source and access date
- usage terms or license status
- train/validation/test or external split definition
- sample count
- Dice, sensitivity/recall, specificity, precision, FNR/FPR, HD95
- calibration or uncertainty method
- baseline definition
- run date and reproducibility metadata
- explicit flags that no clinical, medical-device, compliance, CE, or
  production-readiness claim is being made

## Interpretation Boundary

These numbers are useful for showing that local offline evaluation artifacts
exist and that AOS can be discussed as a control layer around model outputs.
They do not establish clinical validity or generalization. They also do not
prove that AOS improves the underlying model.

The correct interpretation is:

```text
model output quality metric != AOS control decision
AOS control decision != human radiology decision
human radiology decision != public clinical claim
```

See the machine-readable summary in
[`evidence/radiology_offline_evaluation.json`](../evidence/radiology_offline_evaluation.json).
