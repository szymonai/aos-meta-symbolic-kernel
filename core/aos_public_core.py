from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Literal, TypeAlias

REFERENCE_IMPLEMENTATION_ONLY = True

Verdict: TypeAlias = Literal["PASS", "WARN", "BLOCK"]


def derive_verdict(upper_bound: float, limit: float, warn_margin: float) -> Verdict:
    if upper_bound > limit:
        return "BLOCK"
    if upper_bound > limit - warn_margin:
        return "WARN"
    return "PASS"


def _require_finite(name: str, value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _canonical_demo_payload(
    value: float,
    uncertainty: float,
    limit: float,
    verdict: Verdict,
) -> bytes:
    return json.dumps(
        {
            "limit": value_to_json_number(limit),
            "uncertainty": value_to_json_number(uncertainty),
            "value": value_to_json_number(value),
            "verdict": verdict,
        },
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def value_to_json_number(value: float) -> float:
    return float(value)


@dataclass(frozen=True, slots=True)
class DemoAuditRecord:
    value: float
    uncertainty: float
    limit: float
    verdict: Verdict
    audit_digest: str

    def verify_demo_digest(self) -> bool:
        payload = _canonical_demo_payload(
            self.value,
            self.uncertainty,
            self.limit,
            self.verdict,
        )
        expected = hashlib.sha256(payload).hexdigest()
        return self.audit_digest == expected


class DemoIntervalGate:
    """Limited demonstrator of PASS/WARN/BLOCK interval gating.

    This is not a production delivery format.
    """

    def __init__(self, limit: float, warn_margin: float) -> None:
        self.limit = _require_finite("limit", limit)
        self.warn_margin = _require_finite("warn_margin", warn_margin)
        if self.warn_margin < 0:
            raise ValueError("warn_margin must be non-negative")
        if self.warn_margin >= self.limit:
            raise ValueError("warn_margin must be lower than limit")

    def evaluate(
        self,
        value: float,
        uncertainty: float,
    ) -> DemoAuditRecord:
        value = _require_finite("value", value)
        uncertainty = _require_finite("uncertainty", uncertainty)
        if uncertainty < 0:
            raise ValueError("uncertainty must be non-negative")

        upper_bound = _require_finite("upper_bound", value + uncertainty)
        verdict = derive_verdict(upper_bound, self.limit, self.warn_margin)
        payload = _canonical_demo_payload(value, uncertainty, self.limit, verdict)
        digest = hashlib.sha256(payload).hexdigest()

        return DemoAuditRecord(
            value=value,
            uncertainty=uncertainty,
            limit=self.limit,
            verdict=verdict,
            audit_digest=digest,
        )
