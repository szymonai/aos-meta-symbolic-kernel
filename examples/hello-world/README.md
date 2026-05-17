# AOS Hello World

Minimal public example of an AOS-style control decision.

Scenario:

```text
model proposes: 10 / x
input: x = 0
AOS verdict: BLOCK
reason: denominator must be non-zero
audit_id: sha256:...
```

Run:

```bash
docker-compose up
```

This example is intentionally small. It demonstrates public verdict structure
and audit evidence only.
