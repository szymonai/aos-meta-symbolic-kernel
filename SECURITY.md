# Security Policy

Report security issues privately to the maintainer.

Do not open public issues containing secrets, credentials, private datasets,
model weights, thresholds, calibration data, private audit records, deployment
details, or specialist-system information.

This repository is a limited demonstrator. It does not contain the production
AOS Core security architecture, key-management model, policy engine, audit
contract, adapter protocol, validation stack, or deployment design.

Production/commercial systems require separate security engineering, including:

- KMS-backed key handling
- key rotation and revocation
- ACLs and least privilege
- log retention and deletion policy
- incident response workflow
- supply-chain review
- secret scanning
- environment-specific policy review

Do not infer production security properties from this public demonstrator.
