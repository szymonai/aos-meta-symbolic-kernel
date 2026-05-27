from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.aos_public_core import (  # noqa: E402
    build_signal_evidence,
    parse_signal,
    verify_signal_evidence,
)


def main() -> int:
    signal = parse_signal(
        {
            "signal_id": "minimal-runtime-risk-band",
            "score": 6400,
            "uncertainty": 400,
            "limit": 7000,
            "warn_margin": 1000,
            "metadata_complete": True,
        }
    )
    evidence = asdict(build_signal_evidence(signal))
    replay = verify_signal_evidence(evidence)

    print(
        json.dumps(
            {
                "audit_id": evidence["audit_id"],
                "input_digest": evidence["input_digest"],
                "replay_valid": replay["valid"],
                "signal_id": evidence["signal_id"],
                "verdict": evidence["verdict"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if replay["valid"] and evidence["verdict"] == "WARN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
