# LLM/Agent Hard-Case Benchmark Summary

This benchmark evaluates fixed LLM-like outputs against evidence and
policy signals. It is an offline smoke benchmark, not a live LLM
evaluation, external guardrail-framework comparison, or general
hallucination-rate claim. It is not sufficient for a high-quality
public effectiveness proof.

- schema: `llm-assurance-offline/v1`
- scenarios: `540`
- evidence level: `E2_FIXED_OUTPUT_HARD_CASE_BENCHMARK`
- public evidence status: `INSUFFICIENT_FOR_HIGH_QUALITY_PUBLIC_EFFECTIVENESS_PROOF`
- claim strength: `synthetic_fixed_output_hard_case_only`
- technical claim: `On this fixed smoke benchmark, a deterministic evidence gate reduces silent pass-through of unsupported, policy-violating, and unsafe agent outputs versus simple local baselines while preserving replayable audit evidence.`
- confidence intervals: `Wilson score interval, 95%`
- scenario SHA-256: `8b8d9cd34fadb9a7dc5673a8f8593bd8a571825e9cf512d6237a3aba537f487c`
- surfaces: `supported LLM answers, insufficient-evidence RAG answers, unsupported LLM claims, policy-violating outputs, unsafe agent action proposals`
- per-case decision records: `2160`
- difficulty scope: `D1-D9`
- scalability profile: `O(number_of_scenarios * number_of_guards)`

| Guard | Unsupported pass | Policy pass | Unsafe-action pass | Block recall | Safe pass | Warn yield | Warn load | False block | Audit coverage | Replay |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| llm_only | 100.00% | 100.00% | 100.00% | 0.00% | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| citation_presence_guard | 100.00% | 100.00% | 100.00% | 0.00% | 100.00% | 50.00% | 10.00% | 0.00% | 0.00% | 100.00% |
| prompt_guardrail_sim | 66.67% | 66.67% | 66.67% | 0.00% | 66.67% | 100.00% | 46.67% | 0.00% | 0.00% | 100.00% |
| aos_evidence_gate | 0.00% | 0.00% | 0.00% | 100.00% | 100.00% | 100.00% | 20.00% | 0.00% | 100.00% | 100.00% |

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
