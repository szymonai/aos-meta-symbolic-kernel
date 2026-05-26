# LLM Assurance Evaluation

This document defines the evidence standard for evaluating AOS on LLM outputs.
It is a future evaluation profile, not a current superiority claim.

## Evaluation Target

AOS should be evaluated as a deterministic control layer above an LLM:

```text
LLM output + evidence signals + explicit policy
  -> AOS gate
  -> PASS / WARN / BLOCK
  -> replayable audit evidence
```

The core question is not whether AOS makes the LLM truthful. The question is:

```text
How often does AOS prevent unsupported, policy-violating, or unsafe outputs
from passing silently?
```

For agentic systems, the same question applies to proposed actions:

```text
How often does AOS prevent invalid, unsafe, or policy-violating tool calls
from reaching execution?
```

## Claim Types

| Claim | Evidence type | Public status |
| --- | --- | --- |
| Hallucination-rate reduction | Empirical benchmark | Not yet claimed |
| Policy compliance | Formal proof over normalized symbolic inputs | Partially demonstrated for the abstract verdict model |
| Planner robustness | Adversarial plan/action benchmark | Not yet claimed |
| Guardrail comparison | Reproducible benchmark against named baselines | Not yet claimed |

## Evidence Layers

| Layer | Meaning | Minimum evidence |
| --- | --- | --- |
| Design claim | Architecture and policy definition only |
| Fixed-output smoke | Public fixed outputs, per-case verdicts, replay digests |
| Reproducible hard-case benchmark | 100+ cases, multiple surfaces, confidence intervals |
| Controlled-study protocol | 500+ cases, frozen model outputs, named comparators, ablations |
| Controlled-study effectiveness | Protocol gate plus independent signal extraction, normalization audit, matched baselines, failures, and trade-offs |
| External replication | Independent reproduction by third party |

The current public LLM/agent profile is a fixed-output smoke benchmark. The
repository also contains a synthetic hard-case benchmark. Neither is sufficient
for a high-quality public effectiveness proof. A stronger public claim should
target controlled-study effectiveness or higher.

Candidate technical claim:

```text
A deterministic evidence gate can reduce silent pass-through of unsupported,
policy-violating, and unsafe agent outputs versus simple guard baselines,
while preserving replayable audit evidence.
```

This claim becomes defensible only when tested on a larger predefined benchmark
with fixed comparators and reported uncertainty.

## Minimal Benchmark Shape

Each scenario should include:

```text
scenario_id
prompt
model_output
reference_evidence
policy
expected_label
aos_verdict
baseline_verdicts
audit_digest
replay_verdict
```

The expected label should be assigned before evaluation:

```text
SUPPORTED
UNSUPPORTED
POLICY_VIOLATION
INSUFFICIENT_EVIDENCE
UNSAFE_ACTION
```

AOS maps these labels into workflow decisions:

```text
SUPPORTED -> PASS
INSUFFICIENT_EVIDENCE -> WARN
UNSUPPORTED / POLICY_VIOLATION / UNSAFE_ACTION -> BLOCK
```

## Agent And Tool-Call Criteria

Agentic evaluation should include more than text hallucination. A valid scenario
set should cover:

| Surface | Example failure | Expected control response |
| --- | --- | --- |
| Factual answer | Unsupported claim | `BLOCK` |
| RAG answer | Insufficient source coverage | `WARN` |
| Policy answer | Instruction conflicts with policy | `BLOCK` |
| Tool call | Invalid or missing required argument | `BLOCK` or `WARN` |
| Planner step | Action order violates preconditions | `BLOCK` |
| Execution proposal | Destructive or privileged action | `BLOCK` |
| Prompt injection | Request attempts to override policy | `BLOCK` |

The LLM or agent planner should be treated as a candidate generator. AOS should
evaluate normalized evidence and action signals before any downstream action is
accepted or executed.

## Metrics

Primary metrics:

| Metric | Meaning |
| --- | --- |
| `unsupported_pass_rate` | Unsupported outputs that passed without warning or block |
| `policy_violation_pass_rate` | Policy violations that passed without warning or block |
| `unsafe_action_pass_rate` | Unsafe actions that passed without warning or block |
| `invalid_tool_call_pass_rate` | Invalid tool calls that passed without warning or block |
| `block_recall` | Share of expected `BLOCK` cases blocked |
| `warn_yield` | Share of uncertain cases routed to `WARN` |
| `false_block_rate` | Supported outputs incorrectly blocked |
| `audit_coverage_rate` | Decisions carrying replay evidence |
| `replay_success_rate` | Same inputs reproduce the same verdict and audit evidence |

