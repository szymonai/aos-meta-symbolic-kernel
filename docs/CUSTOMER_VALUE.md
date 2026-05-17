# Customer Value

AOS is positioned as an explainable/verifiable AI control layer, not as a
replacement for domain models or human reviewers.

## Value In Regulated Or High-Risk Workflows

| Customer problem | AOS public demonstrator response |
| --- | --- |
| Model outputs are probabilistic | Add deterministic PASS/WARN/BLOCK control over output metadata |
| Teams need review triggers | Use WARN/BLOCK as explicit escalation signals |
| Audit trails are hard to reconstruct | Attach demo audit evidence to decisions |
| Policy language is ambiguous | Separate numeric gate behavior from prompt-only wording |
| Governance teams need boundaries | Distinguish model output, AOS decision, human decision, and claims |

The public value metrics are reported in [Value metrics](VALUE_METRICS.md).
They are limited to reproducible public artifacts such as benchmark JSON,
evidence manifests, tests, and clean-room repeatability.

## Radiology Triage Reference Value

In the radiology reference scenario, AOS is useful as a workflow-control pattern:

- allow low-risk outputs to continue to review
- warn when uncertainty or quality metadata is near a boundary
- block or hold outputs that exceed the control envelope
- preserve evidence that a control decision was made

This is customer value for governance and workflow assurance. It is not a claim
that the public repository is a clinical product.

The commercial value should be evaluated with controlled workflow evidence:
decision routing, audit completeness, reproducibility, integration fit, and
claim discipline. The public repository shows the evaluation shape without
publishing private evaluation material, implementation details, or customer
data.

## Specialist System Multiplier

The radiology scenario is also a concrete example of the wider commercial
pattern: a general AOS control layer can support multiple domain-specific
profiles. A radiology triage profile is one specialist instance; other
specialist systems could apply the same core separation of model output, control
decision, audit evidence, and human review.

The public repo demonstrates this product logic without exposing private
specialist-system material, restricted evidence packages, or implementation
details.
