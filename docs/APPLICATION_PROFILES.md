# Application Profiles

AOS is a domain-neutral runtime assurance layer. The public repository should
be read as one reusable control pattern, not as a set of released specialist
products.

The shared pattern is:

```text
AI output
  -> quality, uncertainty, or risk signal
  -> explicit policy
  -> AOS gate
  -> PASS / WARN / BLOCK
  -> replayable audit evidence
```

An application profile is appropriate when the workflow can expose bounded
signals, explicit policies, a deterministic verdict, and evidence that can be
replayed. The final business, operational, scientific, or clinical decision
remains outside the public demonstrator.

## Agent And Tool-Call Gate

Potential use: AI-agent actions, MCP tool calls, RAG workflows, code-assistant
actions, and enterprise copilots before execution or escalation.

Example public signals:

- tool-call risk tier
- policy match
- retrieval confidence
- source coverage
- semantic distance
- identity or sealed-state status

Not claimed: model correctness, hallucination elimination, autonomous-agent
safety, production security, or complete agent-system certification.

## Document And Workflow Review

Potential use: document AI, extraction pipelines, structured review queues,
approval workflows, and human-review triggers.

Example public signals:

- schema validity
- extraction confidence
- source coverage
- missing-field status
- policy match

Not claimed: legal correctness, compliance certification, final approval, or
replacement of expert review.

## Cybersecurity Automation Gate

Potential use: triage and approval control before automated security actions
are executed or escalated.

Example public signals:

- alert confidence
- action risk
- asset criticality
- blast-radius estimate
- policy match

Not claimed: complete threat detection, autonomous defense certification,
incident-response correctness, or production security readiness.

## Industrial And Physical-System Review

Potential use: engineering review, simulation-derived signals, industrial QA,
and operating-envelope checks before downstream workflow use.

Example public signals:

- operating-envelope limit
- mass-balance error
- energy drift
- temperature or pressure bound
- sensor uncertainty

Not claimed: replacement of numerical solvers, certified simulation tools,
engineering sign-off, or safety certification.

## Robotics And Edge Review

Potential use: uncertain perception, navigation, sensor, or actuator-risk
signals before physical action or escalation.

Example public signals:

- object confidence
- estimated distance
- sensor uncertainty
- collision margin
- navigation-zone status

Not claimed: autonomous safety certification, real-time control certification,
or certified robotics deployment.

## Scientific Research Pipeline Gate

Potential use: research artifacts, structural candidates, generated hypotheses,
or simulation candidates before downstream computational or laboratory work.

Example public signals:

- structural validity
- constraint violations
- provenance status
- candidate confidence
- reproducibility metadata

Not claimed: scientific discovery, biological activity, therapeutic validity,
wet-lab validation, or experimental success.

## Healthcare R&D And Radiology Reference

Potential use: healthcare research workflows and radiology reference scenarios
where model-output metadata can be routed to review or workflow hold.

Example public signals:

- output quality metadata
- uncertainty signal
- policy threshold
- review status
- audit evidence

Not claimed: clinical validation, diagnosis, treatment recommendation,
medical-device status, regulatory approval, or clinical deployment readiness.

The radiology reference profile in this repository should be understood as one
concrete instance of the general control pattern, not as the full specialist
system.

## Financial Workflow Review

Potential use: review queues where AI-generated risk signals are checked before
they affect an internal workflow.

Example public signals:

- risk score
- uncertainty margin
- policy limit
- identity status
- review trigger

Not claimed: final financial decision-making, compliance certification,
regulated approval, or automated approval authority.

## Reading These Profiles

These profiles explain where the AOS pattern can be evaluated. They do not
publish production integrations, customer-specific policies, controlled
evidence, deployment settings, or specialist-system implementation material.
