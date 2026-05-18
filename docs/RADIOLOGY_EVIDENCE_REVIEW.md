# Radiology Evidence Review

Radiology is kept as a reference profile for explaining the AOS control pattern.
It is not a product in this public repository and is not a medical-device,
clinical-validation, regulatory-compliance, safety-certification, or
production-readiness claim.

## Public Status

The public repository does not publish current radiology performance metrics.
It also does not publish cohort reports, per-case records, model artifacts,
clinical workflow material, audit logs, or specialist implementation details.

The public role of this profile is limited to the control-layer shape:

```text
model output metadata
  -> uncertainty or quality signal
  -> AOS PASS / WARN / BLOCK verdict
  -> audit evidence
  -> human review, escalation, or workflow hold
```

## What Can Be Said

- Radiology is one possible reference profile for AOS.
- AOS can be described as a control layer around model-output metadata.
- Public examples may discuss separation between model output, AOS verdict,
  human decision, and clinical claim.
- Updated domain metrics require a separate clean aggregate evidence packet
  before publication.

## What Is Not Publicly Claimed

- clinical validation;
- diagnosis or treatment recommendation;
- medical-device status;
- regulatory approval or certification;
- production deployment readiness;
- current BraTS or radiology benchmark performance;
- broad comparative or state-of-the-art performance;
- production-grade signatures or audit manifests.

## Evidence Required Before Metrics Publication

Any future public metric should be supported by an aggregate evidence packet
with:

- dataset name, version, source, access date, and usage terms;
- split definition and sample count;
- metric definitions and baseline definitions;
- run date and reproducibility metadata;
- non-redistribution status for protected data;
- explicit flags that no clinical, regulatory, medical-device, or production
  claim is being made.

Machine-readable boundary:
[`evidence/radiology_evidence_review.json`](../evidence/radiology_evidence_review.json).
