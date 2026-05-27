# Evidence Status

This repository currently publishes demonstrator evidence only.

| Evidence layer | Current status | Useful for | Not sufficient for |
| --- | --- | --- | --- |
| Fixed-output smoke | Included | runner correctness, audit digest coverage, replay checks | public effectiveness proof |
| Synthetic hard cases | Included | scale/difficulty sanity check over synthetic cases | real-world LLM or agent behavior |
| Controlled-study protocol | Runner included | checking frozen-output study completeness | effectiveness claim by itself |
| RAGTruth diagnostic runner | Included, generated artifacts ignored | testing signal-extractor limits on public data | current effectiveness evidence |
| Operational control replay | Included | production-relevant offline replay over public frozen traces | production deployment proof |
| Controlled-study effectiveness | Not achieved | future high-quality public claim | current repository claims |
| Lean proof surface | Included | selected abstract verdict invariants | runtime equivalence or effectiveness evidence |
| Repository integrity manifest | Included | checking selected artifact hashes and public path consistency | external validation or release signing |
| External replication | Not achieved | independent validation | current repository claims |

Current public conclusion:

```text
The repository demonstrates a reproducible control pattern and one
production-relevant offline replay over public frozen traces.
It does not provide production deployment proof or external validation.
```

Smoke and hard-case result tables should be treated as appendices. They are
useful because they expose per-guard metrics, confidence intervals, audit
coverage, replay, and failure modes. They should not be used as the headline
proof.

The operational control replay is the current strongest public effectiveness
artifact. It is stronger than synthetic smoke checks because it uses public
frozen operational traces and known anomaly windows. It remains bounded because
the signal extractor is deterministic and public, the dataset is external, and
the run is offline shadow-mode only.

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
