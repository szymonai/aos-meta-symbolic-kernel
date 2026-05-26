# Formal Claims Boundary

This document defines the public scope of the Lean proof surface. It is a
boundary statement, not a full-system verification claim.

## Public Scope

The public Lean layer verifies selected properties of an abstract
`PASS` / `WARN` / `BLOCK` verdict model. The public Python runtime is tested
against the same decision behavior on a bounded demonstrator subset.
It also contains a small abstract contract for audit-ready decisions,
controlled-study protocol gating, and the stronger effectiveness-evidence gate.

This supports a limited statement:

> The public repository demonstrates selected formal properties of a bounded
> verdict model and tests the reference runtime against that model in the public
> demonstrator.

## What Is Covered

- abstract verdict behavior;
- deterministic `PASS` / `WARN` / `BLOCK` structure;
- selected interval-boundary properties;
- audit-ready decision predicates over abstract records;
- controlled-study readiness predicates over abstract study criteria;
- public evidence-level separation between protocol and effectiveness evidence;
- synthetic benchmark behavior;
- bounded runtime correspondence tests.

## What Is Not Covered

- full Python-to-Lean refinement;
- arbitrary floating-point behavior;
- JSON/IO/security/key-management correctness;
- correctness of model-output hashes beyond the public runner checks;
- policy calibration or threshold validity;
- semantic truth of model outputs or retrieved evidence;
- deployment, concurrency, availability, or production security;
- domain, regulatory, financial, or safety approval;
- end-to-end product correctness.

## Safe Public Wording

Use:

> Lean verifies selected properties of the abstract public verdict model.

Avoid:

> The AOS system is formally verified.

Use:

> The public tests check bounded correspondence between the reference runtime
> and the public verdict model.

Avoid:

> The Lean layer proves production runtime correctness.

## Interpretation

A successful Lean build means that the selected formal target compiles in the
declared environment. It does not, by itself, prove the correctness of the full
system, the quality of domain policies, or the safety of any deployment.
