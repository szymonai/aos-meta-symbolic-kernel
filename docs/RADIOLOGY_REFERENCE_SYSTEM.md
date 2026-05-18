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
workflow. It does not publish the full specialist system, adapters,
clinical workflow, controlled technical artifacts, data, masks, or model
weights.

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
patient records, checkpoints, controlled technical artifacts, or workflow
material.

## Current Metrics Boundary

This public repository does not publish current radiology performance metrics.
Radiology is retained as a reference profile for explaining the control pattern,
not as a domain-performance result.

Updated domain results should be published only after a clean aggregate evidence
packet is available. The packet must include dataset provenance, split
definition, sample count, baseline definition, reproducibility metadata, and
explicit non-claim flags.

This avoids presenting historical, partial, or superseded metrics as the current
system state.

See [Radiology evidence review](RADIOLOGY_EVIDENCE_REVIEW.md).

## Specialist System Interpretation

A specialist radiology profile would be one possible product family built on a
production system. The public demonstrator only shows the shape of the control
contract:

- model output is not treated as a final decision
- uncertainty or quality metadata is evaluated before workflow use
- AOS emits a control verdict
- audit evidence records the control event
- human review or escalation remains outside AOS

This is utility evidence for the architecture, not a clinical proof.

See [Application Profiles](APPLICATION_PROFILES.md) for the broader context:
radiology is one reference profile within a domain-neutral assurance pattern.
