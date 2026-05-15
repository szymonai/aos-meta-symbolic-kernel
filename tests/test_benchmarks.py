from __future__ import annotations

import json

from benchmarks.run_benchmarks import METRICS_PATH, run


def guard_by_name(metrics: dict[str, object], name: str) -> dict[str, object]:
    guards = metrics["guards"]
    assert isinstance(guards, list)
    for guard in guards:
        assert isinstance(guard, dict)
        if guard["name"] == name:
            return guard
    raise AssertionError(f"missing guard metrics: {name}")


def test_benchmark_runner_writes_valid_metrics_json() -> None:
    metrics = run()

    with METRICS_PATH.open(encoding="utf-8") as file:
        parsed = json.load(file)

    assert parsed["schema_version"] == "synthetic-advantage/v1"
    assert parsed["scenario_count"] == 12
    assert metrics["scenario_mix"] == {"safe": 4, "warning": 4, "unsafe": 4}


def test_aos_has_zero_false_passes_for_unsafe_cases() -> None:
    metrics = run()
    aos = guard_by_name(metrics, "aos_gate_adapter")

    assert aos["false_pass"] == 0
    assert aos["block_count"] == 4


def test_baselines_have_expected_false_passes() -> None:
    metrics = run()
    simple = guard_by_name(metrics, "simple_threshold_guard")
    prompt = guard_by_name(metrics, "prompt_guardrail_sim")

    assert simple["false_pass"] >= 1
    assert prompt["false_pass"] >= 1


def test_every_aos_decision_has_audit_digest() -> None:
    metrics = run()
    aos = guard_by_name(metrics, "aos_gate_adapter")

    assert aos["audit_record_present"] == 12
    assert aos["deterministic_replay_passed"] is True
