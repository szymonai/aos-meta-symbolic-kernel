# Plain-Language Overview

AOS is a control layer for AI systems.

It does not replace the AI model. It checks the model's output before that
output affects a workflow.

## The Basic Idea

Many AI systems produce useful but uncertain outputs. AOS adds a deterministic
checkpoint between the model and the workflow:

```text
AI output -> AOS check -> PASS / WARN / BLOCK -> audit evidence
```

In plain terms:

- `PASS` means the output can continue through the public demo workflow.
- `WARN` means the output should be reviewed or escalated.
- `BLOCK` means the output should not continue without further review.

## Why This Is Useful

AOS helps separate three things that are often mixed together:

- what the model produced;
- what the control layer decided;
- what a human or organization does next.

That separation is useful for auditability, review triggers, governance, and
workflow safety.

## What This Public Repository Shows

This repository shows a limited public version of the pattern:

- a small `PASS` / `WARN` / `BLOCK` gate;
- synthetic examples;
- reproducible benchmark metrics;
- public audit identifiers;
- a small formal proof surface for abstract verdict logic;
- clear boundaries around what is not being claimed.

## What This Public Repository Does Not Show

This repository does not publish the private AOSKernel, production deployment
materials, customer data, private decision parameters, clinical validation,
regulatory approval, or commercial performance evidence.

The public repository should be read as a transparent demonstrator of the
control-layer idea, not as the full private system.
