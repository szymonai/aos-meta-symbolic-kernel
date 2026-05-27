from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CASES = Path(__file__).with_name("profile_cases.json")
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.aos_public_core import (  # noqa: E402
    build_signal_evidence,
    parse_signal,
    verify_signal_evidence,
)


def load_cases(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "aos-application-profile-cases/v1":
        raise ValueError("unexpected application profile schema")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("profile cases must be a non-empty list")
    return cases


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    evidence = asdict(build_signal_evidence(parse_signal(case["input"])))
    replay = verify_signal_evidence(evidence)
    expected = case["expected_verdict"]
    verdict = evidence["verdict"]
    return {
        "application": case["application"],
        "audit_id": evidence["audit_id"],
        "case_id": case["case_id"],
        "expected_verdict": expected,
        "input_digest": evidence["input_digest"],
        "matched_expected": verdict == expected,
        "replay_valid": replay["valid"],
        "verdict": verdict,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    results = [evaluate_case(case) for case in load_cases(args.cases)]
    print(json.dumps(results, indent=2, sort_keys=True))

    if args.check and not all(
        result["matched_expected"] and result["replay_valid"] for result in results
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
