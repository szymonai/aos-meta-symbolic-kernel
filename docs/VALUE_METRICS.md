# Value Metrics

This document reports only public, reproducible value metrics from the limited
demonstrator. It does not report production-system metrics, customer
outcomes, production service levels, clinical utility, regulated performance, or
commercial validation.

## Current Public Dataset

Source: `benchmarks/results/metrics.json`

| Metric | Current value |
| --- | ---: |
| Schema version | `synthetic-advantage/v1` |
| Synthetic scenarios | 12 |
| Safe scenarios | 4 |
| Warning scenarios | 4 |
| Unsafe scenarios | 4 |

The scenario set is synthetic. It is useful for reproducible public inspection,
not for domain validation.

## Current AOS Demonstrator Results

Source: `benchmarks/results/metrics.json`

| Metric | Current value |
| --- | ---: |
| Adapter | `aos_gate_adapter` |
| False passes on synthetic unsafe cases | 0 |
| False blocks on synthetic safe cases | 0 |
| PASS decisions | 4 |
| WARN decisions | 4 |
| BLOCK decisions | 4 |
| Decisions with audit digest | 12 |
| Deterministic replay | `true` |

These values mean that the current public gate produces one auditable decision
per public scenario and replays deterministically on the included synthetic
benchmark set.

## Public Boundary Metrics

Sources: `evidence/demonstrator_manifest.json` and
`benchmarks/results/metrics.json`

| Boundary field | Current value |
| --- | --- |
| Production-system code included | `false` |
| Internal policy logic included | `false` |
| Real clinical thresholds included | `false` |
| Specialist validation materials included | `false` |
| Data redistributed in repository | `false` |
| Clinical claim | `false` |
| Clinical validation claim | `false` |
| External validation completed | `false` |
| Medical-device claim | `false` |
| Regulatory compliance claim | `false` |
| Production runtime claim | `false` |
| Benchmark production-ready claim | `false` |
| Benchmark external-validation claim | `false` |
| Benchmark domain-validation claim | `false` |
| Python-Lean refinement claim | `false` |

These fields are value metrics because they make the public repository easier to
review: the demonstrator exposes a bounded control pattern while explicitly
separating public evidence from production-system material.

## Clean-Room Repeatability

Source: `docs/CLEAN_ROOM_TEST.md`

The clean-room test is the public repeatability check. A reviewer should be able
to clone the repository, install development requirements, run linting and
tests, rebuild the benchmark metrics, parse the evidence JSON files, and build
the public Lean target using only the repository contents.

## Not Claimed

The public metrics above do not establish:

- production readiness
- clinical safety or clinical utility
- medical-device status
- regulatory compliance
- external validation
- customer ROI
- revenue performance
- best-in-class or state-of-the-art status
- access to production-system material

Any future public value claim should identify the exact evidence source, the
dataset or workflow boundary, the current numeric result, and the claims that
remain out of scope.
