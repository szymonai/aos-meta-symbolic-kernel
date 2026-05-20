from __future__ import annotations

import math
from dataclasses import FrozenInstanceError, replace

import pytest

from core.aos_public_core import (
    REFERENCE_IMPLEMENTATION_ONLY,
    DemoIntervalGate,
    derive_verdict,
)


def test_reference_flag_is_explicit() -> None:
    assert REFERENCE_IMPLEMENTATION_ONLY is True


def test_pass_warn_block_boundaries() -> None:
    gate = DemoIntervalGate(limit=100.0, warn_margin=5.0)

    assert gate.evaluate(95.0, 0.0).verdict == "PASS"
    assert gate.evaluate(95.0, 0.1).verdict == "WARN"
    assert gate.evaluate(99.0, 1.0).verdict == "WARN"
    assert gate.evaluate(99.0, 1.1).verdict == "BLOCK"


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
