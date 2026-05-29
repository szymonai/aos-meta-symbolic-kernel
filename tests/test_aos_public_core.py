from __future__ import annotations

import math
from dataclasses import FrozenInstanceError, asdict, replace

import pytest

from core.aos_public_core import (
    REFERENCE_IMPLEMENTATION_ONLY,
    DemoIntervalGate,
    build_signal_evidence,
    derive_verdict,
    parse_signal,
    verify_signal_evidence,
)


def test_reference_flag_is_explicit() -> None:
    assert REFERENCE_IMPLEMENTATION_ONLY is True


def test_pass_warn_block_boundaries() -> None:
    gate = DemoIntervalGate(limit=100.0, warn_margin=5.0)

    assert gate.evaluate(95.0, 0.0).verdict == "PASS"
    assert gate.evaluate(95.0, 0.1).verdict == "WARN"
    assert gate.evaluate(99.0, 1.0).verdict == "WARN"
    assert gate.evaluate(99.0, 1.1).verdict == "BLOCK"


def test_decimal_interval_boundaries_for_non_integer_inputs() -> None:
    gate = DemoIntervalGate(limit=0.3, warn_margin=0.1)

    assert gate.evaluate(0.1, 0.1).verdict == "PASS"
    assert gate.evaluate(0.1, 0.2).verdict == "WARN"
    assert gate.evaluate(0.1, 0.20000000000000004).verdict == "BLOCK"


def test_demo_audit_digest_detects_tampering() -> None:
    record = DemoIntervalGate(100.0, 5.0).evaluate(90.0, 2.0)

    assert record.verify_demo_digest()
    assert not replace(record, value=91.0).verify_demo_digest()


def test_demo_record_is_immutable() -> None:
    record = DemoIntervalGate(100.0, 5.0).evaluate(90.0, 2.0)

    with pytest.raises(FrozenInstanceError):
        record.value = 1.0


@pytest.mark.parametrize("bad_value", [math.nan, math.inf, -math.inf])
def test_non_finite_inputs_are_rejected(bad_value: float) -> None:
    gate = DemoIntervalGate(100.0, 5.0)

    with pytest.raises(ValueError):
        gate.evaluate(bad_value, 0.0)

    with pytest.raises(ValueError):
        gate.evaluate(1.0, bad_value)


def test_negative_uncertainty_and_warn_margin_are_rejected() -> None:
    with pytest.raises(ValueError):
        DemoIntervalGate(100.0, -1.0)

    with pytest.raises(ValueError):
        DemoIntervalGate(100.0, 5.0).evaluate(90.0, -1.0)


def test_upper_bound_overflow_is_rejected() -> None:
    with pytest.raises(ValueError):
        DemoIntervalGate(1e308, 5.0).evaluate(1e308, 1e308)


def test_abstract_verdict_function() -> None:
    assert derive_verdict(90.0, 100.0, 5.0) == "PASS"
    assert derive_verdict(96.0, 100.0, 5.0) == "WARN"
    assert derive_verdict(101.0, 100.0, 5.0) == "BLOCK"


def test_canonical_signal_evidence_replays() -> None:
    signal = parse_signal(
        {
            "limit": 9000,
            "metadata_complete": True,
            "score": 8200,
            "signal_id": "demo-signal-001",
            "uncertainty": 1200,
            "warn_margin": 1000,
        }
    )
    evidence = build_signal_evidence(signal)
    result = verify_signal_evidence(asdict(evidence))

    assert evidence.verdict == "BLOCK"
    assert evidence.audit_id.startswith("sha256:")
    assert result["valid"] is True
    assert result["mismatches"] == []


def test_demo_signal_evidence_contract_is_unchanged() -> None:
    signal = parse_signal(
        {
            "limit": 9000,
            "metadata_complete": True,
            "score": 8200,
            "signal_id": "demo-signal-001",
            "uncertainty": 1200,
            "warn_margin": 1000,
        }
    )

    assert asdict(build_signal_evidence(signal)) == {
        "audit_id": (
            "sha256:e545f9db7dac16f41dd2aef400efb377e47d4d8afee34a6736a408b1254bca7e"
        ),
        "claim_boundary": {
            "external_validation_claim": False,
            "production_use_claim": False,
            "regulated_use_claim": False,
        },
        "input": {
            "limit": 9000,
            "metadata_complete": True,
            "policy_id": "demo_gate_policy_v1",
            "policy_version": "1.0.0",
            "score": 8200,
            "signal_id": "demo-signal-001",
            "uncertainty": 1200,
            "warn_margin": 1000,
        },
        "input_digest": (
            "sha256:fc96f9b6deb3d6c25efed961dcff5888fb0b20f68e89e3cbab4a5edc47ccb8fc"
        ),
        "policy_id": "demo_gate_policy_v1",
        "policy_version": "1.0.0",
        "reason": "Score plus uncertainty exceeds the allowed envelope.",
        "replayable": True,
        "schema_version": "aos-demo-evidence/v1",
        "signal_id": "demo-signal-001",
        "verdict": "BLOCK",
    }


def test_incomplete_signal_blocks_before_numeric_band() -> None:
    signal = parse_signal(
        {
            "limit": 9000,
            "metadata_complete": False,
            "score": 100,
            "signal_id": "incomplete-signal",
            "uncertainty": 0,
            "warn_margin": 1000,
        }
    )
    evidence = build_signal_evidence(signal)

    assert evidence.verdict == "BLOCK"
    assert evidence.reason == "Required metadata is incomplete."
