from __future__ import annotations

from typing import Any

BLOCK_TERMS = ("block", "deny", "denied", "unsafe", "exceeds", "violate")
WARN_TERMS = ("review", "uncertain", "near", "close", "escalate")


def evaluate(scenario: dict[str, Any]) -> dict[str, str]:
    """Deterministic text heuristic that simulates prompt-only guardrails."""
    text = str(scenario["prompt_text"]).casefold()
    if any(term in text for term in BLOCK_TERMS):
        return {"verdict": "BLOCK"}
    if any(term in text for term in WARN_TERMS):
        return {"verdict": "WARN"}
    return {"verdict": "PASS"}
