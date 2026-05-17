# Repository Best Practices

This repository is maintained as a professional public demonstrator. The goal is
to be understandable, reproducible, evidence-led, and publication-safe without
exposing the private AOSKernel or restricted material.

## First-Read Clarity

The repository should explain the following within the first review pass:

- what AOS is;
- what AI problem it addresses;
- how `PASS` / `WARN` / `BLOCK` decisions work;
- how to run the public demonstrator;
- what public evidence supports the current claims;
- what is deliberately not included.

README should stay concise at the top. A plain-language explanation belongs in
`docs/PLAIN_LANGUAGE_OVERVIEW.md`; deeper technical material belongs in focused
documents under `docs/`.

## Evidence-First Documentation

Public claims should be tied to a visible evidence source:

- benchmark metrics should cite `benchmarks/results/metrics.json`;
- public boundary claims should cite `evidence/demonstrator_manifest.json`;
- radiology context should remain bounded by the evidence review files;
- integrity statements should follow `docs/INTEGRITY_ANCHORS.md`;
- proof statements should stay inside the scope defined in `SCOPE_OF_PROOF.md`.

Do not publish stale metrics, unsupported performance claims, or broad product
claims without a current, reproducible, public evidence packet.

## Repository Structure

| Area | Role |
| --- | --- |
| `README.md` | First-contact positioning, quickstart, public boundary |
| `docs/PLAIN_LANGUAGE_OVERVIEW.md` | Non-specialist explanation |
| `docs/SDK_BOUNDARY.md` | Public SDK/integration boundary |
| `core/` | Minimal executable public demonstrator |
| `benchmarks/` | Synthetic benchmark runner and public metrics |
| `lean/` | Abstract public proof surface |
| `evidence/` | Machine-readable evidence and claim boundaries |
| `examples/` | Small runnable public examples |
| `docs/` | Focused explanation, governance, value, and boundary documents |
| `tests/` | Functional, evidence, and publication-safety checks |
| `.github/` | CI, CODEOWNERS, and PR hygiene |

## Security And IP Hygiene

The repository must not include:

- secrets, credentials, tokens, private logs, or local paths;
- customer, partner, patient, or private dataset material;
- model weights, checkpoints, DICOM/NIfTI, masks, labels, ONNX, TensorRT,
  safetensors, PT/PTH, or similar artifacts;
- non-public decision parameters, restricted evidence packages, or private
  implementation material;
- production deployment settings, commercial delivery material, or private key
  material.

## CI And Verification Hygiene

CI should protect the public demonstrator by checking:

- linting;
- Python tests;
- benchmark generation and metrics JSON validity;
- evidence JSON validity;
- hello-world example execution;
- Lean placeholder scan;
- Lean build.

Local validation should use the same checks before publication.

## PR And Release Hygiene

Changes should be small, reviewable, and evidence-aware. Public change notes
should summarize:

- what changed;
- which files or public concepts are affected;
- what validation passed;
- which claims remain out of scope.

Avoid noisy change history, broad mixed-purpose edits, unsupported marketing
language, direct competitive scorecards, and disclosure-sensitive technical
detail.

## Audience Standard

The repository should be readable by:

- developers who want to run the demonstrator;
- GitHub readers who want to understand project scope quickly;
- academic reviewers who care about evidence boundaries;
- business or investor readers who need product logic without overclaims;
- technical enthusiasts who need a small runnable example.

Good public material increases clarity without increasing disclosure risk.
