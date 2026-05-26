# AI Problems Addressed

This document describes the public problem framing for AOS. It is not a claim
that the public demonstrator solves all AI safety, governance, security, or
regulatory problems.

| Current AI problem | AOS public response |
| --- | --- |
| Model outputs are probabilistic | Add deterministic `PASS` / `WARN` / `BLOCK` control decisions |
| Uncertainty is often lost after inference | Evaluate uncertainty or quality signals before workflow use |
| Guardrails can be hard to audit | Attach a reproducible audit identifier to each public decision |
| Prompt-only policy can be ambiguous | Use explicit public rules in the demonstrator |
| Reviews need escalation signals | Route uncertain or unsafe public cases to `WARN` or `BLOCK` |
| Many AI outputs look similarly plausible | Let policy-compliant outputs proceed while escalating or blocking others |
| Downstream actions can be expensive | Make review, experimentation, compute, or operational escalation more selective |
| Edge workflows need local control | Keep the public gate pattern small, deterministic, and replayable |
| Governance teams need claim boundaries | Separate model output, AOS verdict, human decision, and external claim |
| AI systems are domain-specific | Keep the public control pattern domain-neutral |
| LLM outputs may include unsupported claims | Define measurable `unsupported_pass_rate` rather than claiming hallucination elimination |
| Agent plans can contain invalid or unsafe actions | Treat LLM plans as candidates that require symbolic policy checks before execution |

## What This Does Not Mean

AOS does not claim that a model is correct. It does not eliminate hallucinations,
replace human review, approve a workflow, or make domain, regulatory, or
production-readiness claims in this public repository.

The public value is narrower and more defensible: deterministic control over
bounded model-output signals, audit evidence, and a clear decision boundary for
selective progression, escalation, or blocking.

Future LLM-oriented claims require a separate reproducible evaluation profile.
See [LLM assurance evaluation](LLM_ASSURANCE_EVALUATION.md).
