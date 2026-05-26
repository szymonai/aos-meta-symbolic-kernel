from __future__ import annotations

import json

from benchmarks import (
    freeze_public_outputs,
    freeze_ragtruth_outputs,
    generate_llm_assurance_hard_cases,
    run_e3_controlled_study,
    run_latency_benchmark,
    run_llm_assurance_benchmark,
    run_llm_hard_case_benchmark,
)
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


def test_latency_benchmark_reports_bounded_smoke_metrics() -> None:
    metrics = run_latency_benchmark.build_latency_metrics(iterations=2, warmup=1)
    parsed = json.loads(run_latency_benchmark.metrics_to_json(metrics))

    assert parsed["schema_version"] == "latency-smoke/v1"
    assert parsed["benchmark_metadata"]["benchmark_kind"] == (
        "local_latency_smoke_benchmark"
    )
    assert parsed["scenario_count"] == 12

    claim_boundary = parsed["claim_boundary"]
    assert claim_boundary["production_latency_claim"] is False
    assert claim_boundary["production_sla_claim"] is False
    assert claim_boundary["capacity_planning_claim"] is False

    usefulness = parsed["usefulness_verification"]
    assert "local micro-latency inspection" in usefulness["useful_for"]
    assert "production service-level agreement" in usefulness["not_useful_for"]

    guards = parsed["guards"]
    assert {guard["name"] for guard in guards} == {
        "simple_threshold_guard",
        "json_schema_guard",
        "prompt_guardrail_sim",
        "aos_gate_adapter",
    }
    for guard in guards:
        assert guard["sample_count"] == 24
        assert guard["iterations"] == 2
        assert guard["scenario_count"] == 12
        assert guard["median_us"] >= 0
        assert guard["p95_us"] >= 0
        assert guard["p99_us"] >= 0


def llm_guard_by_name(metrics: dict[str, object], name: str) -> dict[str, object]:
    guards = metrics["guards"]
    assert isinstance(guards, list)
    for guard in guards:
        assert isinstance(guard, dict)
        if guard["name"] == name:
            return guard
    raise AssertionError(f"missing LLM assurance guard metrics: {name}")


def test_llm_assurance_benchmark_reports_agent_and_llm_surfaces() -> None:
    metrics = run_llm_assurance_benchmark.run(write=False)
    parsed = json.loads(run_llm_assurance_benchmark.metrics_to_json(metrics))

    assert parsed["schema_version"] == "llm-assurance-offline/v1"
    assert parsed["scenario_count"] == 20
    assert parsed["scenario_mix"] == {
        "supported": 5,
        "insufficient_evidence": 5,
        "block_expected": 10,
    }

    metadata = parsed["benchmark_metadata"]
    assert metadata["benchmark_kind"] == "fixed_output_llm_assurance_smoke"
    assert metadata["evidence_level"] == "E1_FIXED_OUTPUT_OFFLINE_SMOKE"
    assert metadata["public_evidence_status"] == (
        "INSUFFICIENT_FOR_HIGH_QUALITY_PUBLIC_EFFECTIVENESS_PROOF"
    )
    assert metadata["claim_strength"] == "smoke_test_only"
    assert "fixed smoke benchmark" in metadata["candidate_technical_claim"]
    assert metadata["confidence_interval_method"] == "Wilson score interval, 95%"
    assert metadata["minimum_e3_upgrade"]["minimum_scenarios"] == 500
    assert metadata["minimum_e3_upgrade"]["target_evidence_level"] == (
        "E3_EFFECTIVENESS_READY_CONTROLLED_STUDY"
    )
    assert "independent_signal_extraction" in metadata["minimum_e3_upgrade"][
        "required_effectiveness_gates"
    ]
    required_difficulty = metadata["minimum_e3_upgrade"][
        "required_difficulty_classes"
    ]
    assert any("prompt-injection" in item for item in required_difficulty)
    assert any("conflicting policies" in item for item in required_difficulty)
    assert "unsupported LLM claims" in metadata["evaluation_surfaces"]
    assert "unsafe agent action proposals" in metadata["evaluation_surfaces"]

    evidence_density = parsed["evidence_density"]
    assert evidence_density["per_case_decision_records"] == 80
    assert evidence_density["scenario_difficulty_scope"] == "mostly D1-D2"
    assert evidence_density["confidence_intervals_included"] is True
    assert evidence_density["per_case_results_included"] is True

    assert "adversarial prompting" in parsed["known_unknowns"]
    assert "citation manipulation" in parsed["known_unknowns"]

    scalability = parsed["scalability_profile"]
    assert scalability["runner_complexity"] == (
        "O(number_of_scenarios * number_of_guards)"
    )

    claim_boundary = parsed["claim_boundary"]
    assert claim_boundary["live_llm_evaluation_claim"] is False
    assert claim_boundary["general_hallucination_rate_claim"] is False
    assert claim_boundary["external_guardrail_framework_comparison_claim"] is False
    assert claim_boundary["high_quality_public_effectiveness_proof_claim"] is False
    assert claim_boundary["public_effectiveness_proof_sufficient"] is False