Secondary metrics:

| Metric | Meaning |
| --- | --- |
| `latency_overhead_ms` | Added local gate latency |
| `policy_determinism_rate` | Same normalized input and policy produce same decision |
| `baseline_delta` | Difference between AOS and each comparator on primary metrics |

## Evidence Density

A useful public benchmark should expose enough structure for external review:

- one row per scenario and per guard;
- expected label assigned before evaluation;
- observed verdict for each guard;
- primary metrics by failure type;
- confidence intervals for rate metrics;
- scenario hash;
- deterministic replay status;
- audit digest coverage;
- claim-boundary flags.

Aggregate-only results are weak evidence. Per-case results plus hashes are more
useful because reviewers can inspect failure modes, not only headline rates.

## Difficulty Controls

A low pass-through rate is only meaningful if the scenarios are hard enough.
The benchmark should report difficulty classes:

| Class | Description |
| --- | --- |
| D1 | Obvious violation with clean evidence |
| D2 | Missing or incomplete evidence |
| D3 | Partially true answer with unsupported extra claim |
| D4 | Noisy evidence or weak citation support |
| D5 | Conflicting retrieval evidence |
| D6 | Manipulated or irrelevant citations |
| D7 | Prompt-injection attempt |
| D8 | Agentic tool misuse or invalid action plan |
| D9 | Conflicting policies or unclear precedence |

Current smoke scenarios are mostly D1-D2. That makes the benchmark useful as a
smoke test, not as a hard robustness result.

## Required Hard Cases

A stronger benchmark should include:

- noisy evidence;
- partially true answers with unsupported additions;
- manipulated citations;
- irrelevant citations;
- prompt injection;
- conflicting retrieval;
- ambiguous policy language;
- policy precedence conflicts;
- invalid tool arguments;
- tool calls with missing authorization;
- destructive tool actions;
- multi-step plans that violate preconditions.

## Scalability Criteria

The benchmark should scale linearly:

```text
O(number_of_scenarios * number_of_guards)
```

Scale-up should add cases before adding rhetoric:

| Scale | Use |
| --- | --- |
| 20 cases | Smoke test only |
| 100+ cases | Early reproducible benchmark |
| 500+ cases | Candidate controlled study |
| 1000+ cases | Stronger stress benchmark if labels remain auditable |

For agentic systems, the scaled dataset should include tool-call schemas,
planner preconditions, invalid arguments, forbidden actions, and prompt
injection attempts, not only factual QA.

## Trade-Off Metrics

Blocking more unsafe outputs is not sufficient. The evaluation must also report
costs:

| Metric | Meaning |
| --- | --- |
| `false_block_rate` | Supported outputs incorrectly blocked |
| `warn_load_rate` | Share of cases routed to review |
| `safe_pass_rate` | Supported outputs that still pass |
| `latency_overhead_ms` | Local decision overhead |
| `evidence_required_rate` | Cases needing additional evidence |
| `manual_review_cost_proxy` | Review volume created by `WARN` |

Without these trade-off metrics, a benchmark can hide an overly conservative
gate behind a strong `block_recall`.

## Known Unknowns

The current fixed-output smoke profile does not establish behavior under:

- thousands of cases;
- live model outputs;
- real hallucinations from current LLMs;
- ambiguous evidence;
- conflicting policies;
- adversarial prompting;
- noisy retrieval;
- citation manipulation;
- agentic tool misuse.

The correct interpretation is:

```text
The smoke benchmark shows that the public gate and metrics work on fixed
scenarios.
It does not show robust performance under realistic adversarial conditions.
```

## Controlled Study

The controlled-study layer is the first point where a strong public benchmark
claim becomes reasonable. It requires frozen model outputs, not synthetic-only
cases.

The clean public-data order and controlled-study profiles are defined in
[controlled-study public dataset profile](E3_PUBLIC_DATASETS.md): RAGTruth,
HaluEval, AgentDojo, then FEVER.

Runnable protocol:

```bash
python benchmarks/freeze_public_outputs.py \
  --input path/to/public_model_outputs.jsonl \
  --output path/to/frozen_outputs.jsonl \
  --source-dataset FEVER \
  --source-split test \
  --model-id provider/model-version

python benchmarks/freeze_ragtruth_outputs.py \
  --response path/to/ragtruth/response.jsonl \
  --source-info path/to/ragtruth/source_info.jsonl \
  --output path/to/frozen_outputs.jsonl \
  --manifest-output path/to/ragtruth_e3_manifest.json

python benchmarks/run_e3_controlled_study.py \
  --input path/to/frozen_outputs.jsonl \
  --manifest benchmarks/e3_study_manifest.example.json
```

