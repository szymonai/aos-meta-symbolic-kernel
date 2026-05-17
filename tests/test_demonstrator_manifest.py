from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_demonstrator_manifest_preserves_public_boundary() -> None:
    manifest = json.loads(
        (ROOT / "evidence" / "demonstrator_manifest.json").read_text(
            encoding="utf-8",
        )
    )

    assert manifest["status"] == "limited_public_demonstrator"
    assert manifest["contains_full_aos_core"] is False
    assert manifest["contains_internal_policy_logic"] is False
    assert manifest["contains_real_clinical_thresholds"] is False
    assert manifest["contains_specialist_validation_stack"] is False
    assert manifest["claim_boundary"]["medical_device_claim"] is False
    assert manifest["claim_boundary"]["clinical_validation_claim"] is False
