from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "api-gate"


def run_api_gate(
    *args: str,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "aos_api_gate.py", *args],
        cwd=EXAMPLE,
        check=check,
        capture_output=True,
        input=input_text,
        text=True,
    )


def test_api_gate_sample_evidence_replays() -> None:
    result = run_api_gate("replay", "--evidence", "sample_evidence.json")
    payload = json.loads(result.stdout)

    assert payload["valid"] is True
    assert payload["mismatches"] == []
    assert payload["replayed"]["signal_id"] == "demo-signal-001"
    assert payload["replayed"]["verdict"] == "BLOCK"
    assert payload["replayed"]["audit_id"].startswith("sha256:")


def test_api_gate_evaluate_and_replay_round_trip() -> None:
    result = run_api_gate("evaluate", "--input", "sample_input.json")
    evidence = json.loads(result.stdout)
    sample = json.loads((EXAMPLE / "sample_evidence.json").read_text(encoding="utf-8"))

    assert evidence == sample
    assert evidence["schema_version"] == "aos-demo-evidence/v1"
    assert evidence["signal_id"] == "demo-signal-001"
    assert evidence["verdict"] == "BLOCK"
    assert evidence["reason"] == "Score plus uncertainty exceeds the allowed envelope."
    assert evidence["input_digest"].startswith("sha256:")
    assert evidence["audit_id"].startswith("sha256:")
    assert evidence["claim_boundary"] == {
        "external_validation_claim": False,
        "production_use_claim": False,
        "regulated_use_claim": False,
    }


def test_api_gate_replay_rejects_tampered_evidence() -> None:
    sample_text = (EXAMPLE / "sample_evidence.json").read_text(encoding="utf-8")
    evidence = json.loads(sample_text)
    evidence["verdict"] = "PASS"
    result = run_api_gate(
        "replay",
        "--evidence",
        "-",
        check=False,
        input_text=json.dumps(evidence),
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    assert payload["valid"] is False
    assert payload["mismatches"][0]["field"] == "verdict"