def test_llm_assurance_aos_blocks_unsupported_policy_and_agent_risks() -> None:
    metrics = run_llm_assurance_benchmark.run(write=False)
    aos = llm_guard_by_name(metrics, "aos_evidence_gate")

    assert aos["unsupported_pass_rate"] == 0.0
    assert aos["unsupported_pass_rate_ci95"] == [0.0, 0.434482]
    assert aos["policy_violation_pass_rate"] == 0.0
    assert aos["unsafe_action_pass_rate"] == 0.0
    assert aos["block_recall"] == 1.0
    assert aos["block_recall_ci95"] == [0.722467, 1.0]
    assert aos["warn_yield"] == 1.0
    assert aos["false_block_rate"] == 0.0
    assert aos["audit_coverage_rate"] == 1.0
    assert aos["replay_success_rate"] == 1.0


def test_llm_assurance_artifacts_match_runner_output() -> None:
    metrics = run_llm_assurance_benchmark.run(write=False)

    assert run_llm_assurance_benchmark.METRICS_PATH.read_text(
        encoding="utf-8"
    ) == run_llm_assurance_benchmark.metrics_to_json(metrics)
    assert run_llm_assurance_benchmark.SUMMARY_PATH.read_text(
        encoding="utf-8"
    ) == run_llm_assurance_benchmark.build_summary(metrics) + "\n"


def test_llm_hard_case_benchmark_reports_e2_scale_and_difficulty() -> None:
    metrics = run_llm_hard_case_benchmark.run(write=False)
    parsed = json.loads(run_llm_hard_case_benchmark.metrics_to_json(metrics))

    assert parsed["scenario_count"] == 540
    assert parsed["benchmark_metadata"]["evidence_level"] == (
        "E2_FIXED_OUTPUT_HARD_CASE_BENCHMARK"
    )
    assert parsed["benchmark_metadata"]["public_evidence_status"] == (
        "INSUFFICIENT_FOR_HIGH_QUALITY_PUBLIC_EFFECTIVENESS_PROOF"
    )
    assert parsed["benchmark_metadata"]["claim_strength"] == (
        "synthetic_fixed_output_hard_case_only"
    )
    assert parsed["evidence_density"]["scenario_difficulty_scope"] == "D1-D9"
    assert parsed["evidence_density"]["difficulty_class_count"] == 9
    assert parsed["evidence_density"]["per_case_decision_records"] == 2160

    aos = llm_guard_by_name(metrics, "aos_evidence_gate")
    assert aos["unsupported_pass_rate"] == 0.0
    assert aos["policy_violation_pass_rate"] == 0.0
    assert aos["unsafe_action_pass_rate"] == 0.0
    assert aos["block_recall"] == 1.0
    assert aos["safe_pass_rate"] == 1.0
    assert aos["warn_yield"] == 1.0
    assert aos["false_block_rate"] == 0.0
    assert aos["audit_coverage_rate"] == 1.0


