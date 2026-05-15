from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = {
    "id": str,
    "domain": str,
    "description": str,
    "value": (int, float),
    "uncertainty": (int, float),
    "limit": (int, float),
    "expected_aos_verdict": str,
    "prompt_text": str,
    "risk_label": str,
}


def evaluate(scenario: dict[str, Any]) -> dict[str, str]:
    """Baseline that validates shape and types, not decision safety."""
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in scenario or not isinstance(scenario[field], expected_type):
            return {"verdict": "BLOCK"}
    return {"verdict": "PASS"}
