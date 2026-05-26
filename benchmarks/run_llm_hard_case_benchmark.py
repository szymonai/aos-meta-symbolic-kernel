from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmarks import run_llm_assurance_benchmark as base  # noqa: E402

SCENARIOS_PATH = ROOT / "llm_assurance_hard_cases.json"
RESULTS_DIR = ROOT / "results"
METRICS_PATH = RESULTS_DIR / "llm_hard_case_metrics.json"
SUMMARY_PATH = RESULTS_DIR / "llm_hard_case_summary.md"


def load_scenarios() -> list[dict[str, Any]]:
    with SCENARIOS_PATH.open(encoding="utf-8") as file:
        scenarios = json.load(file)
    if not isinstance(scenarios, list):
        raise ValueError("llm_assurance_hard_cases.json must contain a list")
    return scenarios


def build_metrics(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = base.build_metrics(scenarios)
    metadata = metrics["benchmark_metadata"]
    metadata["benchmark_kind"] = "fixed_output_llm_agent_hard_case_benchmark"
    metadata["evidence_level"] = "E2_FIXED_OUTPUT_HARD_CASE_BENCHMARK"
    metadata["public_evidence_status"] = (
        "INSUFFICIENT_FOR_HIGH_QUALITY_PUBLIC_EFFECTIVENESS_PROOF"
    )
    metadata["claim_strength"] = "synthetic_fixed_output_hard_case_only"
    metadata["primary_use"] = "scaled_hard_case_policy_and_agent_gate_check"
    metadata["scenario_source"] = "benchmarks/llm_assurance_hard_cases.json"
    metadata["result_artifacts"] = [
        "benchmarks/results/llm_hard_case_metrics.json",
        "benchmarks/results/llm_hard_case_summary.md",
    ]
    return metrics


def metrics_to_json(metrics: dict[str, Any]) -> str:
    return base.metrics_to_json(metrics)


def build_summary(metrics: dict[str, Any]) -> str:
    return base.build_summary(metrics).replace(
        "# LLM Assurance Offline Benchmark Summary",
        "# LLM/Agent Hard-Case Benchmark Summary",
        1,
    )


def run(*, write: bool = True) -> dict[str, Any]:
    scenarios = load_scenarios()
    metrics = build_metrics(scenarios)
    if write:
        RESULTS_DIR.mkdir(exist_ok=True)
        METRICS_PATH.write_text(metrics_to_json(metrics), encoding="utf-8")
        SUMMARY_PATH.write_text(build_summary(metrics) + "\n", encoding="utf-8")
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    metrics = run(write=not args.check)
    if args.check:
        expected_metrics = metrics_to_json(metrics)
        expected_summary = build_summary(metrics) + "\n"
        if METRICS_PATH.read_text(encoding="utf-8") != expected_metrics:
            raise SystemExit("llm_hard_case_metrics.json is not up to date")
        if SUMMARY_PATH.read_text(encoding="utf-8") != expected_summary:
            raise SystemExit("llm_hard_case_summary.md is not up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
