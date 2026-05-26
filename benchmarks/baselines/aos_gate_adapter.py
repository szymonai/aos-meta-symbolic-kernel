from __future__ import annotations

from functools import lru_cache
from typing import Any

from core.aos_public_core import DemoIntervalGate

WARN_MARGIN = 5.0


@lru_cache(maxsize=64)
def _gate_for_policy(limit: float, warn_margin: float) -> DemoIntervalGate:
    return DemoIntervalGate(limit=limit, warn_margin=warn_margin)


def evaluate(scenario: dict[str, Any]) -> dict[str, str]:
    """Adapter from synthetic benchmark scenarios to the public demo gate."""
    gate = _gate_for_policy(float(scenario["limit"]), WARN_MARGIN)
    record = gate.evaluate(
        value=float(scenario["value"]),
        uncertainty=float(scenario["uncertainty"]),
    )
    return {
        "verdict": record.verdict,
        "audit_digest": record.audit_digest,
    }
