# AOS Public Abstraction Map

AOS is built as a layered assurance system. This public repository exposes the
smallest useful slice of that architecture: enough to show the control pattern
while staying within the approved public demonstrator boundary.

## Public Layer Stack

| Layer | Public object | Purpose |
| --- | --- | --- |
| L0 | Source output or operational trace | Raw material outside the AOS verdict contract |
| L1 | Signal extraction / normalization adapter | Converts source material into a bounded public signal |
| L2 | Bounded input signal | Minimal input for the public control example |
| L3 | Interval gate | Deterministic PASS/WARN/BLOCK verdict |
| L4 | Demo audit digest | Reproducible evidence that a demo decision was made |
| L5 | Benchmarks and replay profiles | Bounded behavioral and empirical control checks |
| L6 | Lean verdict logic | Abstract proof surface for verdict invariants |
| L7 | Runtime substrate boundary | Separates AOS semantics from Python/native/GPU execution choices |
| L8 | Evidence summaries and public boundary docs | Aggregate evidence inventory and claim discipline |

## Core Control Shape

```text
source output, metadata, or operational trace
  -> deterministic signal extraction / normalization
  -> bounded uncertainty / quality / risk signal
  -> deterministic control envelope
  -> PASS / WARN / BLOCK
  -> audit evidence
  -> human review, escalation, or workflow hold
```

The public implementation demonstrates this shape with a single interval gate:

```text
upper_bound = value + uncertainty

upper_bound > limit                 -> BLOCK
upper_bound > limit - warn_margin   -> WARN
otherwise                           -> PASS
```

This simplification is intentional. It preserves the public assurance idea while
staying within the approved disclosure boundary.

Implementation substrates sit below this contract. Python, Rust, C++, CUDA,
PTX, assembly, WASM, or eBPF are not alternative AOS semantics; they are possible
ways to execute or observe the same contract if separately implemented and
tested.

## What The Public Repo Demonstrates

The public repo can demonstrate that:

- the demonstrator gate is deterministic;
- synthetic unsafe interval-crossing cases are blocked by the AOS adapter;
- demo audit digests are reproducible and tamper-sensitive;
- operational replay measures control behavior after deterministic signal
  extraction from public frozen traces;
- the Lean file verifies selected abstract verdict invariants for the
  simplified model;
- public evidence files preserve explicit claim boundaries.

## What The Public Repo Does Not Prove

The public repo does not prove:

- model correctness;
- signal-extractor optimality;
- production threshold calibration;
- Python-to-Lean refinement;
- production audit security;
- domain validity;
- regulatory compliance;
- external performance ranking;
- autonomous operational control;
- safety of any specialist profile.

## Information-Dense Reading Path

For a fast technical review, read in this order:

1. `README.md` for project claim and public boundary.
2. `docs/architecture.md` for the public control architecture.
3. `docs/RUNTIME_SUBSTRATES.md` for the implementation substrate boundary.
4. `core/aos_public_core.py` for the executable control primitive.
5. `benchmarks/results/summary.md` for the synthetic comparison.
6. `benchmarks/results/operational_control_replay_summary.md` for the
   operational replay profile.
7. `lean/AOSPublicCore.lean` for the proof surface.
8. `evidence/demonstrator_manifest.json` for machine-readable claim limits.
