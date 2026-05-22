from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SCENARIOS_PATH = ROOT / "scenarios.json"
RESULTS_DIR = ROOT / "results"
METRICS_PATH = RESULTS_DIR / "metrics.json"
SUMMARY_PATH = RESULTS_DIR / "summary.md"

AOS_WARN_MARGIN = 5.0
BENCHMARK_SCHEMA_VERSION = "synthetic-comparison/v1"
BENCHMARK_KIND = "synthetic_sanity_benchmark"

BASELINES = {
    "simple_threshold_guard": "benchmarks.baselines.simple_threshold_guard",
    "json_schema_guard": "benchmarks.baselines.json_schema_guard",
    "prompt_guardrail_sim": "benchmarks.baselines.prompt_guardrail_sim",
    "aos_gate_adapter": "benchmarks.baselines.aos_gate_adapter",
}

CLAIM_BOUNDARY = {
    "production_ready_claim": False,
    "external_validation_claim": False,
    "domain_validation_claim": False,
    "python_lean_refinement_claim": False,
    "external_framework_comparison_claim": False,
    "statistical_significance_claim": False,
}

USEFULNESS_VERIFICATION = {
    "useful_for": [
        "checking deterministic policy conformance",
        "checking replay stability",
        "checking public audit digest coverage",
        "explaining evidence boundaries to public reviewers",
    ],
    "not_useful_for": [
        "production readiness",
        "domain validation",
        "external framework ranking",
        "statistical significance",
        "regulated-use safety",
    ],
    "requires_clean_room_reproduction": True,
}


def load_scenarios() -> list[dict[str, Any]]:
    with SCENARIOS_PATH.open(encoding="utf-8") as file:
        scenarios = json.load(file)
    if not isinstance(scenarios, list):
        raise ValueError("scenarios.json must contain a list")
    return scenarios


def is_false_pass(expected: str, observed: str) -> bool:
    return expected == "BLOCK" and observed != "BLOCK"


def is_false_block(expected: str, observed: str) -> bool:
    return expected != "BLOCK" and observed == "BLOCK"


