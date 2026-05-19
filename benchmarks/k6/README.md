# k6 Smoke Benchmark

This is a synthetic smoke benchmark for the public API-shaped demo gate. It is
intended to check basic request handling and response shape under a small,
repeatable load.

It is not production latency, throughput, scalability, or availability evidence.

## Run

Start the demo API:

```bash
python examples/api-gate/aos_api_gate.py serve
```

In another terminal:

```bash
k6 run benchmarks/k6/aos_api_smoke.js
```

Optional target:

```bash
AOS_API_URL=http://127.0.0.1:8080 k6 run benchmarks/k6/aos_api_smoke.js
```

The script uses only synthetic payloads and does not require credentials.
