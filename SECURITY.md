# Security Policy

Report security issues privately to the maintainer.

Do not open public issues, pull requests, discussions, comments, screenshots, or
logs containing secrets, credentials, private datasets, model weights,
thresholds, calibration data, private audit records, deployment details,
customer information, partner information, vulnerability exploit details, or
specialist-system information.

This repository is a limited demonstrator. It does not contain the production
AOS Core security architecture, key-management model, policy engine, audit
contract, adapter protocol, validation stack, commercial SDK, or deployment
design.

Security reports do not grant permission to copy, exploit, publish, disclose,
redistribute, commercialize, or derive products from AOS material. Coordinated
handling and written maintainer approval are required before any public
disclosure.

Production/commercial systems require separate security engineering, including:

- KMS-backed key handling
- key rotation and revocation
- ACLs and least privilege
- log retention and deletion policy
- incident response workflow
- supply-chain review
- secret scanning
- environment-specific policy review
- dependency and build provenance review
- private vulnerability intake and disclosure process

Do not infer production security properties from this public demonstrator.
