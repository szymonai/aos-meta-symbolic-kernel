# Value Metrics

This document reports only public, reproducible value metrics from the limited
demonstrator. It does not report production-system metrics, customer
outcomes, production service levels, clinical utility, regulated performance, or
commercial validation.

## Current Public Dataset

Source: `benchmarks/results/metrics.json`

| Metric | Current value |
| --- | ---: |
| Schema version | `synthetic-comparison/v1` |
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
| Critical false-pass rate | 0.00 |
| False positive blocks / false alarms | 0 |
| False positive block rate | 0.00 |
| Unsafe block rate | 1.00 |
| Exact PASS / WARN / BLOCK match rate | 1.00 |
| Safe pass rate | 1.00 |
| Warning preservation rate | 1.00 |
| PASS decisions | 4 |
| WARN decisions | 4 |
| BLOCK decisions | 4 |
| Decisions with audit digest | 12 |
| Audit coverage rate | 1.00 |
| Deterministic replay | `true` |

These values mean that the current public gate produces one auditable decision
per public scenario and replays deterministically on the included synthetic
benchmark set.

## How To Read Error Metrics

The public benchmark is a three-verdict control test. For a safety-control
reading, synthetic unsafe cases that should be `BLOCK` are treated as the
positive class.

| Metric | Interpretation |
| --- | --- |
| `false_pass` | Critical miss: an unsafe synthetic case was not blocked. This is the safety-control false negative. |
| `false_block` / `false_positive_block` | False alarm: a synthetic `PASS` or `WARN` case was blocked. This is the safety-control false positive. |
| `critical_false_pass_rate` | `false_pass` divided by expected `BLOCK` cases. Lower is better. |
| `unsafe_block_rate` | Share of expected `BLOCK` cases that were blocked. Higher is better. |
| `false_positive_block_rate` | False positive blocks divided by expected non-`BLOCK` cases. Lower is better. |
| `safe_pass_rate` | Share of expected `PASS` cases that remained `PASS`. |
| `warning_preservation_rate` | Share of expected `WARN` cases that remained `WARN`. |
| `exact_match_rate` | Share of all scenarios where the observed verdict exactly matched the expected `PASS` / `WARN` / `BLOCK` label. |
| `audit_coverage_rate` | Share of decisions carrying an audit digest. |

These metrics are interpretation aids for the public synthetic benchmark only.
They are not domain validation, production performance, external validation, or
statistical significance evidence.

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
| Benchmark external-framework comparison claim | `false` |
| Benchmark statistical significance claim | `false` |
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
