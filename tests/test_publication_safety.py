from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MEDICAL_OR_MODEL_EXTENSIONS = {
    ".dcm",
    ".dicom",
    ".nii",
    ".nrrd",
    ".mha",
    ".mhd",
    ".mgz",
    ".ckpt",
    ".pt",
    ".pth",
    ".onnx",
    ".safetensors",
}

TEXT_EXTENSIONS = {
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}

FORBIDDEN_TEXT_PATTERNS = [
    re.compile(pattern)
    for pattern in (
        "C:" + r"\\",
        "C:" + r"/Users/",
        "C:" + r"/Data/",
        "Users" + r"\\fidry",
        "ghp" + r"_[A-Za-z0-9_]+",
        "github" + r"_pat_[A-Za-z0-9_]+",
        "-----BEGIN " + r"(?:RSA |EC |OPENSSH |)?PRIVATE" + " KEY-----",
        r"YALE-\d",
        r"GLI24_\d",
        r"BraTS-GLI-\d",
        "SIL-3 " + "equivalent",
        "SIL-3 " + "equivalence",
        "Truth" + r"\s+" + "Kernel",
        "universal" + r"\s+" + "truth",
        "production" + r"\s+" + "medical" + r"\s+" + "system",
        "hardware" + r"\s+" + "as" + r"\s+" + "mathematical" + r"\s+" + "truth",
        "sac" + "red",
        "final" + r"\s+" + "proof",
        "mathematically" + r"\s+" + "absolute",
        "clinical" + r"\s+" + "guarantee",
    )
]

FORBIDDEN_LEAN_TERMS = ("ax" + "iom", "sor" + "ry", "ad" + "mit", "un" + "safe")


def iter_repo_files() -> list[Path]:
    ignored_parts = {".git", ".lake", ".ruff_cache", "__pycache__"}
    return [
        path
        for path in REPO_ROOT.rglob("*")
        if path.is_file() and not any(part in ignored_parts for part in path.parts)
    ]


def load_json(relative_path: str) -> dict[str, object]:
    with (REPO_ROOT / relative_path).open(encoding="utf-8") as file:
        payload = json.load(file)
    assert isinstance(payload, dict)
    return payload


def test_evidence_json_files_are_valid_and_claim_flags_are_false() -> None:
    manifest = load_json("evidence/demonstrator_manifest.json")
    radiology = load_json("evidence/radiology_offline_evaluation.json")
    radiology_review = load_json("evidence/radiology_evidence_review.json")

    claim_boundary = manifest["claim_boundary"]
    assert isinstance(claim_boundary, dict)
    for key in (
        "clinical_claim",
        "clinical_validation_claim",
        "medical_device_claim",
        "regulatory_compliance_claim",
        "production_runtime_claim",
    ):
        assert claim_boundary[key] is False

    claim_flags = radiology["claim_flags"]
    assert isinstance(claim_flags, dict)
    for key in (
        "clinical_claim",
        "medical_device_claim",
        "regulatory_compliance_claim",
        "data_redistributed_in_repo",
        "production_ready_claim",
        "sota_claim",
    ):
        assert claim_flags[key] is False

    current_status = radiology["current_public_evidence_status"]
    assert isinstance(current_status, dict)
    assert (
        current_status["brats_2025_results"]
        == "not available in current public evidence"
    )
    assert "offline_evaluations" not in radiology

    review_flags = radiology_review["claim_flags"]
    assert isinstance(review_flags, dict)
    for key in (
        "clinical_claim",
        "clinical_validation_claim",
        "medical_device_claim",
        "regulatory_compliance_claim",
        "production_ready_claim",
        "sota_claim",
        "sil_claim",
        "data_redistributed_in_repo",
    ):
        assert review_flags[key] is False

    reviewed = radiology_review["verified_internal_artifacts"]
    assert isinstance(reviewed, list)
    assert {item["id"] for item in reviewed if isinstance(item, dict)} == {
        "dataset832_fold0_validation_label2",
        "internal_cohort_report_mdr83",
        "private_formal_integrity_status",
    }

    milestones = radiology_review["public_milestones"]
    assert isinstance(milestones, dict)
    assert milestones["internal_cohort_dice_wt"] == 0.8108
    assert milestones["internal_cohort_dice_et"] == 0.8033
    assert milestones["dataset832_fold_label2_dice"] == 0.8843
    assert milestones["dataset832_fold_label2_recall"] == 0.9085
    assert milestones["formal_tasks_completed"] == 3292

    manifest_hash = milestones["manifest_payload_sha512"]
    assert isinstance(manifest_hash, str)
    assert len(manifest_hash) == 128
    assert all(character in "0123456789abcdef" for character in manifest_hash)


