from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmarks import run_e3_controlled_study  # noqa: E402

SCHEMA_VERSION = "aos-frozen-public-output/v1"
REQUIRED_METRICS = sorted(run_e3_controlled_study.REQUIRED_METRICS)


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{path} must contain JSON objects")
    return rows


def load_sources(path: Path) -> dict[str, dict[str, Any]]:
    rows = load_jsonl(path)
    return {str(row["source_id"]): row for row in rows}


def difficulty_for(labels: list[dict[str, Any]]) -> str:
    if not labels:
        return "D1"
    if len(labels) == 1:
        return "D3"
    return "D4"


def category_for(labels: list[dict[str, Any]]) -> str:
    return "UNSUPPORTED" if labels else "SUPPORTED"


def source_coverage_for(labels: list[dict[str, Any]]) -> float:
    return 1.0 if not labels else 0.5


def normalize_record(
    response: dict[str, Any],
    source: dict[str, Any] | None,
) -> dict[str, Any]:
    labels = response.get("labels") or []
    if not isinstance(labels, list):
        raise ValueError(f"RAGTruth response {response.get('id')} has invalid labels")

    category = category_for(labels)
    model_output = str(response["response"])
    source_payload = {"response": response, "source_info": source}
    unsupported_count = len(labels)
    return {
        "id": f"ragtruth-{response['id']}",
        "freeze_schema_version": SCHEMA_VERSION,
        "source_dataset": "RAGTruth",
        "source_split": str(response["split"]),
        "source_record_sha256": canonical_json_sha256(source_payload),
        "source_id": str(response["source_id"]),
        "model_id": str(response["model"]),
        "model_output": model_output,
        "model_output_sha256": text_sha256(model_output),
        "category": category,
        "difficulty_class": difficulty_for(labels),
        "expected_aos_verdict": "BLOCK" if category == "UNSUPPORTED" else "PASS",
        "required_citation_count": 1,
        "provided_citation_count": 1,
        "source_coverage": source_coverage_for(labels),
        "unsupported_claim_count": unsupported_count,
        "policy_violation_count": 0,
        "unsafe_action_count": 0,
        "prompt": "" if source is None else str(source.get("prompt", "")),
        "reference_evidence": [] if source is None else [source.get("source_info")],
        "ragtruth_quality": response.get("quality"),
        "ragtruth_temperature": response.get("temperature"),
        "ragtruth_task_type": None if source is None else source.get("task_type"),
        "ragtruth_label_count": unsupported_count,
    }


def build_records(
    responses: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    *,
    split: str | None = "test",
    quality: str | None = "good",
    max_records: int | None = None,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for response in responses:
        if split is not None and response.get("split") != split:
            continue
        if quality is not None and response.get("quality") != quality:
            continue
        source = sources.get(str(response["source_id"]))
        records.append(normalize_record(response, source))
        if max_records is not None and len(records) >= max_records:
            break
    return records


def records_to_jsonl(records: list[dict[str, Any]]) -> str:
    return "\n".join(
        json.dumps(record, allow_nan=False, separators=(",", ":"), sort_keys=True)
        for record in records
    ) + "\n"


def build_manifest(records: list[dict[str, Any]]) -> dict[str, Any]:
    prompt_digest = canonical_json_sha256(
        sorted({str(record.get("prompt", "")) for record in records})
    )
    model_count = len({str(record["model_id"]) for record in records})
    return {
        "study_id": "ragtruth-hallucination-text-e3",
        "evaluation_profile": "hallucination_text",
        "frozen_model_outputs": True,
        "dataset_sources": [
            {
                "name": "RAGTruth",
                "url": "https://github.com/ParticleMedia/RAGTruth",
                "license": "MIT",
                "use": "RAG hallucination and grounding cases",
                "e3_status": "near_direct_frozen_outputs",
            }
        ],
        "output_generation": {
            "mode": "public_frozen_outputs",
            "model_id": f"per-record ({model_count} models)",
            "prompt_template_sha256": prompt_digest,
            "temperature": "per-record",
            "top_p": None,
        },
        "comparators": [
            {"name": "llm_only", "version": "local"},
            {"name": "citation_presence_guard", "version": "local"},
            {"name": "prompt_guardrail_sim", "version": "local"},
            {"name": "aos_evidence_gate", "version": "local"},
        ],
        "predefined_metrics": REQUIRED_METRICS,
        "labeling_protocol": (
            "RAGTruth records with empty hallucination labels are SUPPORTED; "
            "records with one or more hallucination labels are UNSUPPORTED. "
            "Difficulty classes are mapped from label multiplicity: D1 for "
            "empty labels, D3 for one labeled unsupported span, D4 for multiple "
            "labeled unsupported spans."
        ),
        "case_level_results": True,
        "claim_boundary": (
            "Controlled hallucination_text profile over public frozen RAGTruth "
            "outputs; no production-readiness, full-stack, or external "
            "replication claim."
        ),
    }


def run(
    *,
    response_path: Path,
    source_info_path: Path,
    output_path: Path,
    manifest_output_path: Path | None = None,
    split: str | None = "test",
    quality: str | None = "good",
    max_records: int | None = None,
    write: bool = True,
) -> list[dict[str, Any]]:
    responses = load_jsonl(response_path)
    sources = load_sources(source_info_path)
    records = build_records(
        responses,
        sources,
        split=split,
        quality=quality,
        max_records=max_records,
    )
    if write:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(records_to_jsonl(records), encoding="utf-8")
        if manifest_output_path is not None:
            manifest_output_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_output_path.write_text(
                json.dumps(
                    build_manifest(records),
                    allow_nan=False,
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--response", required=True, type=Path)
    parser.add_argument("--source-info", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--split", default="test")
    parser.add_argument("--quality", default="good")
    parser.add_argument("--max-records", type=int)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    split = None if args.split.lower() == "all" else args.split
    quality = None if args.quality.lower() == "all" else args.quality
    records = run(
        response_path=args.response,
        source_info_path=args.source_info,
        output_path=args.output,
        manifest_output_path=args.manifest_output,
        split=split,
        quality=quality,
        max_records=args.max_records,
        write=not args.check,
    )
    if args.check and args.output.read_text(encoding="utf-8") != records_to_jsonl(
        records
    ):
        raise SystemExit(f"{args.output} is not up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
