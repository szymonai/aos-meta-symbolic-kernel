# Public Architecture

AOS is presented here as a domain-neutral meta-symbolic kernel. The public
architecture is deliberately small:

```text
source system or AI output
  -> signal extraction / normalization adapter
  -> bounded public signal
  -> explicit policy
  -> AOS gate
  -> PASS / WARN / BLOCK
  -> explanation
  -> replayable audit evidence
  -> optional Lean proof surface
```

`Meta-symbolic` means that the kernel operates above model internals while using
explicit symbolic policies, deterministic verdict logic, and replayable evidence
to supervise model-output effects. `Kernel` means the compact control core that
turns bounded signals and policy rules into workflow verdicts. Verification is
one function of that kernel, alongside gating, routing, and evidence generation.

## Components

| Component | Public role |
| --- | --- |
| Source system or AI output | Produces raw material for evaluation |
| Signal extraction / normalization adapter | Converts raw material into bounded public signals |
| Bounded public signal | Carries score, uncertainty, limit, warning margin, and metadata completeness |
| Explicit policy | Defines the public demonstrator boundary |
| AOS gate | Produces a deterministic verdict |
| Verdict | Routes the workflow as `PASS`, `WARN`, or `BLOCK` |
| Explanation | Gives the public reason for the verdict |
| Audit manifest | Preserves a reproducible evidence identifier and, for signed packets, Ed25519 provenance metadata |
| Lean proof surface | Covers abstract verdict logic only |
| Runtime substrate | Executes the contract without changing AOS semantics |

## Runtime Assurance Pattern

The public pattern is not model replacement and not anomaly detection. It is a
control kernel around bounded signals derived from model outputs or operational
traces:

```text
raw output or trace -> bounded signal -> deterministic control decision
```

This is useful when a workflow needs explicit review triggers, audit evidence,
and a clear separation between AI output and operational decision-making.

## Substrate Independence

AOS is defined by the control contract, not by a programming language, CPU/GPU
target, or operating-system layer. The public implementation uses Python for
the reference runtime and Lean 4 for a narrow proof surface. C++, Rust, CUDA,
PTX, assembly, WASM, and eBPF would be optional implementation substrates only.
They may improve deployment shape, latency, portability, or hardware placement,
but they must preserve the same bounded-signal, policy, verdict, and audit
contract.

See [Runtime Substrates](RUNTIME_SUBSTRATES.md).

## Evidence Profiles

The same public control kernel is exercised by different evidence profiles:

| Profile | Source | Architectural meaning |
| --- | --- | --- |
| Synthetic demonstrator | Handwritten bounded signals | Checks the public gate and replay path |
| LLM/agent fixed outputs | Pre-normalized evidence signals | Checks policy and evidence gating behavior |
| Operational control replay | Public time-series traces plus deterministic extractor | Checks control behavior after signal extraction |

The operational replay profile adds an adapter before the gate. It does not
change the AOS core contract: AOS still receives a bounded signal and returns a
deterministic verdict with replayable evidence.

## Boundary

This public architecture does not describe production-system internals,
deployment integrations, deployment settings, production security, or delivery
material.

The public Lean surface covers the verdict contract after signal extraction. It
does not prove the correctness of signal extraction, threshold calibration,
domain validity, or production behavior.

See [Integrity Anchors](INTEGRITY_ANCHORS.md) for the public SHA-256, SHA-512,
and Ed25519 convention.
