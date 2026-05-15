# Synthetic Technical Advantage Summary

This benchmark compares deterministic interval gating with three simple
guardrail baselines on synthetic scenarios. It is not a production
benchmark, external validation, or domain validation claim.

| Guard | False pass | False block | PASS | WARN | BLOCK | Audit records | Replay |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| simple_threshold_guard | 2 | 0 | 10 | 0 | 2 | 0 | True |
| json_schema_guard | 4 | 0 | 12 | 0 | 0 | 0 | True |
| prompt_guardrail_sim | 2 | 0 | 4 | 6 | 2 | 0 | True |
| aos_gate_adapter | 0 | 0 | 4 | 4 | 4 | 12 | True |

Interpretation:

- `false_pass` means a synthetic unsafe scenario was not blocked.
- `audit_record_present` counts decisions that include an audit digest.
- `deterministic_replay_passed` means rerunning the same guard on the
  same scenarios produced identical decisions and audit digests.

The public AOS demo gate is expected to block all synthetic unsafe
cases because it evaluates `value + uncertainty` against the limit.