def test_llm_hard_case_artifacts_match_runner_output() -> None:
    metrics = run_llm_hard_case_benchmark.run(write=False)

    assert run_llm_hard_case_benchmark.METRICS_PATH.read_text(
        encoding="utf-8"
    ) == run_llm_hard_case_benchmark.metrics_to_json(metrics)
    assert run_llm_hard_case_benchmark.SUMMARY_PATH.read_text(
        encoding="utf-8"
    ) == run_llm_hard_case_benchmark.build_summary(metrics) + "\n"


def e3_fixture_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for record in generate_llm_assurance_hard_cases.build_scenarios():
        output = str(record["model_output"])
        records.append(
            {
                **record,
                "freeze_schema_version": "aos-frozen-public-output/v1",
                "source_dataset": "public-fixture",
                "source_split": "test",
                "source_record_sha256": run_e3_controlled_study.text_sha256(
                    record["id"]
                ),
                "model_id": "fixture-model-v1",
                "model_output_sha256": run_e3_controlled_study.text_sha256(output),
            }
        )
    return records


def e3_manifest(
    *,
    frozen: bool = True,
    effectiveness_ready: bool = False,
) -> dict[str, object]:
    if effectiveness_ready:
        effectiveness_design = {
            "normalized_signals_source": "independent_extractor",
            "labels_used_as_aos_signals": False,
            "normalization_layer_evaluated": True,
            "held_out_manual_audit_present": True,
            "baseline_inputs_matched": True,
            "failure_cases_reported": True,
            "tradeoff_metrics_reported": True,
        }
    else:
        effectiveness_design = {
            "normalized_signals_source": "dataset_label_mapping",
            "labels_used_as_aos_signals": True,
            "normalization_layer_evaluated": False,
            "held_out_manual_audit_present": False,
            "baseline_inputs_matched": True,
            "failure_cases_reported": False,
            "tradeoff_metrics_reported": True,
        }
    return {
        "study_id": "fixture-e3-study",
        "evaluation_profile": "full_stack",
        "frozen_model_outputs": frozen,
        "effectiveness_design": effectiveness_design,
        "dataset_sources": [
            {
                "name": "public-fixture",
                "url": "https://example.test/public-fixture",
                "license": "fixture",
            }
        ],
        "output_generation": {
            "model_id": "fixture-model-v1",
            "prompt_template_sha256": "0" * 64,
            "temperature": 0,
            "top_p": 1,
        },
        "labeling_protocol": "Fixture labels assigned before guard evaluation.",
        "comparators": [
            {"name": "llm_only", "version": "local"},
            {"name": "citation_presence_guard", "version": "local"},
            {"name": "prompt_guardrail_sim", "version": "local"},
            {"name": "aos_evidence_gate", "version": "local"},
        ],
        "predefined_metrics": sorted(run_e3_controlled_study.REQUIRED_METRICS),
    }


