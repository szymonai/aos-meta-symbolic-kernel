from __future__ import annotations

import json
from pathlib import Path

from benchmarks import (
    freeze_public_outputs,
    freeze_ragtruth_outputs,
    generate_llm_assurance_hard_cases,
    run_controlled_study,
    run_latency_benchmark,
    run_llm_assurance_benchmark,
    run_llm_hard_case_benchmark,
    run_operational_control_replay,
    run_ragtruth_public_benchmark,
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


def write_operational_replay_fixture() -> object:
    return (
        Path(__file__).parent
        / "fixtures"
        / "operational_control_replay"
        / "NAB"
    )


def operational_guard_by_name(
    metrics: dict[str, object],
    name: str,
) -> dict[str, object]:
    guards = metrics["guards"]
    assert isinstance(guards, list)
    for guard in guards:
        assert isinstance(guard, dict)
        if guard["name"] == name:
            return guard
    raise AssertionError(f"missing operational replay guard metrics: {name}")


def test_operational_control_replay_builds_fixture_metrics() -> None:
    nab_root = write_operational_replay_fixture()
    metrics = run_operational_control_replay.build_metrics(
        nab_root=nab_root,
        rolling_window=3,
        min_history=3,
    )
    parsed = json.loads(run_operational_control_replay.metrics_to_json(metrics))

    assert parsed["schema_version"] == "operational-control-replay/v1"
    assert parsed["series_count"] == 1
    assert parsed["anomaly_window_count"] == 1
    assert parsed["claim_boundary"]["production_deployment_claim"] is False
    assert parsed["benchmark_metadata"]["dataset_redistributed_in_repo"] is False
    assert parsed["production_relevance_profile"]["claim_type"] == (
        "production_relevant_offline_replay"
    )
    assert parsed["production_relevance_profile"][
        "labels_used_as_aos_input_signals"
    ] is False
    assert parsed["scalability_profile"]["gate_complexity_per_signal"] == "O(1)"
    assert parsed["auditability_profile"][
        "aos_audit_record_expected_per_evaluated_record"
    ] is True
    assert parsed["falsification_profile"]["check_command"] == (
        "python benchmarks/run_operational_control_replay.py --check"
    )

    pass_through = operational_guard_by_name(parsed, "pass_through_baseline")
    aos = operational_guard_by_name(parsed, "aos_control_gate")

    assert pass_through["anomaly_window_silent_pass_rate"] == 1.0
    assert aos["anomaly_window_review_or_block_rate"] == 1.0
    assert aos["audit_coverage_rate"] == 1.0
    assert aos["replay_success_rate"] == 1.0
    assert "offline shadow-mode" in run_operational_control_replay.build_summary(
        parsed
    )


def test_committed_operational_control_replay_artifacts_are_bounded() -> None:
    metrics_path = (
        run_operational_control_replay.RESULTS_DIR
        / "operational_control_replay_metrics.json"
    )
    summary_path = (
        run_operational_control_replay.RESULTS_DIR
        / "operational_control_replay_summary.md"
    )
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    summary = summary_path.read_text(encoding="utf-8")

    assert metrics["schema_version"] == "operational-control-replay/v1"
    assert metrics["benchmark_metadata"]["dataset"] == "Numenta Anomaly Benchmark"
    assert metrics["benchmark_metadata"]["dataset_redistributed_in_repo"] is False
    assert metrics["claim_boundary"]["production_deployment_claim"] is False
    assert metrics["claim_boundary"]["anomaly_detector_superiority_claim"] is False
    assert "not a production deployment proof" in summary
    assert "Production-Relevant Proof Profile" in summary
    assert "Falsification Criteria" in summary

    production_relevance = metrics["production_relevance_profile"]
    scalability = metrics["scalability_profile"]
    auditability = metrics["auditability_profile"]
    falsification = metrics["falsification_profile"]

    assert production_relevance["claim_type"] == "production_relevant_offline_replay"
    assert production_relevance["public_operational_data"] is True
    assert production_relevance["offline_shadow_mode"] is True
    assert production_relevance["labels_used_as_aos_input_signals"] is False
    assert scalability["evaluated_record_count"] == metrics["evaluated_record_count"]
    assert scalability["series_count"] == metrics["series_count"]
    assert scalability["gate_complexity_per_signal"] == "O(1)"
    assert auditability["aggregate_decision_stream_sha256"] == (
        metrics["aggregate_decision_stream_sha256"]
    )
    assert auditability["per_series_source_sha256"] is True
    assert "AOS replay success falls below 100%" in " ".join(
        falsification["falsification_conditions"]
    )

    aos = operational_guard_by_name(metrics, "aos_control_gate")
    block_only = operational_guard_by_name(metrics, "block_only_score_baseline")
    assert aos["anomaly_window_review_or_block_rate"] >= (
        block_only["anomaly_window_review_or_block_rate"]
    )
    assert aos["audit_coverage_rate"] == 1.0
    assert aos["replay_success_rate"] == 1.0


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
    assert metadata["evidence_level"] == "FIXED_OUTPUT_SMOKE"
    assert metadata["public_evidence_status"] == (
        "INSUFFICIENT_FOR_HIGH_QUALITY_PUBLIC_EFFECTIVENESS_PROOF"
    )
    assert metadata["claim_strength"] == "smoke_test_only"
    assert "fixed smoke benchmark" in metadata["candidate_technical_claim"]
    assert metadata["confidence_interval_method"] == "Wilson score interval, 95%"
    assert metadata["minimum_controlled_study_upgrade"]["minimum_scenarios"] == 500
    assert metadata["minimum_controlled_study_upgrade"]["target_evidence_level"] == (
        "CONTROLLED_STUDY_EFFECTIVENESS_READY"
    )
    assert "independent_signal_extraction" in metadata[
        "minimum_controlled_study_upgrade"
    ][
        "required_effectiveness_gates"
    ]
    required_difficulty = metadata["minimum_controlled_study_upgrade"][
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
        "SYNTHETIC_FIXED_OUTPUT_HARD_CASE_BENCHMARK"
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


def controlled_study_fixture_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for record in generate_llm_assurance_hard_cases.build_scenarios():
        output = str(record["model_output"])
        records.append(
            {
                **record,
                "freeze_schema_version": "aos-frozen-public-output/v1",
                "source_dataset": "public-fixture",
                "source_split": "test",
                "source_record_sha256": run_controlled_study.text_sha256(
                    record["id"]
                ),
                "model_id": "fixture-model-v1",
                "model_output_sha256": run_controlled_study.text_sha256(output),
            }
        )
    return records


def controlled_study_manifest(
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
        "study_id": "fixture-controlled-study",
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
        "predefined_metrics": sorted(run_controlled_study.REQUIRED_METRICS),
    }


def test_controlled_study_protocol_can_satisfy_protocol_criteria() -> None:
    metrics = run_controlled_study.build_metrics(
        controlled_study_fixture_records(),
        controlled_study_manifest(),
    )
    assessment = metrics["controlled_study_assessment"]

    assert metrics["schema_version"] == "llm-assurance-controlled-study/v1"
    assert metrics["benchmark_metadata"]["evidence_level"] == (
        "CONTROLLED_STUDY_PROTOCOL_ONLY_NO_EFFECTIVENESS_CLAIM"
    )
    assert metrics["benchmark_metadata"]["protocol_evidence_level"] == (
        "CONTROLLED_STUDY_PROTOCOL_READY"
    )
    assert assessment["controlled_study_criteria_satisfied"] is True
    assert assessment["protocol_criteria_satisfied"] is True
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


def test_controlled_study_protocol_does_not_overclaim() -> None:
    records = controlled_study_fixture_records()[:20]
    metrics = run_controlled_study.build_metrics(
        records,
        controlled_study_manifest(frozen=False),
    )
    assessment = metrics["controlled_study_assessment"]

    assert metrics["benchmark_metadata"]["evidence_level"] == (
        "CONTROLLED_STUDY_EFFECTIVENESS_NOT_READY"
    )
    assert metrics["benchmark_metadata"]["protocol_evidence_level"] == (
        "CONTROLLED_STUDY_PROTOCOL_NOT_READY"
    )
    assert assessment["controlled_study_criteria_satisfied"] is False
    assert assessment["effectiveness_criteria_satisfied"] is False
    assert "minimum_500_cases" in assessment["missing_criteria"]
    assert "frozen_model_outputs" in assessment["missing_criteria"]
    assert "protocol_criteria_satisfied" in assessment[
        "missing_effectiveness_criteria"
    ]


def test_effectiveness_claim_requires_independent_normalization_design() -> None:
    metrics = run_controlled_study.build_metrics(
        controlled_study_fixture_records(),
        controlled_study_manifest(effectiveness_ready=True),
    )
    assessment = metrics["controlled_study_assessment"]

    assert metrics["benchmark_metadata"]["evidence_level"] == (
        "CONTROLLED_STUDY_EFFECTIVENESS_READY"
    )
    assert metrics["benchmark_metadata"]["protocol_evidence_level"] == (
        "CONTROLLED_STUDY_PROTOCOL_READY"
    )
    assert assessment["protocol_criteria_satisfied"] is True
    assert assessment["effectiveness_criteria_satisfied"] is True
    assert assessment["missing_effectiveness_criteria"] == []
    assert metrics["claim_boundary"]["controlled_study_protocol_claim"] is True
    assert metrics["claim_boundary"]["controlled_study_effectiveness_claim"] is True


def test_controlled_text_profile_does_not_require_agent_categories() -> None:
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
                        "source_record_sha256": run_controlled_study.text_sha256(
                            f"{difficulty}-{category}-{index}"
                        ),
                        "model_id": "fixture-model-v1",
                        "model_output": output,
                        "model_output_sha256": run_controlled_study.text_sha256(
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

    manifest = controlled_study_manifest()
    manifest["evaluation_profile"] = "hallucination_text"
    metrics = run_controlled_study.build_metrics(records, manifest)
    assessment = metrics["controlled_study_assessment"]

    assert metrics["benchmark_metadata"]["evidence_level"] == (
        "CONTROLLED_STUDY_PROTOCOL_ONLY_NO_EFFECTIVENESS_CLAIM"
    )
    assert assessment["effectiveness_criteria_satisfied"] is False


def test_ragtruth_public_normalizer_does_not_use_labels_as_aos_signals() -> None:
    supported = run_ragtruth_public_benchmark.normalize_row(
        {
            "id": 1,
            "source_id": 10,
            "model": "fixture-model",
            "split": "test",
            "quality": "good",
            "labels": [],
            "response": "Paris is the capital of France.",
            "source_info": "France has Paris as its capital city.",
            "prompt": "Answer from the provided source.",
            "task_type": "QA",
        }
    )
    unsupported = run_ragtruth_public_benchmark.normalize_row(
        {
            "id": 2,
            "source_id": 11,
            "model": "fixture-model",
            "split": "test",
            "quality": "good",
            "labels": [{"start": 0, "end": 5, "label_type": "hallucination"}],
            "response": "The system supports private production credentials.",
            "source_info": "The public demo contains no production credentials.",
            "prompt": "Answer from the provided source.",
            "task_type": "QA",
        }
    )

    assert supported["category"] == "SUPPORTED"
    assert supported["expected_aos_verdict"] == "PASS"
    assert unsupported["category"] == "UNSUPPORTED"
    assert unsupported["expected_aos_verdict"] == "BLOCK"
    assert supported["signal_extraction"]["labels_used_as_aos_signals"] is False
    assert unsupported["signal_extraction"]["labels_used_as_aos_signals"] is False
    assert supported["warn_source_coverage_threshold"] == 0.85
    assert unsupported["warn_source_coverage_threshold"] == 0.85
    assert "ragtruth_label_count" in unsupported
    assert "unsupported_claim_count" in unsupported


def test_ragtruth_public_manifest_keeps_effectiveness_boundary() -> None:
    records = [
        run_ragtruth_public_benchmark.normalize_row(
            {
                "id": 1,
                "source_id": 10,
                "model": "fixture-model",
                "split": "test",
                "quality": "good",
                "labels": [],
                "response": "Paris is the capital of France.",
                "source_info": "France has Paris as its capital city.",
                "prompt": "Answer from the provided source.",
                "task_type": "QA",
            }
        )
    ]
    manifest = run_ragtruth_public_benchmark.build_manifest(
        records,
        dataset="leobianco/ragtruth",
        config="default",
        split="test",
        fetched_rows=1,
        warn_source_coverage_threshold=0.85,
    )

    design = manifest["effectiveness_design"]
    policy = manifest["aos_policy"]
    assert design["normalized_signals_source"] == "independent_extractor"
    assert design["labels_used_as_aos_signals"] is False
    assert design["held_out_manual_audit_present"] is False
    assert policy["warn_source_coverage_threshold"] == 0.85
    assert "not a production-readiness" in manifest["claim_boundary"]


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


def test_freeze_public_outputs_creates_controlled_study_compatible_records() -> None:
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
