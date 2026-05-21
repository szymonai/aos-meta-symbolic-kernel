# Integrity Anchors

This repository uses integrity language only for public evidence provenance. It
does not publish signing keys, certificate bundles, production signing
infrastructure, or deployment evidence packets.

## Public Convention

| Anchor | Public role |
| --- | --- |
| SHA-256 | Compatibility and quick evidence identification |
| SHA-512 | Audit-grade long-form payload verification |
| Ed25519 | Authenticity and provenance for signed evidence packets |

## How To Read Ed25519 Here

Ed25519 should be read as a signature scheme for cleared public evidence
packets. A valid signed packet can show that a specific manifest payload was
approved by the signing authority associated with the published public key.

The public repository currently contains SHA-linked demonstrator evidence and
metadata describing the recommended Ed25519 provenance layer. It does not
publish production signing key material or a production signature
scheme.

## Current Demonstrator Digest Boundary

The current public gate emits SHA-256 identifiers over canonical demonstrator
payloads. These identifiers support local replay checks: the same public input,
policy, and verdict should reproduce the same digest.

A SHA-256 demonstrator digest is not a signature, HMAC, append-only audit
ledger, key-management design, non-repudiation proof, or production security
control. Production auditability requires a separately designed evidence layer,
such as HMAC-backed records, signed packets, KMS-backed key handling, immutable
log storage, retention policy, and tamper-response procedures.

## Safe Publication Rule

When a future evidence packet is signed, publish only:

- the public evidence packet or manifest approved for release;
- the SHA-256 identifier for quick checking;
- the SHA-512 payload hash for audit-grade verification;
- the Ed25519 public key or key identifier;
- the Ed25519 signature;
- the signing date and scope boundary.

Do not publish signing key material, internal certificate chains, deployment
evidence, controlled logs, deployment settings, or implementation details outside
the public demonstrator.