def test_e3_controlled_study_protocol_can_satisfy_e3_criteria() -> None:
    metrics = run_e3_controlled_study.build_metrics(
        e3_fixture_records(),
        e3_manifest(),
    )
    assessment = metrics["controlled_study_assessment"]

    assert metrics["schema_version"] == "llm-assurance-controlled-study/v1"
    assert metrics["benchmark_metadata"]["evidence_level"] == (
        "E3_PROTOCOL_ONLY_NO_EFFECTIVENESS_CLAIM"
    )
    assert metrics["benchmark_metadata"]["protocol_evidence_level"] == (
        "E3_PROTOCOL_CONTROLLED_REPRODUCIBLE_STUDY"
    )
    assert assessment["e3_criteria_satisfied"] is True
    assert assessment["protocol_e3_criteria_satisfied"] is True
    assert assessment["effectiveness_criteria_satisfied"] is False
    assert assessment["missing_criteria"] == []
    assert "labels_not_used_as_aos_signals" in assessment[
        "missing_effectiveness_criteria"
    ]
    assert "normalization_layer_evaluated" in assessment[
        "missing_effectiveness_criteria"
    ]
    assert assessment["criteria"]["minimum_500_cases"] is True
    assert assessment["criteria"]["required_difficulties_covered"] is True
    assert assessment["criteria"]["minimum_cases_per_category"] is True
    assert assessment["criteria"]["minimum_cases_per_difficulty"] is True
    assert assessment["criteria"]["output_generation_metadata_present"] is True
    assert assessment["criteria"]["source_record_hashes_present"] is True
    assert assessment["criteria"]["aos_audit_coverage"] is True


def test_e3_controlled_study_protocol_does_not_overclaim() -> None:
    records = e3_fixture_records()[:20]
    metrics = run_e3_controlled_study.build_metrics(
        records,
        e3_manifest(frozen=False),
    )
    assessment = metrics["controlled_study_assessment"]

    assert metrics["benchmark_metadata"]["evidence_level"] == (
        "E3_EFFECTIVENESS_NOT_READY"
    )
    assert metrics["benchmark_metadata"]["protocol_evidence_level"] == (
        "E3_PROTOCOL_RUN_NOT_E3"
    )
    assert assessment["e3_criteria_satisfied"] is False
    assert assessment["effectiveness_criteria_satisfied"] is False
    assert "minimum_500_cases" in assessment["missing_criteria"]
    assert "frozen_model_outputs" in assessment["missing_criteria"]
    assert "protocol_e3_criteria_satisfied" in assessment[
        "missing_effectiveness_criteria"
    ]


def test_e3_effectiveness_claim_requires_independent_normalization_design() -> None:
    metrics = run_e3_controlled_study.build_metrics(
        e3_fixture_records(),
        e3_manifest(effectiveness_ready=True),
    )
    assessment = metrics["controlled_study_assessment"]

    assert metrics["benchmark_metadata"]["evidence_level"] == (
        "E3_EFFECTIVENESS_READY_CONTROLLED_STUDY"
    )
    assert metrics["benchmark_metadata"]["protocol_evidence_level"] == (
        "E3_PROTOCOL_CONTROLLED_REPRODUCIBLE_STUDY"
    )
    assert assessment["protocol_e3_criteria_satisfied"] is True
    assert assessment["effectiveness_criteria_satisfied"] is True
    assert assessment["missing_effectiveness_criteria"] == []
    assert metrics["claim_boundary"]["e3_protocol_claim"] is True
    assert metrics["claim_boundary"]["e3_effectiveness_claim"] is True


