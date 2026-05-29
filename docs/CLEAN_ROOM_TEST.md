# Clean-Room Test

This test verifies only the limited public demonstrator. It is designed for a
fresh public checkout using only the repository contents.

## Commands

```bash
python -m pip install -e .[dev]
python -m ruff check .
python -m pytest tests -q
python tools/verify_public_integrity.py
python benchmarks/run_benchmarks.py --check
python benchmarks/run_llm_assurance_benchmark.py --check
python benchmarks/run_llm_hard_case_benchmark.py --check
python benchmarks/run_operational_control_replay.py --check
python -m json.tool benchmarks/results/metrics.json
python -m json.tool benchmarks/results/operational_control_replay_metrics.json
python -m json.tool evidence/demonstrator_manifest.json
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
| Operational replay series | 58 |
| Operational replay evaluated records | 362,774 |
| Operational replay anomaly windows | 116 |
| Operational replay AOS window review/block rate | 96.55% |
| Operational replay AOS audit/replay | 100% / 100% |

The hello-world Docker Compose check is a container smoke test for the public
demonstrator example. It is not a production deployment claim.

The API-gate replay check verifies that the public sample evidence packet can be
rebuilt from its included input and compared deterministically.

The demonstrator manifest is also expected to keep public boundary fields set to
`false` for claims outside this limited demonstrator, including external
validation, regulated use, safety approval, and production runtime claims.

The operational replay check validates committed public artifacts. If the
external NAB dataset is available locally under `data/external/NAB`, it also
regenerates the replay outputs and detects drift. The dataset itself is not
required in a clean public checkout.

## Scope Boundary

This test does not test specialist systems, datasets, delivery materials,
production security, deployment settings, or deployment outcomes.
