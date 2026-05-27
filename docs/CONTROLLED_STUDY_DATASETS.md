# Controlled-Study Public Dataset Profile

This profile defines the clean public-data path for a controlled study. It does
not publish dataset records or claim that effectiveness evidence has already
been achieved.

Public-data runs produced from label-to-signal mapping are protocol evidence,
not effectiveness proof by themselves. They validate reproducibility, audit
coverage, and comparator execution. They do not prove that AOS can
independently infer semantic truth from raw text.

## Dataset Order

| Order | Dataset | Controlled-study use | Current fit |
| --- | --- | --- | --- |
| 1 | RAGTruth | RAG hallucination and grounding | Best first target: public model responses, model id, temperature, split, labels |
| 2 | HaluEval | hallucination/factuality | Strong scale target: public examples and generated answers |
| 3 | AgentDojo | agent prompt-injection and tool-use control | Agent profile: requires benchmark run and frozen trajectories |
| 4 | FEVER | factual claim verification | Grounding profile: requires model outputs generated from claims/evidence |

## Clean Controlled-Study Rule

Do not force every dataset into one broad claim. Use a profile:

| Profile | Required categories | Required difficulty classes | Best datasets |
| --- | --- | --- | --- |
| `hallucination_text` | `SUPPORTED`, `UNSUPPORTED` | D1, D3, D4 | RAGTruth, HaluEval |
| `rag_grounding` | `SUPPORTED`, `INSUFFICIENT_EVIDENCE`, `UNSUPPORTED` | D1-D6 | RAGTruth plus generated/curated RAG uncertainty cases |
| `agent_control` | `SUPPORTED`, `POLICY_VIOLATION`, `UNSAFE_ACTION` | D7-D9 | AgentDojo |
| `full_stack` | all AOS categories | D1-D9 | combined benchmark only |

RAGTruth and HaluEval are the cleanest first target under
`hallucination_text`. AgentDojo and FEVER are public-data sources, but they
require a controlled generation or benchmark run before they can satisfy a
frozen-output profile.

## Required Frozen Record

Each public-data record must be normalized to:

```text
id
freeze_schema_version
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

## Dataset Mapping

| Dataset | Direct field source | AOS mapping |
| --- | --- | --- |
| RAGTruth | `response`, `model`, `temperature`, `split`, `labels` | non-empty hallucination labels map to `UNSUPPORTED`; empty labels map to `SUPPORTED` |
| HaluEval | `right_*`, `hallucinated_*`, `chatgpt_response`, `hallucination_label` | hallucinated or positive hallucination labels map to `UNSUPPORTED`; right answers map to `SUPPORTED` |
| AgentDojo | benchmark trajectory, tool calls, injection task result | unsafe or policy-violating tool behavior maps to `UNSAFE_ACTION` or `POLICY_VIOLATION` |
| FEVER | `claim`, `label`, `evidence` plus generated model response | `SUPPORTS` maps to `SUPPORTED`; `REFUTES` maps to `UNSUPPORTED`; `NOT ENOUGH INFO` maps to `INSUFFICIENT_EVIDENCE` |

## Protocol Quality Gate

A controlled-study protocol run should fail unless it has:

- 500+ frozen records;
- named public dataset sources with license/provenance;
- frozen model-output hashes and source-record hashes;
- unique record ids;
- output-generation metadata where outputs were generated locally;
- declared labeling protocol;
- all categories required by the selected profile represented;
- all difficulty classes required by the selected profile represented;
- at least 20 cases per required category and difficulty class;
- predefined metrics and named comparators.

## Effectiveness Quality Gate

A high-quality public effectiveness claim requires a second gate:

- normalized signals are produced by an independent extractor;
- dataset labels are not used directly as AOS input signals;
- the normalization layer is evaluated separately;
- a held-out subset is manually audited;
- baselines receive matched inputs;
- false blocks, warnings, and failures are reported;
- trade-off metrics are reported with the headline metrics.

## Public Evidence Boundary

Do not commit large frozen-output files, full per-case metrics, or local
controlled-study artifacts as default public evidence. Keep them reproducible
through commands and publish only a curated summary after review.

A stronger public result should add a non-tautological layer:

- raw model outputs are normalized by an extractor that is evaluated separately;
- labels are not used directly as AOS input signals;
- a held-out subset is manually audited;
- baselines receive the same normalized inputs;
- failures and false blocks are reported, not only headline rates.

## Claim Boundary

Acceptable claim after a passing controlled-study run:

```text
On frozen public-data benchmark X, AOS reduced silent pass-through of
unsupported, policy-violating, or unsafe outputs versus named baselines under
the declared policy and metrics.
```

Not acceptable:

```text
AOS eliminates hallucinations.
AOS proves model truthfulness.
AOS is production-ready.
AOS is externally replicated.
```
