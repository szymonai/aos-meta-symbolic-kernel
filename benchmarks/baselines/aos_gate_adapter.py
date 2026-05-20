from __future__ import annotations

from typing import Any

from core.aos_public_core import DemoIntervalGate

WARN_MARGIN = 5.0


def evaluate(scenario: dict[str, Any]) -> dict[str, str]:
    """Adapter from synthetic benchmark scenarios to the public demo gate."""
    gate = DemoIntervalGate(
        limit=float(scenario["limit"]),
        warn_margin=WARN_MARGIN,
    )
    record = gate.evaluate(
        value=float(scenario["value"]),
        uncertainty=float(scenario["uncertainty"]),
    )
    return {
        "verdict": record.verdict,
        "audit_digest": record.audit_digest,
    }
