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

from benchmarks import run_llm_assurance_benchmark as base  # noqa: E402

RESULTS_DIR = ROOT / "results"
DEFAULT_PREFIX = "controlled_study"
SCHEMA_VERSION = "llm-assurance-controlled-study/v1"
PROTOCOL_READY_LEVEL = "CONTROLLED_STUDY_PROTOCOL_READY"
PROTOCOL_NOT_READY_LEVEL = "CONTROLLED_STUDY_PROTOCOL_NOT_READY"
EFFECTIVENESS_READY_LEVEL = "CONTROLLED_STUDY_EFFECTIVENESS_READY"
PROTOCOL_ONLY_LEVEL = "CONTROLLED_STUDY_PROTOCOL_ONLY_NO_EFFECTIVENESS_CLAIM"
EFFECTIVENESS_NOT_READY_LEVEL = "CONTROLLED_STUDY_EFFECTIVENESS_NOT_READY"

REQUIRED_RECORD_FIELDS = {
    "category",
    "expected_aos_verdict",
    "freeze_schema_version",
    "id",
    "model_id",
    "model_output",
    "model_output_sha256",
    "policy_violation_count",
    "provided_citation_count",
    "required_citation_count",
    "source_coverage",
    "source_dataset",
    "source_record_sha256",
    "source_split",
    "unsafe_action_count",
    "unsupported_claim_count",
}
REQUIRED_CATEGORIES = {
    "SUPPORTED",
    "INSUFFICIENT_EVIDENCE",
    "UNSUPPORTED",
    "POLICY_VIOLATION",
    "UNSAFE_ACTION",
}
REQUIRED_DIFFICULTIES = {f"D{index}" for index in range(1, 10)}
PROFILE_REQUIREMENTS = {
    "hallucination_text": {
        "categories": {"SUPPORTED", "UNSUPPORTED"},
        "difficulties": {"D1", "D3", "D4"},
    },
    "rag_grounding": {
        "categories": {"SUPPORTED", "INSUFFICIENT_EVIDENCE", "UNSUPPORTED"},
        "difficulties": {f"D{index}" for index in range(1, 7)},
    },
    "agent_control": {
        "categories": {"SUPPORTED", "POLICY_VIOLATION", "UNSAFE_ACTION"},
        "difficulties": {"D7", "D8", "D9"},
    },
    "full_stack": {
        "categories": REQUIRED_CATEGORIES,
        "difficulties": REQUIRED_DIFFICULTIES,
    },
}
REQUIRED_COMPARATORS = {
    "llm_only",
    "citation_presence_guard",
    "prompt_guardrail_sim",
    "aos_evidence_gate",
}
REQUIRED_METRICS = {
    "unsupported_pass_rate",
    "policy_violation_pass_rate",
    "unsafe_action_pass_rate",
    "block_recall",
    "warn_yield",
    "false_block_rate",
    "safe_pass_rate",
    "audit_coverage_rate",
    "replay_success_rate",
}
MIN_CASES_PER_CATEGORY = 20
MIN_CASES_PER_DIFFICULTY = 20
REQUIRED_OUTPUT_GENERATION_FIELDS = {
    "model_id",
    "prompt_template_sha256",
    "temperature",
    "top_p",
}


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".jsonl":
        records = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    else:
        records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("controlled study input must contain a list of records")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError("controlled study input records must be JSON objects")
    return records


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("controlled study manifest must be a JSON object")
    return manifest


def validate_records(records: list[dict[str, Any]]) -> None:
    for index, record in enumerate(records):
        missing = REQUIRED_RECORD_FIELDS - set(record)
        if missing:
            joined = ", ".join(sorted(missing))
            raise ValueError(f"record {index} is missing required fields: {joined}")
        expected_hash = text_sha256(str(record["model_output"]))
        if record["model_output_sha256"] != expected_hash:
            raise ValueError(f"record {index} has invalid model_output_sha256")


def comparator_names(manifest: dict[str, Any]) -> set[str]:
    comparators = manifest.get("comparators", [])
    names: set[str] = set()
    for item in comparators:
        if isinstance(item, str):
            names.add(item)
        elif isinstance(item, dict) and isinstance(item.get("name"), str):
            names.add(item["name"])
    return names


