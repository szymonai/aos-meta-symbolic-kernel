# Publication Safety Checklist

Use this checklist before publishing a commit, release, article, demo, pitch
deck excerpt, benchmark result, or evidence packet derived from AOS material.

## Repository Boundary

- [ ] The change belongs in the public demonstrator, not the private AOS Core.
- [ ] No private source, specialist-system code, private proofs, calibration
      paths, policy internals, adapter protocols, thresholds, or validation stack
      details are included.
- [ ] No local paths, credentials, tokens, private logs, customer data, partner
      data, or deployment details are included.
- [ ] No DICOM, NIfTI, masks, labels, scans, checkpoints, weights, ONNX,
      TensorRT engines, safetensors, PT/PTH files, or other model artifacts are
      included.

## Claims

- [ ] No clinical validation claim.
- [ ] No medical-device claim.
- [ ] No MDR, AI Act, CE, ISO, FDA, or other regulatory-compliance claim.
- [ ] No production-readiness claim.
- [ ] No SOTA or external-validation claim unless independently supported and
      explicitly approved.
- [ ] No claim that AOS proves model correctness, eliminates hallucinations, or
      performs autonomous operational control.

## IP Review

- [ ] Copyright notice and proprietary demonstrator boundary remain intact.
- [ ] No third-party material is added without written permission and provenance.
- [ ] No employer-owned, contractor-owned, customer-owned, or partner-owned
      material is added without written clearance.
- [ ] Patent-sensitive implementation detail has either been withheld or cleared
      in writing before disclosure.
- [ ] Trademark-sensitive names or slogans have been checked before publication.
- [ ] External contributions, if any, have a written contributor agreement,
      assignment, or inbound license approved by the maintainer.

## Verification

- [ ] `python -m ruff check .`
- [ ] `python -m pytest tests -q`
- [ ] `python benchmarks/run_benchmarks.py`
- [ ] `python -m json.tool evidence/demonstrator_manifest.json`
- [ ] `python -m json.tool evidence/radiology_offline_evaluation.json`
- [ ] `python -m json.tool evidence/radiology_evidence_review.json`
- [ ] `lake build AOSPublicCore`
- [ ] Text scan for forbidden local paths, secrets, case IDs, model artifacts,
      and overbroad claims.

## Approval Record

Record the following in the PR or release note:

- approving maintainer;
- date;
- commit SHA;
- validation commands run;
- files intentionally withheld;
- patent/trademark review status, if applicable.
