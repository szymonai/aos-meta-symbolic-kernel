# IP Protection Policy

This repository is a limited public demonstrator. It is published for controlled
technical inspection only. It is not an open-source release, not the full AOS
Core, and not a grant of rights to proprietary AOS technology.

This document is an operational publication policy, not legal advice. Final IP,
patent, trademark, licensing, assignment, and enforcement decisions require
qualified counsel.

## Rights Reserved

Copyright (c) 2026 Szymon Hetnar. All rights reserved.

Unless a separate written agreement signed by the copyright holder says
otherwise, no rights are granted to:

- copy, modify, distribute, sublicense, sell, host, or commercialize this code or
  documentation;
- create derivative works;
- incorporate this material into a product, service, dataset, model, benchmark,
  training corpus, or evaluation suite;
- use AOS names, marks, logos, positioning, or product names as a brand;
- use non-public AOS technical material, confidential technical documentation,
  reserved implementation detail, or commercially useful process material.

Viewing the repository, cloning it, opening an issue, or submitting a pull
request does not create an implied license.

## Public Demonstrator Boundary

The public repository may contain only:

- simplified PASS/WARN/BLOCK interval-gate code;
- synthetic scenarios and synthetic benchmark outputs;
- demo audit records and digest examples;
- abstract Lean verdict logic;
- high-level positioning documents;
- aggregate or bounded evidence summaries cleared for public release.

The public repository must not contain:

- private AOSKernel code;
- non-public implementation material;
- restricted evidence packages or internal technical documentation;
- specialist-system source code or artifacts;
- datasets, patient data, scans, masks, labels, DICOM, NIfTI, checkpoints,
  weights, ONNX, TensorRT engines, safetensors, or model binaries;
- private manifests, certificate bundles, private performance traces, or
  commercial delivery materials;
- secrets, credentials, local paths, private logs, customer data, or partner
  information.

## Disclosure Controls

Commercially sensitive material must remain outside this public repository and
under controlled access. Before any public disclosure, classify material into one
of these groups:

- `public-demonstrator`: safe to publish here;
- `private-source`: private repository or vault only;
- `restricted`: controlled access only;
- `review-required`: do not disclose publicly until the publication path is
  cleared;
- `quarantine-review`: non-authoritative generated or unsupported material.

Restricted material should be protected with access controls, audit history,
need-to-know permissions, private backups, confidentiality agreements where
appropriate, and written publication approval.

## Review-Required Material

Do not publish new technical implementation details that may require IP review
until there is a written decision to disclose them. Public disclosure can affect
rights and commercial strategy.

## Public Integrity Anchors

Public evidence packets should use a clear integrity convention:

- SHA-256 for compatibility and quick verification;
- SHA-512 for audit-grade long-form verification;
- Ed25519 signature metadata for authenticity and provenance.

Integrity anchors identify approved public evidence packets. They are not a
license grant, a substitute for the underlying evidence packet, or a disclosure
of non-public technical material.

## Trademarks And Naming

AOS-related names, product names, slogans, and positioning statements are not
licensed for third-party branding. Any public naming change should be checked for
conflicts and trademark strategy before broad launch.

## Contribution Policy

External contributions are not accepted unless the maintainer has approved them
in advance and any required contributor agreement, copyright assignment, or
inbound license is complete in writing.

Unsolicited pull requests may be closed without review. Contributors must not
submit confidential, employer-owned, customer-owned, third-party, medical,
regulated, or export-controlled material.

## Enforcement Record

For each public release or material PR, keep a record of:

- commit SHA and release date;
- files changed;
- publication-safety checks run;
- evidence and claim-boundary checks;
- approving person;
- known withheld private artifacts;
- whether patent/trademark review was required.
