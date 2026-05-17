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
| Governance teams need claim boundaries | Separate model output, AOS verdict, human decision, and external claim |
| AI systems are domain-specific | Keep the public control pattern domain-neutral |

## What This Does Not Mean

AOS does not claim that a model is correct. It does not eliminate hallucinations,
replace human review, certify a workflow, or make clinical, regulatory, or
production-readiness claims in this public repository.

The public value is narrower and more defensible: deterministic control over
bounded model-output signals, audit evidence, and a clear decision boundary.
