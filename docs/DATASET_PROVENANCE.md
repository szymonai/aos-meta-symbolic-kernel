# Dataset Provenance

This repository does not redistribute domain datasets or dataset-specific
evidence. At this stage, public provenance is limited to a boundary statement.

No named dataset, cohort, split, sample count, local artifact, or domain metric
is published as current public evidence in this repository.

The controlled-study manifest is a protocol template only. It names suitable
public dataset families for future evaluation but does not redistribute their
records, labels, model outputs, or derived artifacts. Protocol evidence is not
an effectiveness claim unless the signal-normalization layer is independently
evaluated.

Frozen-output files should be generated outside the repository from public
datasets and stored only when their license permits publication. Each published
frozen record should include source dataset, split, source-record hash, model
id, model-output hash, category, difficulty class, and normalized AOS signals.

## Non-Redistribution

The public repository must not contain:

- personal, partner, or controlled records
- domain datasets
- dataset splits, labels, or per-case identifiers
- images, masks, segmentations, or derived domain artifacts
- model checkpoints
- local dataset paths
- internal audit logs
- controlled technical artifacts

The public evidence is intentionally limited to claim-boundary flags and
reproducible demonstrator artifacts.
