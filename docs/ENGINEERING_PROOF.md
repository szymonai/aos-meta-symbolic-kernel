# Engineering Proof Surface

This document lists the public artifacts that can be executed, checked, and
falsified. It avoids product, clinical, regulatory, and commercial claims.

## Minimal Runtime

Canonical runtime:

```text
core/aos_public_core.py
```

Executable smoke:

```bash
python examples/minimal-runtime/minimal_runtime.py
```

Runtime contract:

| Input | Rule | Output |
| --- | --- | --- |
| `score + uncertainty <= limit - warn_margin` | inside safe band | `PASS` |
| `limit - warn_margin < score + uncertainty <= limit` | review band | `WARN` |
| `score + uncertainty > limit` | outside envelope | `BLOCK` |
| `metadata_complete == false` | incomplete input | `BLOCK` |

The runtime also emits replayable evidence and verifies that evidence from the
included input.

## Benchmark Commands

```bash
python benchmarks/run_benchmarks.py --check
python benchmarks/run_llm_assurance_benchmark.py --check
python benchmarks/run_llm_hard_case_benchmark.py --check
python benchmarks/run_operational_control_replay.py --check
python tools/verify_public_integrity.py
lake build AOSPublicCore
```

Current committed benchmark surfaces:

| Surface | Scale | Primary check |
| --- | ---: | --- |
| Synthetic policy benchmark | 12 scenarios | policy conformance and replay |
| LLM/agent smoke benchmark | 20 fixed outputs | unsafe pass-through on fixed cases |
| Synthetic hard-case benchmark | 540 fixed outputs | D1-D9 difficulty coverage |
| Operational control replay | 362,774 records | public offline replay and audit coverage |

The operational replay is the strongest public engineering artifact because it
uses frozen public operational traces, fixed policy, deterministic signal
extraction, audit records, replay checks, and explicit failure conditions.

## Concrete Application Cases

Executable profile cases:

```bash
python examples/application-profiles/run_profiles.py --check
```

Case file:

```text
examples/application-profiles/profile_cases.json
```

Included application surfaces:

| Surface | Example signal | Expected behavior |
| --- | --- | --- |
| Agent tool-call gate | unsafe tool action risk | `BLOCK` |
| RAG answer review | weak source coverage risk | `WARN` |
| Document extraction | complete low-risk extraction | `PASS` |
| Industrial sensor review | drift plus uncertainty | `BLOCK` |
| Financial workflow review | elevated risk band | `WARN` |
| Quantum job gate | backend calibration risk band | `WARN` |
| Metadata gate | incomplete required metadata | `BLOCK` |

These are not deployments. They are concrete input-to-verdict checks that show
how the same minimal runtime is applied across domains.

## Production Hardening Gates

These gates are not part of the current public proof surface. They are the
minimum engineering layers required before stronger production claims.

| Gate | Current public status | Required artifact |
| --- | --- | --- |
| Real online deployment | not included | live or shadow service run with traffic, SLOs, incident handling, and replayed logs |
| Stateful multi-agent governance | not included | state machine, tool/session identity, policy conflict handling, and replayable agent traces |
| Adversarial replay attacks | not established | anti-replay model, tamper tests, nonce or timestamp policy, and malicious replay suite |
| Trusted uncertainty extraction | not established | calibrated extractor, provenance checks, drift tests, and independent extraction audit |
| Policy DSL | not included | versioned grammar, parser, semantics, fixtures, and migration tests |
| Signed audit attestations | not included | signing format, key-management boundary, verifier, rotation policy, and negative tests |
| Formal runtime correspondence proof | not included | Python-to-Lean or spec-to-runtime refinement proof covering parser and verdict behavior |

Until those artifacts exist, the public claim remains bounded to deterministic
runtime behavior, executable examples, replay checks, benchmark regression, and
the abstract Lean verdict surface.

## Hard Failure Conditions

The public engineering claim fails if:

- benchmark `--check` commands drift from committed artifacts;
- runtime evidence replay fails;
- critical artifacts are not tracked by Git;
- `.gitignore` hides a required public artifact;
- Lean proof placeholders appear in `lakefile.lean` or `lean/`;
- local Markdown links break;
- public claim flags change to production, regulated-use, or external
  validation claims.
