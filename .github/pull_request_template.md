## Summary

-

## Publication Boundary

- [ ] This change stays within the limited public demonstrator boundary.
- [ ] No full AOS Core, non-public implementation material, restricted evidence,
      specialist-system material, private evaluation results, or commercial delivery
      material is included.
- [ ] No medical data, DICOM/NIfTI files, masks, labels, checkpoints, weights,
      ONNX/TensorRT/safetensors/PT/PTH artifacts, secrets, local paths, customer
      data, or private logs are included.

## Claims

- [ ] This change does not add clinical-validation, medical-device,
      regulatory-compliance, production-readiness, SOTA, external-validation, or
      autonomous-control claims.

## IP And Contribution

- [ ] I have authority to submit this material.
- [ ] This submission does not include employer-owned, customer-owned,
      partner-owned, third-party, confidential, export-controlled, or regulated
      material without written clearance.
- [ ] If I am not the maintainer, I understand that contributions are accepted
      only after prior maintainer approval and any required written contributor
      agreement, copyright assignment, or inbound license.

## Validation

- [ ] `python -m ruff check .`
- [ ] `python -m pytest tests -q`
- [ ] `python benchmarks/run_benchmarks.py`
- [ ] `lake build AOSPublicCore`
