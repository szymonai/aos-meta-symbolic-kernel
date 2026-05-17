from __future__ import annotations

import hashlib
import json


def build_verdict(x: int) -> dict[str, object]:
    policy = "denominator_non_zero"
    proposed_expression = "10 / x"

    if x == 0:
        verdict = "BLOCK"
        reason = "denominator must be non-zero"
    else:
        verdict = "PASS"
        reason = "denominator is non-zero"

    audit_payload = {
        "input": {"x": x},
        "policy": policy,
        "proposed_expression": proposed_expression,
        "reason": reason,
        "verdict": verdict,
    }
    digest = hashlib.sha256(
        json.dumps(
            audit_payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    return {
        **audit_payload,
        "audit_id": f"sha256:{digest}",
    }


if __name__ == "__main__":
    print(json.dumps(build_verdict(0), indent=2, sort_keys=True))
