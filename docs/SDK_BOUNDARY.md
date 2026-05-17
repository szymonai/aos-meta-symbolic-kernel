# SDK Boundary

This repository is not a production SDK. It is a limited public demonstrator of
the AOS runtime assurance pattern.

## What The Public Repository Shows

The public repository shows the smallest useful integration shape:

```text
input signal -> AOS-style check -> PASS / WARN / BLOCK -> audit evidence
```

This is enough to understand the control pattern, run the demonstrator, inspect
synthetic metrics, and review the public proof surface.

## What A Future SDK Could Provide

A future commercial SDK could expose a stable integration surface for controlled
deployments, such as:

- verdict evaluation;
- audit evidence export;
- policy configuration through approved interfaces;
- workflow integration hooks;
- evidence packet generation;
- deployment-specific observability;
- enterprise governance integration.

Those are product-direction examples, not claims that this public repository is
already a production SDK.

## What Is Not Public

This repository does not publish:

- production API contracts;
- customer integration code;
- deployment settings;
- production security design;
- commercial support or service-level commitments.

## Public Rule

Use this repository to evaluate the public control-layer idea. Treat SDK,
enterprise deployment, customer integration, and production support as separate
commercial surfaces that require controlled disclosure and separate agreements.
