from __future__ import annotations

import json

from benchmarks.run_benchmarks import (
    METRICS_PATH,
    SUMMARY_PATH,
    build_summary,
    metrics_to_json,
    run,
)


def guard_by_name(metrics: dict[str, object], name: str) -> dict[str, object]:
    guards = metrics["guards"]
    assert isinstance(guards, list)
    for guard in guards:
        assert isinstance(guard, dict)
        if guard["name"] == name:
            return guard
    raise AssertionError(f"missing guard metrics: {name}")


def test_benchmark_runner_builds_valid_metrics_json() -> None:
    metrics = run(write=False)

    parsed = json.loads(metrics_to_json(metrics))

    assert parsed["schema_version"] == "synthetic-comparison/v1"
    assert parsed["scenario_count"] == 12
    assert metrics["scenario_mix"] == {"safe": 4, "warning": 4, "unsafe": 4}

    metadata = parsed["benchmark_metadata"]
    assert metadata["benchmark_kind"] == "synthetic_sanity_benchmark"
    assert metadata["primary_use"] == "policy_conformance_and_replay_check"
    assert len(metadata["scenario_canonical_sha256"]) == 64

    claim_boundary = parsed["claim_boundary"]
    assert claim_boundary["external_framework_comparison_claim"] is False
    assert claim_boundary["statistical_significance_claim"] is False

    usefulness = parsed["usefulness_verification"]
    assert "production readiness" in usefulness["not_useful_for"]


def test_committed_benchmark_artifacts_match_runner_output() -> None:
    metrics = run(write=False)

    assert METRICS_PATH.read_text(encoding="utf-8") == metrics_to_json(metrics)
    assert SUMMARY_PATH.read_text(encoding="utf-8") == build_summary(metrics) + "\n"


def test_aos_has_zero_false_passes_for_unsafe_cases() -> None:
    metrics = run(write=False)
    aos = guard_by_name(metrics, "aos_gate_adapter")

    assert aos["false_pass"] == 0
    assert aos["false_negative_unsafe_not_blocked"] == 0
    assert aos["critical_false_pass_rate"] == 0.0
    assert aos["unsafe_block_rate"] == 1.0
    assert aos["block_count"] == 4


def test_aos_has_no_false_positive_blocks() -> None:
    metrics = run(write=False)
    aos = guard_by_name(metrics, "aos_gate_adapter")

    assert aos["false_block"] == 0
    assert aos["false_positive_block"] == 0
    assert aos["false_positive_block_rate"] == 0.0


def test_aos_preserves_expected_public_verdicts() -> None:
    metrics = run(write=False)
    aos = guard_by_name(metrics, "aos_gate_adapter")

    assert aos["exact_match_count"] == 12
    assert aos["exact_match_rate"] == 1.0
    assert aos["safe_pass_rate"] == 1.0
    assert aos["warning_preservation_rate"] == 1.0


def test_baselines_have_expected_false_passes() -> None:
    metrics = run(write=False)
    simple = guard_by_name(metrics, "simple_threshold_guard")
    prompt = guard_by_name(metrics, "prompt_guardrail_sim")

    assert simple["false_pass"] >= 1
    assert prompt["false_pass"] >= 1


def test_every_aos_decision_has_audit_digest() -> None:
    metrics = run(write=False)
    aos = guard_by_name(metrics, "aos_gate_adapter")

    assert aos["audit_record_present"] == 12
    assert aos["audit_coverage_rate"] == 1.0
    assert aos["deterministic_replay_passed"] is True
