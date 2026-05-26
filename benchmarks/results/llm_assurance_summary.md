# LLM Assurance Offline Benchmark Summary

This benchmark evaluates fixed LLM-like outputs against evidence and
policy signals. It is an offline smoke benchmark, not a live LLM
evaluation, external guardrail-framework comparison, or general
hallucination-rate claim. It is not sufficient for a high-quality
public effectiveness proof.

- schema: `llm-assurance-offline/v1`
- scenarios: `20`
- evidence level: `E1_FIXED_OUTPUT_OFFLINE_SMOKE`
- public evidence status: `INSUFFICIENT_FOR_HIGH_QUALITY_PUBLIC_EFFECTIVENESS_PROOF`
- claim strength: `smoke_test_only`
- technical claim: `On this fixed smoke benchmark, a deterministic evidence gate reduces silent pass-through of unsupported, policy-violating, and unsafe agent outputs versus simple local baselines while preserving replayable audit evidence.`
- confidence intervals: `Wilson score interval, 95%`
- scenario SHA-256: `c8e0e34a28d5afdfd5bbdc79b1a74c6401a27ff88ae187fd6061fb611849da99`
- surfaces: `supported LLM answers, insufficient-evidence RAG answers, unsupported LLM claims, policy-violating outputs, unsafe agent action proposals`
- per-case decision records: `80`
- difficulty scope: `mostly D1-D2`
- scalability profile: `O(number_of_scenarios * number_of_guards)`

| Guard | Unsupported pass | Policy pass | Unsafe-action pass | Block recall | Safe pass | Warn yield | Warn load | False block | Audit coverage | Replay |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| llm_only | 100.00% | 100.00% | 100.00% | 0.00% | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| citation_presence_guard | 100.00% | 66.67% | 100.00% | 0.00% | 100.00% | 40.00% | 15.00% | 0.00% | 0.00% | 100.00% |
| prompt_guardrail_sim | 100.00% | 0.00% | 0.00% | 50.00% | 100.00% | 80.00% | 20.00% | 0.00% | 0.00% | 100.00% |
| aos_evidence_gate | 0.00% | 0.00% | 0.00% | 100.00% | 100.00% | 100.00% | 25.00% | 0.00% | 100.00% | 100.00% |

Interpretation:

- `unsupported_pass_rate` is the share of unsupported claims that
  passed without warning or block.
- `policy_violation_pass_rate` is the share of policy violations that
  passed without warning or block.
- `unsafe_action_pass_rate` is the share of unsafe action proposals that
  passed without warning or block.
- `block_recall` is the share of expected `BLOCK` cases blocked.
- `warn_yield` is the share of insufficient-evidence cases routed to
  `WARN`.
- `audit_coverage_rate` means local replay digest coverage only.
- CI fields in the JSON use Wilson 95% intervals and are descriptive
  only. This benchmark does not claim statistical significance.

The AOS evidence gate uses normalized scenario signals. It does not
prove semantic truth, retrieve evidence, validate a live model, or
provide a high-quality public effectiveness proof.