def test_e3_text_profile_does_not_require_agent_categories() -> None:
    records: list[dict[str, object]] = []
    for difficulty in [f"D{index}" for index in range(1, 7)]:
        for category in ("SUPPORTED", "UNSUPPORTED"):
            for index in range(50):
                output = f"{category.lower()} output {difficulty} {index}"
                unsupported = 1 if category == "UNSUPPORTED" else 0
                records.append(
                    {
                        "id": f"text-{difficulty}-{category}-{index}",
                        "freeze_schema_version": "aos-frozen-public-output/v1",
                        "source_dataset": "public-text-fixture",
                        "source_split": "test",
                        "source_record_sha256": run_e3_controlled_study.text_sha256(
                            f"{difficulty}-{category}-{index}"
                        ),
                        "model_id": "fixture-model-v1",
                        "model_output": output,
                        "model_output_sha256": run_e3_controlled_study.text_sha256(
                            output
                        ),
                        "category": category,
                        "difficulty_class": difficulty,
                        "expected_aos_verdict": (
                            "BLOCK" if unsupported else "PASS"
                        ),
                        "policy_violation_count": 0,
                        "provided_citation_count": 1,
                        "required_citation_count": 1,
                        "source_coverage": 0.9,
                        "unsafe_action_count": 0,
                        "unsupported_claim_count": unsupported,
                    }
                )

    manifest = e3_manifest()
    manifest["evaluation_profile"] = "hallucination_text"
    metrics = run_e3_controlled_study.build_metrics(records, manifest)
    assessment = metrics["controlled_study_assessment"]

    assert metrics["benchmark_metadata"]["evidence_level"] == (
        "E3_PROTOCOL_ONLY_NO_EFFECTIVENESS_CLAIM"
    )
    assert assessment["effectiveness_criteria_satisfied"] is False
    assert assessment["evaluation_profile"] == "hallucination_text"
    assert assessment["required_categories"] == ["SUPPORTED", "UNSUPPORTED"]
    assert assessment["criteria"]["required_categories_covered"] is True
    assert assessment["criteria"]["required_difficulties_covered"] is True


def test_ragtruth_freezer_creates_text_profile_records() -> None:
    responses = [
        {
            "id": "1",
            "source_id": "s1",
            "model": "model-a",
            "temperature": 0.7,
            "labels": [],
            "split": "test",
            "quality": "good",
            "response": "Supported answer.",
        },
        {
            "id": "2",
            "source_id": "s1",
            "model": "model-a",
            "temperature": 0.7,
            "labels": [{"start": 0, "end": 5, "text": "False"}],
            "split": "test",
            "quality": "good",
            "response": "Unsupported answer.",
        },
        {
            "id": "3",
            "source_id": "s1",
            "model": "model-a",
            "temperature": 0.7,
            "labels": [
                {"start": 0, "end": 5, "text": "False"},
                {"start": 6, "end": 10, "text": "Also false"},
            ],
            "split": "test",
            "quality": "good",
            "response": "Multi unsupported answer.",
        },
    ]
    sources = {
        "s1": {
            "source_id": "s1",
            "task_type": "QA",
            "source_info": "Evidence packet.",
            "prompt": "Answer from evidence.",
        }
    }

    records = freeze_ragtruth_outputs.build_records(responses, sources)

    assert [record["category"] for record in records] == [
        "SUPPORTED",
        "UNSUPPORTED",
        "UNSUPPORTED",
    ]
    assert [record["difficulty_class"] for record in records] == ["D1", "D3", "D4"]
    assert records[0]["model_output_sha256"] == (
        freeze_ragtruth_outputs.text_sha256("Supported answer.")
    )
    assert records[1]["expected_aos_verdict"] == "BLOCK"


def test_freeze_public_outputs_creates_e3_compatible_records() -> None:
    row = {
        "id": "public-001",
        "model_output": "The claim is supported by the supplied evidence.",
        "category": "SUPPORTED",
        "difficulty_class": "D1",
        "policy_violation_count": 0,
        "provided_citation_count": 2,
        "required_citation_count": 2,
        "source_coverage": 0.91,
        "unsafe_action_count": 0,
        "unsupported_claim_count": 0,
        "prompt": "Answer from evidence only.",
        "reference_evidence": ["Evidence fragment."],
    }

    records = freeze_public_outputs.freeze_rows(
        [row],
        source_dataset="FEVER",
        source_split="test",
        model_id="fixture-model-v1",
    )

    assert records[0]["freeze_schema_version"] == "aos-frozen-public-output/v1"
    assert records[0]["source_dataset"] == "FEVER"
    assert records[0]["source_record_sha256"] == (
        freeze_public_outputs.canonical_json_sha256(row)
    )
    assert records[0]["model_output_sha256"] == (
        freeze_public_outputs.text_sha256(str(row["model_output"]))
    )
    assert records[0]["expected_aos_verdict"] == "PASS"
