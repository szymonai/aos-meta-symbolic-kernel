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
- use any patentable implementation detail, trade secret, know-how, architecture,
  calibration method, policy engine, validation stack, or optimization layer.

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

- full AOS Core code;
- private audit contract, schema, signing system, or evidence-store design;
- policy semantics, adapter protocol, or domain workflow internals;
- real thresholds, calibration values, calibration curves, or deployment
  settings;
- specialist-system source code or validation stack;
- datasets, patient data, scans, masks, labels, DICOM, NIfTI, checkpoints,
  weights, ONNX, TensorRT engines, safetensors, or model binaries;
- private proof artifacts, private manifests, certificate bundles, or internal
  formal-verification payloads;
- CUDA/PTX/C++/assembler optimization code, private benchmarks, latency traces,
  hardware-specific tuning, or commercial SDK/API material;
- secrets, credentials, local paths, private logs, customer data, or partner
  information.

## Trade Secret Controls

Commercially sensitive implementation details must remain outside this public
repository and under controlled access. Before any public disclosure, classify
material into one of these groups:

- `public-demonstrator`: safe to publish here;
- `private-source`: private repository or vault only;
- `trade-secret`: access-controlled vault only, with need-to-know access;
- `patent-review`: do not disclose publicly until counsel clears the filing
  strategy;
- `quarantine-review`: non-authoritative generated or unsupported material.

Trade-secret material should be protected with access controls, audit history,
need-to-know permissions, private backups, confidentiality agreements where
appropriate, and written publication approval.

## Patent-Sensitive Material

Do not publish new technical implementation details that may be patentable until
there is a written decision to disclose them. Public disclosure can affect patent
rights, especially outside jurisdictions with limited grace periods.

Patent-sensitive examples include:

- control-kernel internals beyond this simplified demonstrator;
- policy synthesis, adapter contracts, and assurance protocols;
- private calibration and validation methods;
- formal-to-runtime refinement methods;
- low-level optimization and hardware execution techniques;
- specialist profile construction methods.

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
