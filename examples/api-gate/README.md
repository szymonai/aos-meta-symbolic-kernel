# AOS API Gate

Minimal public API-shaped example for a replayable AOS control decision.

The example evaluates a bounded workflow signal against an explicit public
policy and returns:

```text
PASS / WARN / BLOCK + reason + SHA-256-linked audit evidence
```

Run from this directory:

```bash
python aos_api_gate.py evaluate --input sample_input.json
python aos_api_gate.py replay --evidence sample_evidence.json
python aos_api_gate.py serve --host 127.0.0.1 --port 8080
```

HTTP endpoints:

```text
GET  /health
POST /v1/evaluate
POST /v1/replay
```

This is a compact integration-shape example for the public demonstrator. It is
not a production SDK, regulated product, or deployment package.
