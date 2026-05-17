# Universal Kernel Positioning

AOS is positioned as a deterministic AI control and audit layer:

```text
one AOS control kernel -> many specialist profiles
```

The kernel pattern is intentionally simple at the public level:

```text
model output
  -> uncertainty or quality signal
  -> deterministic control envelope
  -> PASS / WARN / BLOCK
  -> audit evidence
  -> human review, escalation, or workflow hold
```

## Why This Matters

Most AI evaluation focuses on model quality. AOS focuses on controlled use of
model outputs. That distinction is commercially important because the same
runtime assurance layer can be adapted across domains where organizations need
traceability, review triggers, escalation logic, and evidence discipline before
AI output enters a real workflow.

AOS is domain-neutral by design and can be adapted to different AI workflows,
including enterprise automation, governance, cybersecurity, industrial systems,
research pipelines, and regulated domains.

## Instance 01: Radiology

The radiology reference profile is Instance 01. It demonstrates how a specialist
system can use model outputs and uncertainty signals as inputs to an auditable
control layer.

The public repository publishes only a bounded evidence review:

- internal n=484 cohort milestone: Dice WT `0.8108`, Dice ET `0.8033`, ET recall
  `0.8065`;
- selected Dataset832 fold artifact: label-2 Dice `0.8843`, label-2 recall
  `0.9085`, label-2 precision `0.8665` on 2 validation cases;
- formal-integrity milestone: Lean/Lake `3292/3292` tasks, root build exit code
  `0`, and a public SHA-512 anchor.

This is utility evidence for the architecture. It is not a clinical
validation claim and not a radiology product release.

## Other Potential Profiles

The same kernel pattern can support several application profiles, including:

- LLM/RAG answer review and workflow approval
- enterprise copilot governance
- industrial monitoring and maintenance escalation
- cyber-defense triage and audit
- edge deployment guardrails
- regulated decision-support workflows

The public repository does not publish production-system material,
specialist-system material, customer-specific evidence, or commercial delivery
materials.

See [Application Profiles](APPLICATION_PROFILES.md) for a bounded, non-product
view of potential adaptations.

## Safety Boundary

AOS can be framed with safety-assurance discipline, but this repository does
not claim safety certification, MDR compliance, AI Act compliance, CE marking,
production readiness, or external validation.
