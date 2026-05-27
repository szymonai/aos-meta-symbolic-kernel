# Operational Control Replay Summary

This benchmark replays public time-series traces through a fixed AOS
control policy. It measures whether labeled anomaly windows pass
silently, route to review, or block. It is an offline shadow-mode
benchmark, not a production deployment proof.

Source:

- dataset: `Numenta Anomaly Benchmark`
- repository: `https://github.com/numenta/NAB`
- commit: `ea702d75cc2258d9d7dd35ca8e5e2539d71f3140`
- license: `MIT`
- labels SHA-256: `164294d56679e33a9323f6b3824754183dbf661e31848f328bfc57019df804c4`

Protocol:

- benchmark kind: `public_operational_shadow_replay`
- primary use: `production_relevant_offline_shadow_replay`
- rolling window: `48`
- minimum history: `48`
- limit: `7000`
- warning margin: `2000`
- evaluated records: `362774`
- anomaly windows: `116`
- aggregate decision SHA-256: `ce1b50e45bae936f194cca7d03eb1ac334dcead147ce20d75927e300164c86cf`

Production-Relevant Proof Profile:

- claim type: `production_relevant_offline_replay`
- public operational data: `True`
- offline shadow mode: `True`
- fixed policy: `True`
- labels used as AOS input signals: `False`

Scalability Profile:

- scale unit: `evaluated_records`
- gate complexity per signal: `O(1)`
- extractor complexity: `O(records * rolling_window log rolling_window); practical linear for fixed rolling_window`
- streaming shape: `series-by-series replay with bounded rolling history`

Useful for:

- `offline shadow-mode replay on public operational time-series data`
- `measuring silent anomaly pass-through under a fixed public policy`
- `checking deterministic replay and local audit evidence coverage`
- `comparing review-band control against pass-through and block-only baselines`

Not useful for:

- `production deployment proof`
- `service-level agreement`
- `regulated-use approval`
- `ranking anomaly-detection models`
- `external validation`
- `domain-specific safety approval`

| Guard | Window silent pass | Window review/block | Record review/block | False block | Nominal intervention | Audit | Replay |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pass_through_baseline | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| block_only_score_baseline | 6.03% | 93.97% | 10.44% | 8.69% | 8.69% | 0.00% | 0.00% |
| aos_control_gate | 3.45% | 96.55% | 14.68% | 8.69% | 12.76% | 100.00% | 100.00% |

Interpretation:

- `anomaly_window_silent_pass_rate` is the share of labeled anomaly
  windows with no `WARN` or `BLOCK` decision.
- `anomaly_window_review_or_block_rate` is the share of labeled anomaly
  windows with at least one `WARN` or `BLOCK` decision.
- `anomaly_review_or_block_rate` is the share of anomaly-window records
  routed to `WARN` or `BLOCK`; this is secondary because NAB labels
  anomaly windows rather than every point as an incident.
- `false_block_rate` is the share of nominal records blocked.
- `nominal_intervention_rate` is the share of nominal records routed to
  `WARN` or `BLOCK`.
- `audit_coverage_rate` and `replay_success_rate` are local demonstrator
  evidence checks for the AOS guard.

Falsification Criteria:

- claim: `For the pinned public dataset, policy, and code path, the committed operational replay artifacts reproduce and AOS audit evidence replays.`
- check command: `python benchmarks/run_operational_control_replay.py --check`
- fail if: `committed metrics or summary drift under the same dataset and code`
- fail if: `AOS audit coverage falls below 100% for evaluated records`
- fail if: `AOS replay success falls below 100% for evaluated records`
- fail if: `labels are used as AOS input signals`
- fail if: `claim-boundary flags are changed to production or regulated-use claims`
- fail if: `aggregate decision stream hash changes without artifact update`

Boundary:

The score extractor is deterministic and label-independent, but it is
not a claim that AOS is an anomaly detector. The result is production-
relevant control evidence over public frozen traces.
