from __future__ import annotations

from typing import Any


def evaluate(scenario: dict[str, Any]) -> dict[str, str]:
    """Baseline that ignores uncertainty and checks only value <= limit."""
    value = float(scenario["value"])
    limit = float(scenario["limit"])
    verdict = "PASS" if value <= limit else "BLOCK"
    return {"verdict": verdict}