def safe_rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 6)


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def metrics_to_json(metrics: dict[str, Any]) -> str:
    return (
        json.dumps(
            metrics,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    )


def evaluate_guard(
    name: str,
    module_path: str,
    scenarios: list[dict[str, Any]],
) -> dict[str, Any]:
    module = importlib.import_module(module_path)
    decisions: list[dict[str, Any]] = []

    for scenario in scenarios:
        result = module.evaluate(scenario)
        verdict = result["verdict"]
        decisions.append(
            {
                "id": scenario["id"],
                "expected": scenario["expected_aos_verdict"],
                "verdict": verdict,
                "audit_digest": result.get("audit_digest"),
            }
        )

    replay_decisions: list[dict[str, Any]] = []
    for scenario in scenarios:
        result = module.evaluate(scenario)
        replay_decisions.append(
            {
                "id": scenario["id"],
                "expected": scenario["expected_aos_verdict"],
                "verdict": result["verdict"],
                "audit_digest": result.get("audit_digest"),
            }
        )

    expected_pass = sum(item["expected"] == "PASS" for item in decisions)
    expected_warn = sum(item["expected"] == "WARN" for item in decisions)
    expected_block = sum(item["expected"] == "BLOCK" for item in decisions)
    expected_non_block = expected_pass + expected_warn
    false_pass = sum(
        is_false_pass(item["expected"], item["verdict"]) for item in decisions
    )
    false_block = sum(
        is_false_block(item["expected"], item["verdict"]) for item in decisions
    )
    exact_match = sum(item["expected"] == item["verdict"] for item in decisions)
    unsafe_block = sum(
        item["expected"] == "BLOCK" and item["verdict"] == "BLOCK" for item in decisions
    )
    safe_pass = sum(
        item["expected"] == "PASS" and item["verdict"] == "PASS" for item in decisions
    )
    warning_preserved = sum(
        item["expected"] == "WARN" and item["verdict"] == "WARN" for item in decisions
    )
    audit_record_present = sum(
        isinstance(item["audit_digest"], str) and bool(item["audit_digest"])
        for item in decisions
    )

    return {
        "name": name,
        "expected_pass_count": expected_pass,
        "expected_warn_count": expected_warn,
        "expected_block_count": expected_block,
        "false_pass": false_pass,
        "false_block": false_block,
        "false_negative_unsafe_not_blocked": false_pass,
        "false_positive_block": false_block,
        "exact_match_count": exact_match,
        "exact_match_rate": safe_rate(exact_match, len(decisions)),
        "unsafe_block_rate": safe_rate(unsafe_block, expected_block),
        "critical_false_pass_rate": safe_rate(false_pass, expected_block),
        "false_positive_block_rate": safe_rate(false_block, expected_non_block),
        "safe_pass_rate": safe_rate(safe_pass, expected_pass),
        "warning_preservation_rate": safe_rate(warning_preserved, expected_warn),
        "pass_count": sum(item["verdict"] == "PASS" for item in decisions),
        "warn_count": sum(item["verdict"] == "WARN" for item in decisions),
        "block_count": sum(item["verdict"] == "BLOCK" for item in decisions),
        "audit_record_present": audit_record_present,
        "audit_coverage_rate": safe_rate(audit_record_present, len(decisions)),
        "deterministic_replay_passed": decisions == replay_decisions,
        "decisions": decisions,
    }


def build_summary(metrics: dict[str, Any]) -> str:
    metadata = metrics["benchmark_metadata"]
    usefulness = metrics["usefulness_verification"]
    rows = [
        (
            "| Guard | False pass | False block | Exact match | Unsafe block rate | "
            "False positive block rate | Audit coverage | Replay |"
        ),
        ("| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |"),
    ]
    for guard in metrics["guards"]:
        rows.append(
            "| {name} | {false_pass} | {false_block} | {exact_match_rate:.2%} | "
            "{unsafe_block_rate:.2%} | {false_positive_block_rate:.2%} | "
            "{audit_coverage_rate:.2%} | "
            "{deterministic_replay_passed} |".format(**guard)
        )

    verdict_rows = [
        "| Guard | PASS | WARN | BLOCK | Audit records |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for guard in metrics["guards"]:
        verdict_rows.append(
            "| {name} | {pass_count} | {warn_count} | {block_count} | "
            "{audit_record_present} |".format(**guard)
        )

    return "\n".join(
        [
            "# Synthetic Demonstrator Comparison Summary",
            "",
            "This benchmark compares deterministic interval gating with three simple",
            "guardrail baselines on synthetic scenarios. It is not a production",
            "benchmark, external validation, or domain validation claim.",
            "",
            "Scope limits: the scenario set has 12 synthetic cases, the baselines",
            "are intentionally simple, no external guardrail frameworks are",
            "included, and no statistical significance claim is made.",
            "",
            "Usefulness:",
            "",
            f"- benchmark kind: `{metadata['benchmark_kind']}`",
            f"- primary use: `{metadata['primary_use']}`",
            f"- scenario canonical SHA-256: `{metadata['scenario_canonical_sha256']}`",
            "",
            "Useful for:",
            "",
            *(f"- `{item}`" for item in usefulness["useful_for"]),
            "",
            "Not useful for:",
            "",
            *(f"- `{item}`" for item in usefulness["not_useful_for"]),
            "",
            *rows,
            "",
            "Verdict distribution:",
            "",
            *verdict_rows,
            "",
            "Interpretation:",
            "",
            "- `false_pass` means a synthetic unsafe scenario was not blocked. In a",
            "  safety-control reading, this is the critical false negative.",
            "- `false_block` means a synthetic PASS or WARN scenario was blocked. In a",
            "  safety-control reading, this is the false positive / false alarm.",
            "- `unsafe_block_rate` is the share of synthetic unsafe cases that were",
            "  correctly blocked.",
            "- `exact_match_rate` is the share of scenarios where the observed verdict",
            "  exactly matches the expected PASS / WARN / BLOCK label.",
            "- `audit_record_present` counts decisions that include an audit digest.",
            "- `audit_coverage_rate` is the share of decisions with an audit digest.",
            "- `deterministic_replay_passed` means rerunning the same guard on the",
            "  same scenarios produced identical decisions and audit digests.",
            "",
            "The public AOS demo gate is expected to block all synthetic unsafe",
            "cases because it evaluates `value + uncertainty` against the limit.",
        ]
    )


def build_metrics(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": BENCHMARK_SCHEMA_VERSION,
        "benchmark_metadata": {
            "benchmark_kind": BENCHMARK_KIND,
            "primary_use": "policy_conformance_and_replay_check",
            "scenario_source": "benchmarks/scenarios.json",
            "scenario_canonical_sha256": canonical_json_sha256(scenarios),
            "policy_under_test": (
                "upper_bound = value + uncertainty; "
                "PASS/WARN/BLOCK with warning band"
            ),
            "aos_warn_margin": AOS_WARN_MARGIN,
            "result_artifacts": [
                "benchmarks/results/metrics.json",
                "benchmarks/results/summary.md",
            ],
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "usefulness_verification": USEFULNESS_VERIFICATION,
        "scenario_count": len(scenarios),
        "scenario_mix": {
            "safe": sum(scenario["risk_label"] == "safe" for scenario in scenarios),
            "warning": sum(
                scenario["risk_label"] == "warning" for scenario in scenarios
            ),
            "unsafe": sum(scenario["risk_label"] == "unsafe" for scenario in scenarios),
        },
        "guards": [
            evaluate_guard(name, module_path, scenarios)
            for name, module_path in BASELINES.items()
        ],
    }


def run(*, write: bool = True) -> dict[str, Any]:
    scenarios = load_scenarios()
    metrics = build_metrics(scenarios)

    if not write:
        return metrics

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(metrics_to_json(metrics), encoding="utf-8")
    SUMMARY_PATH.write_text(build_summary(metrics) + "\n", encoding="utf-8")
    return metrics


def check_committed_results() -> None:
    metrics = run(write=False)
    expected = {
        METRICS_PATH: metrics_to_json(metrics),
        SUMMARY_PATH: build_summary(metrics) + "\n",
    }
    mismatches = [
        path
        for path, expected_content in expected.items()
        if path.read_text(encoding="utf-8") != expected_content
    ]
    if mismatches:
        files = ", ".join(str(path.relative_to(REPO_ROOT)) for path in mismatches)
        raise SystemExit(
            "Benchmark result drift detected in "
            f"{files}. Run `python benchmarks/run_benchmarks.py` "
            "and commit the updated artifacts."
        )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed benchmark artifacts match generated output",
    )
    args = parser.parse_args(argv)

    if args.check:
        check_committed_results()
        return

    run()


if __name__ == "__main__":
    main()
