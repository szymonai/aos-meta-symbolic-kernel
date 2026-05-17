from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_hello_world_example_blocks_zero_denominator() -> None:
    result = subprocess.run(
        [sys.executable, "hello_world.py"],
        cwd=ROOT / "examples" / "hello-world",
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["proposed_expression"] == "10 / x"
    assert payload["input"] == {"x": 0}
    assert payload["policy"] == "denominator_non_zero"
    assert payload["verdict"] == "BLOCK"
    assert payload["reason"] == "denominator must be non-zero"
    assert isinstance(payload["audit_id"], str)
    assert payload["audit_id"].startswith("sha256:")
    assert len(payload["audit_id"]) == len("sha256:") + 64