Each input record must include:

```text
id
source_dataset
source_split
source_record_sha256
model_id
model_output
model_output_sha256
category
difficulty_class
expected_aos_verdict
required_citation_count
provided_citation_count
source_coverage
unsupported_claim_count
policy_violation_count
unsafe_action_count
```

Quality gates for controlled-study protocol:

- at least 500 frozen records;
- complete dataset provenance: dataset name plus URL or citation plus license
  reference;
- frozen model-output hashes and source-record hashes;
- explicit output-generation metadata: model id, prompt-template hash,
  temperature, and top-p;
- unique record identifiers;
- labeling protocol declared before evaluation;
- all categories required by the selected profile covered;
- all difficulty classes required by the selected profile covered;
- at least 20 cases per required category and difficulty class;
- named comparators and predefined metrics.

The controlled-study runner reports two levels:

```text
protocol_evidence_level
effectiveness_evidence_level
```

`protocol_evidence_level` reports whether the frozen-output study satisfies the
protocol criteria. `effectiveness_evidence_level` reports whether the run is
allowed to support an effectiveness claim.

Protocol evidence alone is not enough for a high-quality public proof. A
high-quality effectiveness claim additionally requires:

- independent signal extraction;
- labels not used directly as AOS input signals;
- separate evaluation of the normalization layer;
- held-out manual audit;
- matched comparator inputs;
- reported failures and trade-off metrics.

The Lean surface mirrors this boundary at the abstract level: controlled-study
readiness is reachable only when the readiness predicate holds, and the audit
predicate is required by that predicate. This does not prove semantic truth of
model outputs.

Passing the protocol gate is necessary but not sufficient for a strong public
effectiveness claim. When normalized AOS signals are derived directly from
dataset labels, the public evidence level must remain protocol-only.

## Stronger Evidence Minimum

Before making a strong public claim, require:

- 500+ labeled fixed-output cases;
- frozen model/provider versions or stored model outputs;
- named comparator implementations and versions;
- predefined metrics;
- Wilson or bootstrap confidence intervals;
- ablation: no gate, prompt guard, schema/citation guard, AOS;
- separate reporting for factual, RAG, policy, tool-call, planner, and unsafe
  action surfaces;
- public per-case results without private data.
- explicit separation between protocol evidence and effectiveness evidence.

## Comparator Set

A valid comparison should separate:

- LLM only;
- schema-only validation;
- prompt-only guardrail;
- deterministic threshold or rule guard;
- AOS gate;
- AOS gate plus any external guardrail, if included.

External framework comparisons require named versions, fixed configuration,
open scenario data, and reproducible execution logs. Without that, this
repository should not claim external-framework superiority.

## Formal Scope

Formal guarantees can cover:

- deterministic verdict selection;
- policy ordering;
- normalized input handling;
- `PASS` / `WARN` / `BLOCK` consistency;
- replay invariants over canonical evidence.

Formal guarantees do not cover:

- semantic truth of an LLM output;
- correctness of retrieved documents;
- completeness of evidence;
- production parser correctness unless separately verified;
- production runtime security;
- human or organizational decision quality.

## Public Claim Boundary

Acceptable future claim:

```text
On benchmark X, AOS reduced unsupported pass rate from A to B under policy P,
with replayable decisions and fixed comparator configurations.
```

Not acceptable:

```text
AOS eliminates hallucinations.
AOS proves LLM truthfulness.
AOS is superior to guardrails in general.
AOS makes agent systems safe.
```

## Current Status

The current public repository demonstrates deterministic synthetic policy
gating, audit digest coverage, deterministic replay, and a limited Lean proof
surface for the abstract verdict model.

It also includes a fixed-output offline LLM/agent assurance smoke benchmark
covering supported answers, insufficient-evidence RAG answers, unsupported
claims, policy violations, and unsafe agent action proposals.

It also includes a synthetic hard-case benchmark. This improves scale and
difficulty coverage, but remains fixed-output and synthetic.

The current evidence is insufficient for a high-quality public effectiveness
proof. It does not yet include a live LLM evaluation, independent normalization
study, adversarial planner benchmark, controlled 500+ case effectiveness study,
external replication, or external guardrail-framework comparison.
