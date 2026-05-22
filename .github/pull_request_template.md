## Summary

-

## Publication Boundary

- [ ] This change stays within the limited public demonstrator boundary.
- [ ] No controlled technical, evidence, specialist-system, deployment, or
      delivery material is included.
- [ ] No controlled datasets, labels, checkpoints, weights,
      ONNX/TensorRT/safetensors/PT/PTH artifacts, secrets, local paths,
      controlled data, or internal logs are included.

## Claims

- [ ] This change does not add domain-validation, regulatory-compliance,
      production-readiness, external-ranking, external-validation, or
      autonomous-control claims.

## IP And Contribution

- [ ] I have authority to submit this material.
- [ ] This submission does not include employer-owned, third-party,
      confidential, export-controlled, or regulated
      material without written clearance.
- [ ] If I am not the maintainer, I understand that contributions are accepted
      only after prior maintainer approval and any required written contributor
      agreement, copyright assignment, or inbound license.

## Validation

- [ ] `python -m ruff check .`
- [ ] `python -m pytest tests -q`
- [ ] `python benchmarks/run_benchmarks.py --check`
- [ ] `lake build AOSPublicCore`
