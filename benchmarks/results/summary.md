# Synthetic Demonstrator Comparison Summary

This benchmark compares deterministic interval gating with three simple
guardrail baselines on synthetic scenarios. It is not a production
benchmark, external validation, or domain validation claim.

Scope limits: the scenario set has 12 synthetic cases, the baselines
are intentionally simple, no external guardrail frameworks are
included, and no statistical significance claim is made.

| Guard | False pass | False block | Exact match | Unsafe block rate | False positive block rate | Audit coverage | Replay |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| simple_threshold_guard | 2 | 0 | 50.00% | 50.00% | 0.00% | 0.00% | True |
| json_schema_guard | 4 | 0 | 33.33% | 0.00% | 0.00% | 0.00% | True |
| prompt_guardrail_sim | 2 | 0 | 66.67% | 50.00% | 0.00% | 0.00% | True |
| aos_gate_adapter | 0 | 0 | 100.00% | 100.00% | 0.00% | 100.00% | True |

Verdict distribution:

| Guard | PASS | WARN | BLOCK | Audit records |
| --- | ---: | ---: | ---: | ---: |
| simple_threshold_guard | 10 | 0 | 2 | 0 |
| json_schema_guard | 12 | 0 | 0 | 0 |
| prompt_guardrail_sim | 4 | 6 | 2 | 0 |
| aos_gate_adapter | 4 | 4 | 4 | 12 |

Interpretation:

- `false_pass` means a synthetic unsafe scenario was not blocked. In a
  safety-control reading, this is the critical false negative.
- `false_block` means a synthetic PASS or WARN scenario was blocked. In a
  safety-control reading, this is the false positive / false alarm.
- `unsafe_block_rate` is the share of synthetic unsafe cases that were
  correctly blocked.
- `exact_match_rate` is the share of scenarios where the observed verdict
  exactly matches the expected PASS / WARN / BLOCK label.
- `audit_record_present` counts decisions that include an audit digest.
- `audit_coverage_rate` is the share of decisions with an audit digest.
- `deterministic_replay_passed` means rerunning the same guard on the
  same scenarios produced identical decisions and audit digests.

The public AOS demo gate is expected to block all synthetic unsafe
cases because it evaluates `value + uncertainty` against the limit.
