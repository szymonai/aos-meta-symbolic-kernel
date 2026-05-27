# Value Metrics

This document reports only public, reproducible value metrics from the limited
demonstrator. It does not report production-system metrics, deployment
outcomes, production service levels, domain utility, regulated performance, or
market validation.

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

`Audit coverage rate` means that each demonstrator decision carries a local
replay digest. It does not mean that the repository publishes a production audit
ledger, signing infrastructure, HMAC key design, immutable log store, retention
policy, or non-repudiation mechanism.

## Operational Control Replay

Source: `benchmarks/results/operational_control_replay_metrics.json`

This is the strongest current public effectiveness artifact. It replays public
frozen operational time-series traces from the Numenta Anomaly Benchmark through
a deterministic signal extractor and the AOS public gate. It is offline
shadow-mode evidence, not production deployment evidence.

| Metric | Current value |
| --- | ---: |
| Schema version | `operational-control-replay/v1` |
| Source series | 58 |
| Evaluated records | 362,774 |
| Labeled anomaly windows | 116 |
| AOS anomaly-window review/block rate | 96.55% |
| AOS anomaly-window silent pass rate | 3.45% |
| AOS record-level anomaly review/block rate | 14.68% |
| AOS false block rate | 8.69% |
| AOS nominal intervention rate | 12.76% |
| AOS audit coverage rate | 100.00% |
| AOS replay success rate | 100.00% |

These values are useful because they expose the trade-off directly: the AOS
control gate catches nearly all labeled anomaly windows at least once, but it
also creates review/intervention load on nominal records. The result is
production-relevant control evidence over frozen traces; it is not a claim that
AOS is an anomaly-detection model.

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
| `audit_coverage_rate` | Share of decisions carrying a local replay digest. |

These metrics are interpretation aids for the public synthetic benchmark only.
They are not domain validation, production performance, external validation, or
statistical significance evidence. They are also not sufficient for a
high-quality public effectiveness proof.

## Public Boundary Metrics

Sources: `evidence/demonstrator_manifest.json` and
`benchmarks/results/metrics.json`

| Boundary field | Current value |
| --- | --- |
| Production-system code included | `false` |
| Internal policy logic included | `false` |
| Real-world domain thresholds included | `false` |
| Specialist validation materials included | `false` |
| Data redistributed in repository | `false` |
| Domain-validation claim | `false` |
| External validation completed | `false` |
| High-quality public effectiveness proof claim | `false` |
| Public effectiveness proof sufficient | `false` |
| Regulated-use claim | `false` |
| Regulatory compliance claim | `false` |
| Safety-approval claim | `false` |
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
- domain safety or domain utility
- regulated-use approval
- regulatory compliance
- external validation
- high-quality public effectiveness proof
- deployment ROI
- revenue performance
- external performance ranking
- access to production-system material

Any future public value claim should identify the exact evidence source, the
dataset or workflow boundary, the current numeric result, and the claims that
remain out of scope.
