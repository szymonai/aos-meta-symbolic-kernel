# Operational Control Replay

This profile defines a production-relevant public evidence path for AOS without
using clinical data, live users, LLM outputs, or agent trajectories.

It evaluates AOS in offline shadow mode:

```text
public frozen operational trace
  -> deterministic signal extraction
  -> AOS PASS / WARN / BLOCK
  -> known anomaly window
  -> audit replay and aggregate metrics
```

## Current Dataset

The current local implementation uses the Numenta Anomaly Benchmark (NAB):

- repository: `https://github.com/numenta/NAB`
- local default path: `data/external/NAB`
- license: MIT
- committed data: none

Raw dataset files remain outside the public repository. The repository may
publish derived metrics, hashes, runner code, and summaries.

## What This Measures

- whether anomaly-window records pass silently;
- whether anomaly-window records route to review or block;
- false blocks on nominal records;
- nominal intervention load;
- deterministic audit evidence coverage;
- replay success for AOS evidence packets.

## Proof Profile

The committed metrics include explicit proof profiles:

- `production_relevance_profile`: why the run is production-relevant while not
  being a production deployment proof;
- `scalability_profile`: evaluated record scale and algorithmic shape;
- `auditability_profile`: source hashes, decision-stream hashes, audit coverage,
  and replay expectations;
- `falsification_profile`: concrete conditions that invalidate the public claim.

The intended public claim is:

> AOS demonstrates production-relevant control behavior in offline replay over
> public operational traces, with deterministic audit evidence and explicit
> falsification criteria.

This claim is narrower than production readiness.

## What This Does Not Prove

- production deployment readiness;
- service-level agreement;
- regulated-use safety;
- domain-specific safety approval;
- that AOS is an anomaly detector;
- external validation;
- universal AOS effectiveness.

## Public Claim Boundary

Safe wording:

> AOS was evaluated in offline shadow-mode replay over frozen public operational
> traces, measuring silent anomaly pass-through, intervention load, audit
> coverage, and deterministic replay.

Also safe:

> AOS demonstrates production-relevant control behavior in offline replay over
> public operational traces.

Avoid:

> This benchmark proves production readiness.

Avoid:

> This benchmark ranks anomaly-detection models.

## Commands

Download the public dataset locally:

```bash
git clone --depth 1 https://github.com/numenta/NAB.git data/external/NAB
```

Run the replay:

```bash
python benchmarks/run_operational_control_replay.py
```

Check committed artifacts:

```bash
python benchmarks/run_operational_control_replay.py --check
```

If the local dataset is unavailable, `--check` validates the committed metrics
schema and claim boundary only. Full regeneration requires local NAB data.
