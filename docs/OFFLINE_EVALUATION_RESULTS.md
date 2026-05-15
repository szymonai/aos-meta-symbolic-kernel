# Offline Evaluation Results

This document summarizes local aggregate artifacts that were available during
repository preparation. These are offline evidence records only. They are not
external validation, clinical validation, production-readiness evidence, or a
medical-device claim.

The repository intentionally publishes only aggregate values. It does not
redistribute patient data, images, masks, DICOM/NIfTI files, checkpoints,
per-case records, local paths, private thresholds, or private audit logs.

## Available Aggregate Evidence

| Evidence item | Sample count | Split | Confirmed metrics | Missing metrics |
| --- | ---: | --- | --- | --- |
| BraTS 2024 Adult Glioma aggregate | 10 | not available in current evidence | Dice mean 0.1136, Dice std 0.0693, Dice median 0.1268, HD95 mean 47.85 mm, HD95 max 62.41 mm | sensitivity/recall, specificity, precision, FNR/FPR, calibration/uncertainty, baselines |
| TCGA_LGG-labeled local BraTS pipeline aggregate | 88 | all | Model A/B Dice mean 0.1277/0.1457, recall mean 0.3189/0.4493, precision mean 0.1202/0.0998, HD95 mean 66.9153/67.9033 | specificity, FNR/FPR, calibration/uncertainty, named baselines |
| Yale Brain Mets aggregate | 100 | not available in current evidence | Dice mean 0.9279, HD95 mean 3.011 mm, total false alarms 7 | sensitivity/recall, specificity, precision, FNR/FPR, calibration/uncertainty, baselines |

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