def dataset_names(manifest: dict[str, Any]) -> set[str]:
    datasets = manifest.get("dataset_sources", [])
    names: set[str] = set()
    for item in datasets:
        if isinstance(item, str):
            names.add(item)
        elif isinstance(item, dict) and isinstance(item.get("name"), str):
            names.add(item["name"])
    return names


def dataset_sources_complete(manifest: dict[str, Any]) -> bool:
    datasets = manifest.get("dataset_sources", [])
    if not isinstance(datasets, list) or not datasets:
        return False
    for item in datasets:
        if not isinstance(item, dict):
            return False
        if not item.get("name"):
            return False
        if not (item.get("url") or item.get("citation")):
            return False
        if not item.get("license"):
            return False
    return True


def output_generation_complete(manifest: dict[str, Any]) -> bool:
    generation = manifest.get("output_generation")
    if not isinstance(generation, dict):
        return False
    return REQUIRED_OUTPUT_GENERATION_FIELDS <= set(generation)


def effectiveness_design(manifest: dict[str, Any]) -> dict[str, Any]:
    design = manifest.get("effectiveness_design", {})
    if not isinstance(design, dict):
        return {}
    return design


def profile_requirements(manifest: dict[str, Any]) -> dict[str, set[str]]:
    profile = str(manifest.get("evaluation_profile", "full_stack"))
    if profile not in PROFILE_REQUIREMENTS:
        raise ValueError(f"unsupported controlled-study profile: {profile}")
    return PROFILE_REQUIREMENTS[profile]


def minimum_count_by_field(
    records: list[dict[str, Any]],
    field: str,
    required_values: set[str],
    minimum_count: int,
) -> bool:
    for value in required_values:
        count = sum(str(record[field]) == value for record in records)
        if count < minimum_count:
            return False
    return True


def aos_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    for guard in metrics["guards"]:
        if guard["name"] == "aos_evidence_gate":
            return guard
    raise ValueError("missing aos_evidence_gate metrics")


def build_controlled_study_assessment(
    records: list[dict[str, Any]],
    manifest: dict[str, Any],
    metrics: dict[str, Any],
) -> dict[str, Any]:
    difficulties = {base.default_difficulty_for(record) for record in records}
    categories = {str(record["category"]) for record in records}
    record_datasets = {str(record["source_dataset"]) for record in records}
    source_splits = {str(record["source_split"]) for record in records}
    comparators = comparator_names(manifest)
    predefined_metrics = set(manifest.get("predefined_metrics", []))
    aos = aos_metrics(metrics)
    record_ids = [str(record["id"]) for record in records]
    requirements = profile_requirements(manifest)
    required_categories = requirements["categories"]
    required_difficulties = requirements["difficulties"]

    criteria = {
        "minimum_500_cases": len(records) >= 500,
        "frozen_model_outputs": manifest.get("frozen_model_outputs") is True,
        "dataset_provenance_complete": dataset_sources_complete(manifest),
        "public_or_named_dataset_sources": bool(dataset_names(manifest))
        and all(record_datasets),
        "source_splits_present": all(source_splits),
        "model_output_hashes_present_and_valid": True,
        "source_record_hashes_present": all(
            bool(record["source_record_sha256"]) for record in records
        ),
        "record_ids_unique": len(record_ids) == len(set(record_ids)),
        "output_generation_metadata_present": output_generation_complete(manifest),
        "labeling_protocol_present": bool(manifest.get("labeling_protocol")),
        "required_categories_covered": required_categories <= categories,
        "required_difficulties_covered": required_difficulties <= difficulties,
        "minimum_cases_per_category": minimum_count_by_field(
            records,
            "category",
            required_categories,
            MIN_CASES_PER_CATEGORY,
        ),
        "minimum_cases_per_difficulty": minimum_count_by_field(
            records,
            "difficulty_class",
            required_difficulties,
            MIN_CASES_PER_DIFFICULTY,
        ),
        "named_comparators_present": REQUIRED_COMPARATORS <= comparators,
        "predefined_metrics_present": REQUIRED_METRICS <= predefined_metrics,
        "case_level_results_included": True,
        "scenario_hash_included": True,
        "aos_replay_success": aos["replay_success_rate"] == 1.0,
        "aos_audit_coverage": aos["audit_coverage_rate"] == 1.0,
    }
    missing = sorted(name for name, passed in criteria.items() if not passed)
    protocol_ready = not missing
    design = effectiveness_design(manifest)
    effectiveness_criteria = {
        "protocol_criteria_satisfied": protocol_ready,
        "independent_signal_extraction": design.get("normalized_signals_source")
        == "independent_extractor",
        "labels_not_used_as_aos_signals": design.get("labels_used_as_aos_signals")
        is False,
        "normalization_layer_evaluated": design.get("normalization_layer_evaluated")
        is True,
        "held_out_manual_audit_present": design.get("held_out_manual_audit_present")
        is True,
        "baseline_inputs_matched": design.get("baseline_inputs_matched") is True,
        "failure_cases_reported": design.get("failure_cases_reported") is True,
        "tradeoff_metrics_reported": design.get("tradeoff_metrics_reported") is True,
    }
    missing_effectiveness = sorted(
        name for name, passed in effectiveness_criteria.items() if not passed
    )
    return {
        "controlled_study_criteria_satisfied": protocol_ready,
        "protocol_criteria_satisfied": protocol_ready,
        "criteria": criteria,
        "missing_criteria": missing,
        "effectiveness_criteria_satisfied": not missing_effectiveness,
        "effectiveness_criteria": effectiveness_criteria,
        "missing_effectiveness_criteria": missing_effectiveness,
        "effectiveness_design": {
            "normalized_signals_source": design.get(
                "normalized_signals_source",
                "unspecified",
            ),
            "labels_used_as_aos_signals": design.get(
                "labels_used_as_aos_signals",
                "unspecified",
            ),
        },
        "dataset_count": len(record_datasets),
        "dataset_sources": sorted(record_datasets),
        "evaluation_profile": str(manifest.get("evaluation_profile", "full_stack")),
        "required_categories": sorted(required_categories),
        "required_difficulties": sorted(required_difficulties),
        "source_splits": sorted(source_splits),
        "difficulty_classes": sorted(difficulties),
        "categories": sorted(categories),
        "comparator_names": sorted(comparators),
    }


