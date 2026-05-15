# Radiology Reference System

This document describes a reference scenario for AI-assisted brain tumor
radiology triage. It is included to make the AOS control-layer pattern easier to
understand in a concrete domain.

Radiology is referenced only as a domain-adapter example. It is not a product in
this public repository and is not a medical-device or clinical-validation claim.

The specialist radiology system may be described as an example specialist
system built on the AOS control-layer pattern. In this public repository, that
description is limited to utility evidence: it shows how AOS can organize model
outputs, uncertainty, audit evidence, and human escalation in a domain-specific
workflow. It does not publish the full specialist system, private adapters,
clinical workflow, thresholds, calibration logic, data, masks, or model weights.

## Control Flow

```text
model output
  -> uncertainty or quality metadata
  -> AOS PASS/WARN/BLOCK decision
  -> audit evidence
  -> human review, escalation, or workflow hold
```

## Separation Of Decisions

| Layer | Meaning | Public demonstrator claim |
| --- | --- | --- |
| Model output | Numeric or segmentation-related output produced by a model | Not proven correct |
| AOS decision | Deterministic control decision over output metadata | Demonstrated with simplified public gate |
| Human decision | Radiologist, operator, or workflow-owner judgment | Outside this repository |
| Clinical claim | Claim about diagnosis, treatment, or clinical validity | Not claimed |

## Intended Reference Use

The reference scenario is triage support, not autonomous diagnosis:

- `PASS`: output metadata is inside the public demo envelope
- `WARN`: output should be reviewed or escalated
- `BLOCK`: output should not be used without further review

The public repo does not include a radiology model, DICOM/NIfTI data, masks,
patient records, checkpoints, clinical thresholds, calibration logic, or private
workflow policy.

## Current Metrics Boundary

This public repository includes a sanitized evidence review for selected
private artifacts. The review separates a small fold validation summary, an
internal cohort report, and private formal-integrity status. Those items are
evidence inventory, not clinical validation or product evidence.

Updated internal results, including any BraTS 2025 runs, should be published
only after a clean aggregate evidence packet is available. The packet must
include dataset provenance, split definition, sample count, calibration method,
baseline definition, reproducibility metadata, and explicit non-claim flags.

This avoids presenting historical, partial, or superseded metrics as the
current system state.

See [Radiology evidence review](RADIOLOGY_EVIDENCE_REVIEW.md).

## Specialist System Interpretation

A specialist radiology profile would be one possible product family built on a
private AOS Core. The public demonstrator only shows the shape of the control
contract:

- model output is not treated as a final decision
- uncertainty or quality metadata is evaluated before workflow use
- AOS emits a control verdict
- audit evidence records the control event
- human review or escalation remains outside AOS

This is a proof-of-utility framing for the architecture, not a clinical proof.
