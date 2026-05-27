from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_minimal_runtime_example_executes() -> None:
    result = subprocess.run(
        [sys.executable, "examples/minimal-runtime/minimal_runtime.py"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["signal_id"] == "minimal-runtime-risk-band"
    assert payload["verdict"] == "WARN"
    assert payload["replay_valid"] is True
    assert payload["audit_id"].startswith("sha256:")
    assert payload["input_digest"].startswith("sha256:")


def test_application_profile_cases_execute_and_replay() -> None:
    result = subprocess.run(
        [sys.executable, "examples/application-profiles/run_profiles.py", "--check"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    records = json.loads(result.stdout)

    assert {record["verdict"] for record in records} == {"PASS", "WARN", "BLOCK"}
    assert {record["application"] for record in records} == {
        "agent_tool_call_gate",
        "document_extraction",
        "financial_workflow_review",
        "industrial_sensor_review",
        "metadata_gate",
        "rag_answer_review",
    }
    assert all(record["matched_expected"] for record in records)
    assert all(record["replay_valid"] for record in records)