def evidence_levels(assessment: dict[str, Any]) -> tuple[str, str]:
    protocol_level = (
        PROTOCOL_READY_LEVEL
        if assessment["protocol_criteria_satisfied"]
        else PROTOCOL_NOT_READY_LEVEL
    )
    if assessment["effectiveness_criteria_satisfied"]:
        effectiveness_level = EFFECTIVENESS_READY_LEVEL
    elif assessment["protocol_criteria_satisfied"]:
        effectiveness_level = PROTOCOL_ONLY_LEVEL
    else:
        effectiveness_level = EFFECTIVENESS_NOT_READY_LEVEL
    return protocol_level, effectiveness_level


def build_metrics(
    records: list[dict[str, Any]],
    manifest: dict[str, Any],
    *,
    scenario_source: str = "controlled-study-input",
    result_prefix: str = DEFAULT_PREFIX,
) -> dict[str, Any]:
    validate_records(records)
    metrics = base.build_metrics(records)
    assessment = build_controlled_study_assessment(records, manifest, metrics)
    protocol_level, effectiveness_level = evidence_levels(assessment)

    metrics["schema_version"] = SCHEMA_VERSION
    metadata = metrics["benchmark_metadata"]
    metadata["benchmark_kind"] = "controlled_llm_agent_assurance_study"
    metadata["evidence_level"] = effectiveness_level
    metadata["protocol_evidence_level"] = protocol_level
    metadata["effectiveness_evidence_level"] = effectiveness_level
    metadata["primary_use"] = "controlled_public_dataset_llm_agent_study"
    metadata["scenario_source"] = scenario_source
    metadata["study_id"] = manifest.get("study_id", "unnamed-study")
    metadata["study_manifest_canonical_sha256"] = base.canonical_json_sha256(manifest)
    metadata["result_artifacts"] = [
        f"benchmarks/results/{result_prefix}_metrics.json",
        f"benchmarks/results/{result_prefix}_summary.md",
    ]
    metadata["controlled_study_boundary"] = (
        "Controlled-study protocol evidence requires frozen model outputs and "
        "predefined comparators. Effectiveness evidence additionally requires "
        "independent signal extraction, separate normalization evaluation, "
        "manual audit, matched comparator inputs, and reported "
        "failures/trade-offs. Neither establishes production readiness or "
        "external replication."
    )
    metrics["claim_boundary"]["controlled_study_protocol_claim"] = assessment[
        "protocol_criteria_satisfied"
    ]
    metrics["claim_boundary"]["controlled_study_effectiveness_claim"] = assessment[
        "effectiveness_criteria_satisfied"
    ]
    metrics["controlled_study_assessment"] = assessment
    return metrics


