# Public Surfaces

This repository can be presented through a small set of external surfaces
without expanding the public technical boundary.

## Selected Surfaces

| Surface | Repository artifact | Public role |
| --- | --- | --- |
| Documentation site | `docs.json` | Mintlify-compatible navigation for public docs |
| Interactive sandbox | `examples/gradio-sandbox/` | Synthetic `PASS` / `WARN` / `BLOCK` demo |
| Code-quality gate | `sonar-project.properties` | Optional SonarQube Cloud project configuration |
| Load smoke test | `benchmarks/k6/` | Synthetic API smoke benchmark for the demo gate |
| Integrity check | `tools/verify_public_integrity.py` | Local consistency check for selected public artifacts |

## Boundary

These artifacts are public demonstrator surfaces. They do not publish
restricted implementation material, datasets, workflow material, production
telemetry, deployment credentials, or persistence backends.

The k6 script is a smoke benchmark for the public API-shaped demo only. It is
not production latency, scalability, availability, or capacity evidence.

The Gradio sandbox is a synthetic interface around public demo logic. It is not
a hosted product, domain validator, regulated workflow, or production SDK.

SonarQube Cloud setup should be completed outside the repository. Service
credentials must not be committed.
