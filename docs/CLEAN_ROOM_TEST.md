# Clean-Room Test

This test verifies only the limited public demonstrator.

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest tests -q
lake build AOSPublicCore
python -m json.tool evidence/demonstrator_manifest.json
```

It does not test the private AOS Core, specialist systems, restricted evidence
packages, non-public implementation material, datasets, or commercial delivery
materials.