def test_readme_links_public_evidence_docs() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    for link in (
        "SCOPE_OF_PROOF.md",
        "docs/AI_PROBLEMS_ADDRESSED.md",
        "docs/architecture.md",
        "docs/RADIOLOGY_REFERENCE_SYSTEM.md",
        "docs/OFFLINE_EVALUATION_RESULTS.md",
        "docs/RADIOLOGY_EVIDENCE_REVIEW.md",
        "docs/UNIVERSAL_KERNEL_POSITIONING.md",
        "docs/DATASET_PROVENANCE.md",
        "docs/CUSTOMER_VALUE.md",
        "docs/VALUE_METRICS.md",
        "docs/REGULATORY_READINESS.md",
        "docs/CALIBRATION_AND_OPTIMIZATION.md",
        "docs/TECHNICAL_ADVANTAGE.md",
        "examples/hello-world",
        "evidence/radiology_offline_evaluation.json",
        "evidence/radiology_evidence_review.json",
    ):
        assert link in readme


def test_required_public_docs_and_examples_exist() -> None:
    for relative_path in (
        "README.md",
        "SCOPE_OF_PROOF.md",
        "docs/AI_PROBLEMS_ADDRESSED.md",
        "docs/architecture.md",
        "docs/CLEAN_ROOM_TEST.md",
        "docs/VALUE_METRICS.md",
        "examples/hello-world/README.md",
        "examples/hello-world/docker-compose.yml",
        "examples/hello-world/hello_world.py",
    ):
        assert (REPO_ROOT / relative_path).is_file(), relative_path


def test_all_json_files_are_valid() -> None:
    for path in iter_repo_files():
        if path.suffix.lower() != ".json":
            continue
        with path.open(encoding="utf-8") as file:
            json.load(file)


def test_lean_sources_do_not_use_placeholder_terms() -> None:
    for path in (REPO_ROOT / "lean").rglob("*.lean"):
        text = path.read_text(encoding="utf-8")
        for term in FORBIDDEN_LEAN_TERMS:
            assert not re.search(rf"\b{term}\b", text), (
                f"Lean placeholder term {term!r} in {path.relative_to(REPO_ROOT)}"
            )


def test_radiology_public_evidence_does_not_publish_stale_metrics() -> None:
    radiology = load_json("evidence/radiology_offline_evaluation.json")

    historical = radiology["historical_artifacts"]
    assert isinstance(historical, list)
    assert historical
    for item in historical:
        assert isinstance(item, dict)
        assert item["status"] == "historical_superseded_not_current"
        assert item["metrics_published_as_current"] is False


def test_no_medical_data_images_masks_or_checkpoints_are_committed() -> None:
    for path in iter_repo_files():
        suffixes = "".join(path.suffixes).lower()
        assert not any(
            suffixes.endswith(extension) for extension in MEDICAL_OR_MODEL_EXTENSIONS
        ), f"forbidden artifact type committed: {path.relative_to(REPO_ROOT)}"


def test_no_local_paths_secrets_or_per_case_ids_in_text_files() -> None:
    for path in iter_repo_files():
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            assert not pattern.search(text), (
                f"forbidden pattern {pattern.pattern!r} in "
                f"{path.relative_to(REPO_ROOT)}"
            )