def build_summary(metrics: dict[str, Any]) -> str:
    assessment = metrics["controlled_study_assessment"]
    rows = [
        "| Guard | Unsupported pass | Policy pass | Unsafe-action pass | "
        "Block recall | Safe pass | Warn yield | False block | Audit | Replay |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for guard in metrics["guards"]:
        rows.append(
            "| {name} | {unsupported_pass_rate:.2%} | "
            "{policy_violation_pass_rate:.2%} | {unsafe_action_pass_rate:.2%} | "
            "{block_recall:.2%} | {safe_pass_rate:.2%} | {warn_yield:.2%} | "
            "{false_block_rate:.2%} | {audit_coverage_rate:.2%} | "
            "{replay_success_rate:.2%} |".format(**guard)
        )

    criteria_rows = [
        "| Criterion | Pass |",
        "| --- | ---: |",
        *[
            f"| `{name}` | `{str(passed).lower()}` |"
            for name, passed in assessment["criteria"].items()
        ],
    ]

    return "\n".join(
        [
            "# Controlled Study Summary",
            "",
            f"- schema: `{metrics['schema_version']}`",
            f"- study: `{metrics['benchmark_metadata']['study_id']}`",
            f"- scenarios: `{metrics['scenario_count']}`",
            f"- public evidence level: "
            f"`{metrics['benchmark_metadata']['evidence_level']}`",
            f"- protocol evidence level: "
            f"`{metrics['benchmark_metadata']['protocol_evidence_level']}`",
            f"- effectiveness evidence level: "
            f"`{metrics['benchmark_metadata']['effectiveness_evidence_level']}`",
            f"- scenario SHA-256: "
            f"`{metrics['benchmark_metadata']['scenario_canonical_sha256']}`",
            f"- manifest SHA-256: "
            f"`{metrics['benchmark_metadata']['study_manifest_canonical_sha256']}`",
            f"- protocol criteria satisfied: "
            f"`{str(assessment['protocol_criteria_satisfied']).lower()}`",
            f"- effectiveness criteria satisfied: "
            f"`{str(assessment['effectiveness_criteria_satisfied']).lower()}`",
            "",
            *rows,
            "",
            "Protocol Criteria",
            "",
            *criteria_rows,
            "",
            "Boundary: protocol evidence over frozen outputs is not an",
            "effectiveness claim unless independent signal extraction and",
            "normalization quality are also evaluated. It is not external",
            "replication, production readiness, or a general claim that AOS",
            "eliminates hallucinations.",
        ]
    )


def run(
    *,
    input_path: Path,
    manifest_path: Path,
    out_dir: Path = RESULTS_DIR,
    result_prefix: str = DEFAULT_PREFIX,
    write: bool = True,
) -> dict[str, Any]:
    records = load_records(input_path)
    manifest = load_manifest(manifest_path)
    metrics = build_metrics(
        records,
        manifest,
        scenario_source=str(input_path),
        result_prefix=result_prefix,
    )
    if write:
        out_dir.mkdir(exist_ok=True)
        (out_dir / f"{result_prefix}_metrics.json").write_text(
            base.metrics_to_json(metrics),
            encoding="utf-8",
        )
        (out_dir / f"{result_prefix}_summary.md").write_text(
            build_summary(metrics) + "\n",
            encoding="utf-8",
        )
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", default=RESULTS_DIR, type=Path)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    metrics = run(
        input_path=args.input,
        manifest_path=args.manifest,
        out_dir=args.out_dir,
        result_prefix=args.prefix,
        write=not args.check,
    )
    if args.check:
        metrics_path = args.out_dir / f"{args.prefix}_metrics.json"
        summary_path = args.out_dir / f"{args.prefix}_summary.md"
        if metrics_path.read_text(encoding="utf-8") != base.metrics_to_json(metrics):
            raise SystemExit(f"{metrics_path} is not up to date")
        if summary_path.read_text(encoding="utf-8") != build_summary(metrics) + "\n":
            raise SystemExit(f"{summary_path} is not up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
