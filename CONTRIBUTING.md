# Contributing

This repository is intentionally limited. Contributions, if accepted, must
preserve the public-demonstrator boundary and the proprietary rights reserved in
[LICENSE](LICENSE) and [NOTICE](NOTICE).

## Contribution Status

External contributions are not accepted unless the maintainer has approved them
in advance and any required contributor agreement, copyright assignment, or
inbound license is complete in writing.

Unsolicited pull requests may be closed without review. Opening an issue,
comment, fork, clone, or pull request does not create an implied license to the
AOS Core, documentation, or product direction.

By submitting material, you represent that you have the right to submit it and
that it does not contain confidential, employer-owned, third-party,
export-controlled, regulated, or otherwise
controlled material unless written clearance has already been obtained.

## Do Not Submit

Do not submit:

- full AOS Core code
- production-system implementation material
- specialist-system material
- model weights, datasets, labels, checkpoints, ONNX/TensorRT engines,
  safetensors, PT/PTH files, or model binaries
- generated claim bundles
- deployment secrets, local paths, internal logs, or controlled data
- material that requires controlled disclosure review

Do not add claims that this public demonstrator is approved, externally
validated, sufficient for autonomous high-risk use, production deployment-ready,
regulatory compliant, or externally ranked.

## Required Checks

Run before submitting changes:

```bash
python -m ruff check .
python -m pytest tests -q
python tools/verify_public_integrity.py
python benchmarks/run_benchmarks.py --check
python benchmarks/run_llm_assurance_benchmark.py --check
python benchmarks/run_llm_hard_case_benchmark.py --check
python benchmarks/run_operational_control_replay.py --check
python -m json.tool evidence/demonstrator_manifest.json
lake build AOSPublicCore
```

Keep documentation, evidence, claims, benchmark outputs, and public positioning
within the demonstrator boundary.
