# Information Architecture

The public repository should be dense, legible, and restrained. Its purpose is
to communicate the technical thesis clearly without publishing private IP or
making claims that the demonstrator cannot support.

## Editorial Principles

- Prefer high-signal artifacts over broad narration.
- Put the strongest technical claims next to their evidence and limitations.
- Keep public/private boundaries explicit and repeated at decision points.
- Use compact tables for layer maps, claim boundaries, and evidence status.
- Use code and tests as primary evidence where possible.
- Avoid marketing adjectives when a measurable property can be shown instead.
- Avoid hiding limitations; bounded claims are more credible than overreach.

## Simplification Rule

A public simplification is acceptable when it:

- preserves the architecture's control shape;
- can be executed, tested, or inspected;
- reduces cognitive load for reviewers;
- does not leak private thresholds, policies, adapters, calibration, or proof
  internals;
- does not imply production, clinical, regulatory, or SOTA status.

A simplification is not acceptable when it:

- changes the meaning of the control pattern;
- creates an unsupported product claim;
- makes the private system look like a thin wrapper around the demo;
- exposes implementation details that should remain trade secret or
  patent-sensitive.

## Information Density Pattern

Each major public artifact should answer four questions quickly:

1. What does this demonstrate?
2. What evidence supports it?
3. What is deliberately withheld?
4. What claim is not being made?

## Suggested Repository Roles

| Artifact | Role |
| --- | --- |
| `README.md` | Thesis, scope, boundary, reading path |
| `core/aos_public_core.py` | Minimal executable assurance primitive |
| `tests/` | Behavioral and publication-safety checks |
| `benchmarks/` | Synthetic comparison, not production benchmark |
| `lean/` | Abstract proof surface, not runtime refinement proof |
| `evidence/` | Machine-readable claim and evidence boundaries |
| `docs/ABSTRACTION_MAP.md` | Layered architecture without private internals |
| `docs/IP_PROTECTION.md` | Publication and rights boundary |
| `docs/PUBLICATION_CHECKLIST.md` | Pre-publication review process |

## Review Standard

A change improves the repository when it increases one of these without reducing
another:

- technical clarity;
- evidence traceability;
- public/private separation;
- claim discipline;
- reviewer confidence;
- IP protection.
