# Contributing

This repository is intentionally limited. Contributions, if accepted, must
preserve the public-demonstrator boundary.

Do not submit:

- full AOS Core code
- full audit contract or schema
- policy semantics
- adapter protocol
- validation stack
- specialist-system code
- model weights or datasets
- thresholds or calibration values
- private proof artifacts
- optimization code or benchmarks
- deployment secrets or private logs

Do not add claims that this public demonstrator is certified, clinically
validated, externally validated, sufficient for autonomous high-risk use, or a
medical device.

Run before submitting changes:

```bash
python -m ruff check .
python -m pytest tests -q
lake build AOSPublicCore
```
