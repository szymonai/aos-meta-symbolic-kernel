# Publication Safety Checklist

Use this checklist before publishing a commit, release, article, demo, pitch
deck excerpt, benchmark result, or evidence packet derived from AOS material.

## Repository Boundary

- [ ] The change belongs in the public demonstrator, not the private AOSKernel.
- [ ] No private source, specialist-system material, restricted evidence,
      reserved technical material, or non-public implementation detail are
      included.
- [ ] No local paths, credentials, tokens, private logs, customer data, partner
      data, or deployment details are included.
- [ ] No DICOM, NIfTI, masks, labels, scans, checkpoints, weights, ONNX,
      TensorRT engines, safetensors, PT/PTH files, or other model artifacts are
      included.
- [ ] Specialized terminology is used only when it is necessary, bounded by
      evidence, and cleared for publication.

## Claims

- [ ] No clinical validation claim.
- [ ] No medical-device claim.
- [ ] No MDR, AI Act, CE, ISO, FDA, or other regulatory-compliance claim.
- [ ] No production-readiness claim.
- [ ] No SOTA or external-validation claim unless independently supported and
      explicitly approved.
- [ ] No named competitive scorecard or direct competitive comparison is added.
- [ ] No claim that AOS proves model correctness, eliminates hallucinations, or
      performs autonomous operational control.

## IP Review

- [ ] Copyright notice and proprietary demonstrator boundary remain intact.
- [ ] No third-party material is added without written permission and provenance.
- [ ] No employer-owned, contractor-owned, customer-owned, or partner-owned
      material is added without written clearance.
- [ ] Review-required technical material has either been withheld or cleared in
      writing before disclosure.
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
      disclosure-sensitive material, and overbroad claims.
- [ ] Public evidence packet anchors, when published, include SHA-256 for quick
      verification, SHA-512 for audit-grade verification, and Ed25519 signature
      metadata for authenticity and provenance.

## Approval Record

Record the following in the PR or release note:

- approving maintainer;
- date;
- commit SHA;
- validation commands run;
- files intentionally withheld;
- patent/trademark review status, if applicable.
