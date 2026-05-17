# Contributing

This repository is intentionally limited. Contributions, if accepted, must
preserve the public-demonstrator boundary and the proprietary rights reserved in
[LICENSE](LICENSE), [NOTICE](NOTICE), and [IP Protection Policy](docs/IP_PROTECTION.md).

## Contribution Status

External contributions are not accepted unless the maintainer has approved them
in advance and any required contributor agreement, copyright assignment, or
inbound license is complete in writing.

Unsolicited pull requests may be closed without review. Opening an issue,
comment, fork, clone, or pull request does not create an implied license to the
AOS Core, documentation, or commercial product direction.

By submitting material, you represent that you have the right to submit it and
that it does not contain confidential, employer-owned, customer-owned,
partner-owned, third-party, export-controlled, medical, regulated, or otherwise
controlled material unless written clearance has already been obtained.

## Do Not Submit

Do not submit:

- full AOS Core code
- production-system implementation material
- specialist-system material
- model weights or datasets
- DICOM, NIfTI, masks, labels, checkpoints, ONNX, TensorRT engines,
  safetensors, PT/PTH files, or model binaries
- generated claim bundles
- deployment secrets, local paths, internal logs, customer data, or partner data
- material that requires controlled disclosure review

Do not add claims that this public demonstrator is certified, clinically
validated, externally validated, sufficient for autonomous high-risk use, a
medical device, production ready, regulatory compliant, or SOTA.

## Required Checks

Run before submitting changes:

```bash
python -m ruff check .
python -m pytest tests -q
python benchmarks/run_benchmarks.py
python -m json.tool evidence/demonstrator_manifest.json
python -m json.tool evidence/radiology_offline_evaluation.json
python -m json.tool evidence/radiology_evidence_review.json
lake build AOSPublicCore
```

Use [Publication Safety Checklist](docs/PUBLICATION_CHECKLIST.md) for any
material change to documentation, evidence, claims, benchmark outputs, or public
positioning.
