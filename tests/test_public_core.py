from __future__ import annotations

from dataclasses import replace

import pytest

from core.aos_public_core import DemoIntervalGate


def test_warn_margin_must_be_lower_than_limit() -> None:
    with pytest.raises(ValueError, match="warn_margin must be lower than limit"):
        DemoIntervalGate(limit=10.0, warn_margin=10.0)

    with pytest.raises(ValueError, match="warn_margin must be lower than limit"):
        DemoIntervalGate(limit=10.0, warn_margin=11.0)


def test_warn_margin_boundary_verdicts_are_explicit() -> None:
    gate = DemoIntervalGate(limit=100.0, warn_margin=5.0)

    assert gate.evaluate(value=95.0, uncertainty=0.0).verdict == "PASS"
    assert gate.evaluate(value=95.001, uncertainty=0.0).verdict == "WARN"
    assert gate.evaluate(value=100.0, uncertainty=0.0).verdict == "WARN"
    assert gate.evaluate(value=100.001, uncertainty=0.0).verdict == "BLOCK"


def test_demo_digest_detects_value_tampering() -> None:
    record = DemoIntervalGate(limit=100.0, warn_margin=5.0).evaluate(
        value=80.0,
        uncertainty=3.0,
    )

    assert record.verify_demo_digest() is True
    assert replace(record, value=81.0).verify_demo_digest() is False
