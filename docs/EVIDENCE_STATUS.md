# Evidence Status

This repository currently publishes demonstrator evidence only.

| Evidence layer | Current status | Useful for | Not sufficient for |
| --- | --- | --- | --- |
| Fixed-output smoke | Included | runner correctness, audit digest coverage, replay checks | public effectiveness proof |
| Synthetic hard cases | Included | scale/difficulty sanity check over synthetic cases | real-world LLM or agent behavior |
| Controlled-study protocol | Runner included | checking frozen-output study completeness | effectiveness claim by itself |
| Controlled-study effectiveness | Not achieved | future high-quality public claim | current repository claims |
| External replication | Not achieved | independent validation | current repository claims |

Current public conclusion:

```text
The repository demonstrates a reproducible control pattern.
It does not yet provide high-quality public effectiveness evidence.
```

Smoke and hard-case result tables should be treated as appendices. They are
useful because they expose per-guard metrics, confidence intervals, audit
coverage, replay, and failure modes. They should not be used as the headline
proof.

A high-quality public effectiveness result requires:

- independent signal extraction;
- labels not used directly as AOS input signals;
- normalization-layer evaluation;
- held-out manual audit;
- matched comparator inputs;
- reported failures and false blocks;
- trade-off metrics;
- frozen outputs from public or named datasets;
- reproducible run commands and artifact hashes.
