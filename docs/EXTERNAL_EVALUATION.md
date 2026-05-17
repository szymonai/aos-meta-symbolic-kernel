# External Evaluation Pathway

This repository is designed to support serious external review while preserving
the approved public disclosure boundary. Evaluation should focus on observable
behavior, evidence discipline, reproducibility, and claim boundaries.

## Principles

- Evaluate the public demonstrator as a bounded artifact, not as the full
  commercial system.
- Prefer reviewer-reproducible tests, synthetic data, reviewer-owned data, and
  aggregate results.
- Use category-level baselines and task-specific acceptance criteria rather than
  named competitive comparisons.
- Publish only evidence that is cleared for public release.
- Keep production-system and customer-specific material outside the public
  repository.
- Separate model output, AOS decision, human decision, and product or regulatory
  claim.

## Evaluation Stages

| Stage | Reviewer access | What can be evaluated | Public boundary | Suitable outcome |
| --- | --- | --- | --- | --- |
| Public self-check | Public repository only | Tests, CI, synthetic benchmark, Lean proof surface, evidence manifests | Public demonstrator only | Technical credibility and boundary review |
| Clean-room technical review | Public repository in a fresh environment | Reproducibility, claim discipline, documentation density, publication safety | Material outside the approved public boundary | Independent public-repo review note |
| Black-box pilot | Controlled evaluation interface | Observable behavior, audit metadata, integration ergonomics, aggregate performance envelope | Public release only by agreement | Aggregate pilot metrics and failure analysis |
| Confidential evaluation | Written agreement | Domain fit, evidence workflow, operational fit, support requirements | Material not expressly included in the evaluation scope | Go/no-go for paid pilot or enterprise evaluation |
| Commercial pilot | Customer-specific agreement | Governance value, audit trail, support model, security posture, measurable acceptance criteria | Reusable core IP and non-customer materials | Revenue-stage pilot with controlled evidence |
| Regulated pathway | Separate quality and regulatory program | Risk management, intended use, clinical or safety evidence as applicable | Public demonstrator remains non-product | Formal regulatory strategy, if pursued |

## Evidence Packet Standard

A serious evaluation packet should include:

- repository commit SHA or controlled build identifier;
- evaluation scenario and intended non-production scope;
- dataset provenance or synthetic data-generation description;
- metrics and acceptance criteria defined before the run;
- aggregate results and failure cases;
- environment and dependency summary;
- list of public artifacts included in the packet;
- public integrity anchors when an evidence packet is released: SHA-256,
  SHA-512, and Ed25519 signature metadata;
- explicit claim boundary and reviewer limitations;
- maintainer approval for any public disclosure.

## Public-Repo Verification

A reviewer should be able to verify the public layer through:

- `python -m ruff check .`
- `python -m pytest tests -q`
- `python benchmarks/run_benchmarks.py`
- `python -m json.tool evidence/demonstrator_manifest.json`
- `python -m json.tool evidence/radiology_offline_evaluation.json`
- `python -m json.tool evidence/radiology_evidence_review.json`
- `lake build AOSPublicCore`

These checks verify the public demonstrator only. They do not validate the full
production system, production security, specialist workflows, clinical utility,
regulatory compliance, or commercial deployment readiness.

## Failure Handling

Failures should be recorded as engineering evidence, not hidden. For each failed
case, record:

- scenario identifier;
- expected behavior;
- observed behavior;
- affected public-demonstrator layer;
- whether the failure affects only the public demonstrator or a controlled pilot;
- remediation status.

Do not publish root-cause detail that falls outside the approved public boundary
or contains security-sensitive material.

## Business-Facing Success Criteria

A pilot is commercially useful when it shows one or more of the following without
creating unsupported claims:

- reduced unsafe or low-quality pass-through in a defined workflow;
- clearer human-review triggers;
- reproducible audit evidence;
- better separation between model behavior and operational decision-making;
- acceptable integration cost and aggregate performance envelope;
- a measurable path to paid deployment or deeper validation.

## Non-Goals

This pathway does not authorize publication of material outside the approved
public boundary, unsupported claims, customer information, security-sensitive
implementation details, or named competitive scorecards.
