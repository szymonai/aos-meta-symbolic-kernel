# Clean-Room Test

This test verifies only the limited public demonstrator. It is designed for a
fresh public checkout using only the repository contents.

## Commands

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest tests -q
python benchmarks/run_benchmarks.py
python -m json.tool benchmarks/results/metrics.json
python -m json.tool evidence/demonstrator_manifest.json
python -m json.tool evidence/radiology_offline_evaluation.json
python -m json.tool evidence/radiology_evidence_review.json
python examples/hello-world/hello_world.py
python examples/api-gate/aos_api_gate.py evaluate --input examples/api-gate/sample_input.json
python examples/api-gate/aos_api_gate.py replay --evidence examples/api-gate/sample_evidence.json
docker compose -f examples/hello-world/docker-compose.yml config --quiet
docker compose -f examples/hello-world/docker-compose.yml run --rm hello-world
lake build AOSPublicCore
```

## Expected Public Results

The current public benchmark evidence is:

| Check | Current expected result |
| --- | --- |
| Synthetic scenarios | 12 |
| Scenario mix | 4 safe, 4 warning, 4 unsafe |
| Public AOS false passes | 0 |
| Public AOS false blocks | 0 |
| Public AOS PASS/WARN/BLOCK counts | 4 / 4 / 4 |
| Public AOS audit digests | 12 |
| Public AOS deterministic replay | `true` |

The hello-world Docker Compose check is a container smoke test for the public
demonstrator example. It is not a production deployment claim.

The API-gate replay check verifies that the public sample evidence packet can be
rebuilt from its included input and compared deterministically.

The demonstrator manifest is also expected to keep public boundary fields set to
`false` for claims outside this limited demonstrator, including clinical claims,
external validation, medical-device status, regulatory compliance, and
production runtime claims.

## Scope Boundary

This test does not test specialist systems, datasets, commercial delivery
materials, production security, deployment settings, or customer outcomes.
