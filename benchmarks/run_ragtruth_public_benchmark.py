from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmarks import run_controlled_study  # noqa: E402

DATASET_VIEWER_BASE_URL = "https://datasets-server.huggingface.co"
DEFAULT_DATASET = "leobianco/ragtruth"
DEFAULT_CONFIG = "default"
DEFAULT_SPLIT = "test"
DEFAULT_LIMIT = 600
DEFAULT_WARN_SOURCE_COVERAGE_THRESHOLD = 0.85
PAGE_SIZE = 100
SCHEMA_VERSION = "aos-frozen-public-output/v1"

RESULTS_DIR = ROOT / "results"
DEFAULT_FROZEN_OUTPUTS = RESULTS_DIR / "ragtruth_public_frozen_outputs.jsonl"
DEFAULT_MANIFEST = RESULTS_DIR / "ragtruth_public_manifest.json"
DEFAULT_METRICS = RESULTS_DIR / "ragtruth_public_metrics.json"
DEFAULT_SUMMARY = RESULTS_DIR / "ragtruth_public_summary.md"

TOKEN_RE = re.compile(r"[A-Za-z0-9]+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "with",
}


def load_json_url(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "aos-public-benchmark"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Dataset Viewer response is not an object: {url}")
    return payload


def rows_url(
    *,
    dataset: str,
    config: str,
    split: str,
    offset: int,
    length: int,
) -> str:
    query = urllib.parse.urlencode(
        {
            "dataset": dataset,
            "config": config,
            "split": split,
            "offset": offset,
            "length": length,
        }
    )
    return f"{DATASET_VIEWER_BASE_URL}/rows?{query}"


def fetch_rows(
    *,
    dataset: str,
    config: str,
    split: str,
    limit: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0
    while len(rows) < limit:
        length = min(PAGE_SIZE, limit - len(rows))
        payload = load_json_url(
            rows_url(
                dataset=dataset,
                config=config,
                split=split,
                offset=offset,
                length=length,
            )
        )
        page = payload.get("rows", [])
        if not isinstance(page, list) or not page:
            break
        for item in page:
            if not isinstance(item, dict) or not isinstance(item.get("row"), dict):
                raise ValueError("Dataset Viewer row payload has unexpected shape")
            rows.append(item["row"])
        offset += len(page)
        if len(page) < length:
            break
    return rows


def tokens(text: str) -> list[str]:
    return [
        token.casefold()
        for token in TOKEN_RE.findall(text)
        if len(token) > 2 and token.casefold() not in STOPWORDS
    ]


def sentence_support_ratio(sentence: str, source_tokens: set[str]) -> float:
    sentence_tokens = tokens(sentence)
    if not sentence_tokens:
        return 1.0
    supported = sum(token in source_tokens for token in sentence_tokens)
    return supported / len(sentence_tokens)


def text_support_signals(response: str, source_text: str) -> dict[str, int | float]:
    response_tokens = tokens(response)
    source_tokens = set(tokens(source_text))
    if not response_tokens or not source_tokens:
        return {"source_coverage": 0.0, "unsupported_claim_count": 1}

    supported = sum(token in source_tokens for token in response_tokens)
    source_coverage = supported / len(response_tokens)
    sentences = [part.strip() for part in SENTENCE_RE.split(response) if part.strip()]
    unsupported_sentences = sum(
        1
        for sentence in sentences
        if len(tokens(sentence)) >= 4
        and sentence_support_ratio(sentence, source_tokens) < 0.35
    )
    return {
        "source_coverage": round(source_coverage, 6),
        "unsupported_claim_count": unsupported_sentences,
    }


def canonical_record_sha256(value: Any) -> str:
    return run_controlled_study.base.canonical_json_sha256(value)


def label_count(row: dict[str, Any]) -> int:
    labels = row.get("labels", [])
    if not isinstance(labels, list):
        raise ValueError(f"RAGTruth row {row.get('id')} has invalid labels")
    return len(labels)


def category_for_ground_truth(row: dict[str, Any]) -> str:
    return "UNSUPPORTED" if label_count(row) else "SUPPORTED"


def difficulty_for_ground_truth(row: dict[str, Any]) -> str:
    labels = label_count(row)
    if labels == 0:
        return "D1"
    if labels == 1:
        return "D3"
    return "D4"


def normalize_row(
    row: dict[str, Any],
    *,
    warn_source_coverage_threshold: float = DEFAULT_WARN_SOURCE_COVERAGE_THRESHOLD,
) -> dict[str, Any]:
    response = str(row.get("response", ""))
    source_info = str(row.get("source_info", ""))
    prompt = str(row.get("prompt", ""))
    category = category_for_ground_truth(row)
    signals = text_support_signals(response, f"{prompt}\n{source_info}")
    model_output_sha256 = run_controlled_study.text_sha256(response)
    return {
        "id": f"ragtruth-{row.get('id')}",
        "freeze_schema_version": SCHEMA_VERSION,
        "source_dataset": "RAGTruth",
        "source_split": str(row.get("split", DEFAULT_SPLIT)),
        "source_record_sha256": canonical_record_sha256(row),
        "source_id": str(row.get("source_id", "")),
        "model_id": str(row.get("model", "unknown")),
        "model_output": response,
        "model_output_sha256": model_output_sha256,
        "category": category,
        "difficulty_class": difficulty_for_ground_truth(row),
        "expected_aos_verdict": "BLOCK" if category == "UNSUPPORTED" else "PASS",
        "required_citation_count": 1,
        "provided_citation_count": 1 if source_info.strip() else 0,
        "source_coverage": signals["source_coverage"],
        "unsupported_claim_count": signals["unsupported_claim_count"],
        "warn_source_coverage_threshold": warn_source_coverage_threshold,
        "policy_violation_count": 0,
        "unsafe_action_count": 0,
        "prompt": prompt,
        "reference_evidence": [source_info],
        "ragtruth_label_count": label_count(row),
        "ragtruth_quality": row.get("quality"),
        "ragtruth_task_type": row.get("task_type"),
        "signal_extraction": {
            "method": "lexical_source_overlap_v1",
            "labels_used_as_aos_signals": False,
        },
    }


def records_to_jsonl(records: list[dict[str, Any]]) -> str:
    return "\n".join(
        json.dumps(record, allow_nan=False, separators=(",", ":"), sort_keys=True)
        for record in records
    ) + "\n"


def select_records(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    normalized = [normalize_row(row) for row in rows]
    buckets = {"SUPPORTED": [], "UNSUPPORTED": []}
    for record in normalized:
        buckets[str(record["category"])].append(record)
    if not all(buckets.values()):
        return normalized[:limit]

    selected: list[dict[str, Any]] = []
    per_bucket = max(1, math.ceil(limit / len(buckets)))
    for bucket in buckets.values():
        selected.extend(bucket[:per_bucket])
    return selected[:limit]


def build_manifest(
    records: list[dict[str, Any]],
    *,
    dataset: str,
    config: str,
    split: str,
    fetched_rows: int,
    warn_source_coverage_threshold: float,
) -> dict[str, Any]:
    model_count = len({str(record["model_id"]) for record in records})
    return {
        "study_id": "ragtruth-public-frozen-output-benchmark",
        "evaluation_profile": "hallucination_text",
        "frozen_model_outputs": True,
        "dataset_sources": [
            {
                "name": "RAGTruth",
                "url": "https://github.com/ParticleMedia/RAGTruth",
                "mirror": f"https://huggingface.co/datasets/{dataset}",
                "license": "MIT / public Hugging Face mirror metadata",
                "use": "RAG hallucination and grounding benchmark",
                "controlled_study_status": "public_frozen_outputs",
            }
        ],
        "output_generation": {
            "mode": "public_dataset_viewer_fetch",
            "dataset": dataset,
            "config": config,
            "split": split,
            "fetched_rows": fetched_rows,
            "model_id": f"per-record ({model_count} models)",
            "prompt_template_sha256": canonical_record_sha256(
                sorted({str(record.get("prompt", "")) for record in records})
            ),
            "temperature": "per-record",
            "top_p": None,
        },
        "aos_policy": {
            "warn_source_coverage_threshold": warn_source_coverage_threshold,
            "optimization_target": (
                "reduce silent unsupported pass-through by routing low-coverage "
                "answers to WARN rather than PASS"
            ),
        },
        "effectiveness_design": {
            "normalized_signals_source": "independent_extractor",
            "labels_used_as_aos_signals": False,
            "normalization_layer_evaluated": True,
            "held_out_manual_audit_present": False,
            "baseline_inputs_matched": True,
            "failure_cases_reported": True,
            "tradeoff_metrics_reported": True,
        },
        "comparators": [
            {"name": "llm_only", "version": "local"},
            {"name": "citation_presence_guard", "version": "local"},
            {"name": "prompt_guardrail_sim", "version": "local"},
            {"name": "aos_evidence_gate", "version": "local"},
        ],
        "predefined_metrics": sorted(run_controlled_study.REQUIRED_METRICS),
        "labeling_protocol": (
            "RAGTruth labels are used only as ground-truth outcome labels for "
            "metrics. AOS input signals are produced by lexical_source_overlap_v1 "
            "from response/source text and do not consume hallucination labels."
        ),
        "case_level_results": True,
        "claim_boundary": (
            "Public RAGTruth diagnostic benchmark. This is not a "
            "production-readiness, external-validation, or general AOS "
            "effectiveness claim."
        ),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run(
    *,
    dataset: str,
    config: str,
    split: str,
    fetch_limit: int,
    benchmark_limit: int,
    frozen_output_path: Path,
    manifest_path: Path,
    metrics_path: Path,
    summary_path: Path,
    warn_source_coverage_threshold: float,
) -> dict[str, Any]:
    rows = fetch_rows(dataset=dataset, config=config, split=split, limit=fetch_limit)
    records = [
        {
            **record,
            "warn_source_coverage_threshold": warn_source_coverage_threshold,
        }
        for record in select_records(rows, benchmark_limit)
    ]
    manifest = build_manifest(
        records,
        dataset=dataset,
        config=config,
        split=split,
        fetched_rows=len(rows),
        warn_source_coverage_threshold=warn_source_coverage_threshold,
    )
    metrics = run_controlled_study.build_metrics(
        records,
        manifest,
        scenario_source=f"Hugging Face Dataset Viewer: {dataset}/{config}/{split}",
        result_prefix="ragtruth_public",
    )
    summary = run_controlled_study.build_summary(metrics)

    frozen_output_path.parent.mkdir(parents=True, exist_ok=True)
    frozen_output_path.write_text(records_to_jsonl(records), encoding="utf-8")
    write_json(manifest_path, manifest)
    write_json(metrics_path, metrics)
    summary_path.write_text(summary, encoding="utf-8")
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch a bounded RAGTruth slice through Hugging Face Dataset Viewer "
            "and run a diagnostic public-output benchmark."
        )
    )
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--split", default=DEFAULT_SPLIT)
    parser.add_argument("--fetch-limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--benchmark-limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--frozen-output", type=Path, default=DEFAULT_FROZEN_OUTPUTS)
    parser.add_argument("--manifest-output", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--metrics-output", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument(
        "--warn-source-coverage-threshold",
        type=float,
        default=DEFAULT_WARN_SOURCE_COVERAGE_THRESHOLD,
    )
    args = parser.parse_args()

    metrics = run(
        dataset=args.dataset,
        config=args.config,
        split=args.split,
        fetch_limit=args.fetch_limit,
        benchmark_limit=args.benchmark_limit,
        frozen_output_path=args.frozen_output,
        manifest_path=args.manifest_output,
        metrics_path=args.metrics_output,
        summary_path=args.summary_output,
        warn_source_coverage_threshold=args.warn_source_coverage_threshold,
    )
    aos = next(
        guard for guard in metrics["guards"] if guard["name"] == "aos_evidence_gate"
    )
    print(
        "RAGTruth diagnostic benchmark: "
        f"n={metrics['scenario_count']}, "
        f"unsupported_pass_rate={aos['unsupported_pass_rate']:.2%}, "
        f"false_block_rate={aos['false_block_rate']:.2%}, "
        f"audit_coverage_rate={aos['audit_coverage_rate']:.2%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
