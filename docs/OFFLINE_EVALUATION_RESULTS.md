# Offline Evaluation Results

This document summarizes local aggregate artifacts that were available during
repository preparation. These are offline evidence records only. They are not
external validation, clinical validation, production-readiness evidence, or a
medical-device claim.

The repository intentionally publishes only aggregate values. It does not
redistribute patient data, images, masks, DICOM/NIfTI files, checkpoints,
per-case records, local paths, restricted technical artifacts, or private audit
logs.

## Current Public Evidence Status

The current public repository includes a bounded radiology evidence review.
It separates small-fold validation metrics, an internal cohort report, and
private formal-integrity evidence. None of these are published as clinical
validation, compliance, production readiness, SOTA, or medical-device evidence.

The safe public milestone is the internal n=484 cohort Dice WT `0.8108`, with
Dice ET `0.8033` and ET recall `0.8065`. A separate Dataset832 fold artifact
shows label-2 Dice `0.8843` and label-2 recall `0.9085` on 2 validation cases;
it is not relabeled as cohort-level Whole Tumor performance.

| Evidence item | Current public status | Reason |
| --- | --- | --- |
| Dataset832/BraTS2024-labelled fold validation summary | selected internal artifact reviewed | Confirms label-2 Dice 0.8843, recall 0.9085, precision 0.8665 on 2 validation cases; this is not a cohort-level result and not BraTS 2025 evidence |
| Internal cohort report | selected internal artifact reviewed | Confirms n=484 report values: Dice WT 0.8108, Dice ET 0.8033, ET recall 0.8065, and 36 ET outliers; not external validation or compliance evidence |
| Private formal-integrity status | selected internal artifact reviewed | Confirms 3292/3292 Lean tasks and root build exit code 0; not Python-to-Lean refinement or clinical correctness evidence |
| BraTS 2025 current results | not available in current public evidence | A clean aggregate artifact with dataset provenance, split, sample count, metrics, baselines, and reproducibility metadata is not present in this public repo |
| Older BraTS/TCGA_LGG/Yale aggregate artifacts | historical/superseded, not current result claims | Newer internal runs may exist; publishing stale numbers would misrepresent the current system |
| Private evaluation evidence | not public | Restricted evidence packages and private performance traces are not public |

## Required Evidence Before Publishing Updated Metrics

Updated radiology metrics should be published only when an aggregate-only
evidence packet is available with:

- dataset name and version
- source and access date
- usage terms or license status
- train/validation/test or external split definition
- sample count
- Dice, sensitivity/recall, specificity, precision, FNR/FPR, HD95
- evaluation method summary
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
[`evidence/radiology_offline_evaluation.json`](../evidence/radiology_offline_evaluation.json)
and the evidence review in
[`evidence/radiology_evidence_review.json`](../evidence/radiology_evidence_review.json).
