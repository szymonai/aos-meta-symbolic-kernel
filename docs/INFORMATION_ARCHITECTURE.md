# Information Architecture

The public repository should be dense, legible, and restrained. Its purpose is
to communicate the technical thesis clearly without expanding beyond evidence
that the demonstrator can support.

## Editorial Principles

- Prefer high-signal artifacts over broad narration.
- Put the strongest technical claims next to their evidence and limitations.
- Keep public scope boundaries explicit and repeated at decision points.
- Use compact tables for layer maps, claim boundaries, and evidence status.
- Use code and tests as primary evidence where possible.
- Avoid marketing adjectives when a measurable property can be shown instead.
- Avoid named competitive comparisons in public materials; quality should be
  shown through evidence, tests, and bounded claims.
- Avoid hiding limitations; bounded claims are more credible than overreach.

## Simplification Rule

A public simplification is acceptable when it:

- preserves the architecture's public control shape;
- can be executed, tested, or inspected;
- reduces cognitive load for reviewers;
- stays within the approved public disclosure boundary;
- does not imply production, clinical, regulatory, or SOTA status.

A simplification is not acceptable when it:

- changes the meaning of the public control pattern;
- creates an unsupported product claim;
- makes the production system look like a thin wrapper around the demo;
- exposes implementation-specific or disclosure-sensitive detail.

## Sensitive Language Rule

Specialized terminology should be used only when it is necessary to explain
public evidence. Public text should not introduce terminology that implies
undisclosed capability; it should either provide bounded evidence or omit the
term.

## Information Density Pattern

Each major public artifact should answer four questions quickly:

1. What does this demonstrate?
2. What evidence supports it?
3. What is outside the public scope?
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
| `docs/ABSTRACTION_MAP.md` | Layered public map without production internals |
| `docs/IP_PROTECTION.md` | Publication and rights boundary |
| `docs/PUBLICATION_CHECKLIST.md` | Pre-publication review process |
| `docs/EXTERNAL_EVALUATION.md` | Controlled external review pathway |

## Review Standard

A change improves the repository when it increases one of these without reducing
another:

- technical clarity;
- evidence traceability;
- public-scope separation;
- claim discipline;
- reviewer confidence;
- IP protection.
