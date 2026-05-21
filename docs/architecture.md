# Public Architecture

AOS is presented here as a domain-neutral meta-symbolic verification layer. The
public architecture is deliberately small:

```text
AI model
  -> uncertain output
  -> explicit policy
  -> AOS gate
  -> PASS / WARN / BLOCK
  -> explanation
  -> audit manifest
  -> optional Lean proof surface
```

`Meta-symbolic` means that the layer operates above model internals while using
explicit symbolic policies, deterministic verdict logic, and replayable evidence
to supervise model-output effects.

## Components

| Component | Public role |
| --- | --- |
| AI model | Produces an output or metadata signal |
| Uncertain output | Carries a value, uncertainty, confidence, or quality signal |
| Explicit policy | Defines the public demonstrator boundary |
| AOS gate | Produces a deterministic verdict |
| Verdict | Routes the workflow as `PASS`, `WARN`, or `BLOCK` |
| Explanation | Gives the public reason for the verdict |
| Audit manifest | Preserves a reproducible evidence identifier and, for signed packets, Ed25519 provenance metadata |
| Lean proof surface | Covers abstract verdict logic only |

## Runtime Assurance Pattern

The public pattern is not model replacement. It is a control layer around model
effects:

```text
probabilistic model output -> deterministic control decision
```

This is useful when a workflow needs explicit review triggers, audit evidence,
and a clear separation between AI output and operational decision-making.

## Boundary

This public architecture does not describe production-system internals,
deployment integrations, deployment settings, production security, or delivery
material.

See [Integrity Anchors](INTEGRITY_ANCHORS.md) for the public SHA-256, SHA-512,
and Ed25519 convention.
