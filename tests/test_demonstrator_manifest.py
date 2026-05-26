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
    assert manifest["public_effectiveness_evidence_status"] == (
        "insufficient_for_high_quality_public_proof"
    )
    assert manifest["contains_full_aos_core"] is False
    assert manifest["contains_internal_policy_logic"] is False
    assert manifest["contains_domain_dataset"] is False
    assert manifest["contains_real_world_evaluation_data"] is False
    assert manifest["contains_specialist_validation_stack"] is False
    assert manifest["claim_boundary"]["domain_validation_claim"] is False
    assert manifest["claim_boundary"][
        "high_quality_public_effectiveness_proof_claim"
    ] is False
    assert manifest["claim_boundary"]["public_effectiveness_proof_sufficient"] is False
    assert manifest["claim_boundary"]["regulated_use_claim"] is False
    assert manifest["claim_boundary"]["safety_approval_claim"] is False
