# Technical Advantage Evidence

This document describes the technical advantage demonstrated by the public AOS
limited demonstrator. It does not describe the private AOS Core, production
policy semantics, specialist adapters, private proof stack, or NDA materials.

## Technical Thesis

AOS is demonstrated here as a small deterministic runtime assurance pattern:

```text
model output + uncertainty -> deterministic gate -> PASS / WARN / BLOCK
                                  -> audit evidence
                                  -> abstract formal invariants
```

The advantage over simple guardrails is not that the public demonstrator is a
production system. The advantage is the combined control pattern:

- a deterministic runtime gate that evaluates uncertainty before use
- audit evidence attached to each demo decision
- formal invariants over the abstract verdict logic

## Demonstrator Evidence Scope

The public evidence layer covers only synthetic scenarios. It compares the AOS
demo gate against simple baselines:

- a threshold-only `if/else` guard
- a JSON-shape guard
- a deterministic text heuristic that simulates prompt-only guardrails

The benchmark records false passes, false blocks, verdict counts, audit-record
presence, and deterministic replay.

## Explicit Limits

This repository still does not prove:

- Python-to-Lean refinement
- equivalence between Python runtime behavior and Lean logic
- production HMAC/audit-envelope security
- domain validation
- external validation
- suitability for regulated or safety-critical deployment
- correctness of an upstream AI model

The Lean proof surface covers abstract verdict ordering and interval logic only.

## Comparison

| Approach | What It Checks | Handles Uncertainty | Audit Evidence | Formal Invariants | Expected Weakness |
| --- | --- | --- | --- | --- | --- |
| Plain `if/else` threshold | `value <= limit` | No | No | No | Can pass unsafe cases when uncertainty crosses the limit |
| JSON schema validation | Shape and basic types | No | No | No | Valid structure can still contain unsafe values |
| Prompt-only guardrail | Text cues or policy wording | No deterministic numeric bound | No | No | Can miss unsafe cases when wording is benign or indirect |
| AOS public demo gate | `value + uncertainty` against the limit and warning band | Yes | Demo HMAC digest | Abstract Lean verdict invariants | Public demo only; not the private production core |

## Reading The Results

See:

- [Benchmark summary](../benchmarks/results/summary.md)
- [Benchmark metrics JSON](../benchmarks/results/metrics.json)
- [Lean proof surface](../lean/AOSPublicCore.lean)
