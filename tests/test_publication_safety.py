from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

CONTROLLED_ARTIFACT_EXTENSIONS = {
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
        "-----BEGIN " + r"(?:RSA |EC |OPENSSH |)?" + "PRI" + "VATE" + " KEY-----",
        "YA" + r"LE-\d",
        r"GLI24_\d",
        "Bra" + r"TS-GLI-\d",
        "S" + "IL-3 " + "equivalent",
        "S" + "IL-3 " + "equivalence",
        "Tr" + "uth" + r"\s+" + "Kernel",
        "universal" + r"\s+" + "tr" + "uth",
        "production" + r"\s+" + "med" + "ical" + r"\s+" + "system",
        "hardware" + r"\s+" + "as" + r"\s+" + "mathematical" + r"\s+" + "tr" + "uth",
        "sac" + "red",
        "final" + r"\s+" + "proof",
        "mathematically" + r"\s+" + "abs" + "olute",
        "clin" + "ical" + r"\s+" + "guar" + "antee",
        r"\b" + "A" + "GI" + r"\b",
        r"\b" + "R" + "H" + r"\s+" + "proof",
        "mathematical" + r"\s+" + "break" + "through",
        "32" + "92",
        "Bra" + "TS",
        "TC" + "GA",
        "Ya" + "le",
        "0" + r"\.8108",
        "0" + r"\.8033",
        "0" + r"\.8065",
        "0" + r"\.8843",
        "0" + r"\.9085",
        "0" + r"\.8665",
        "c4" + "124" + r"[0-9a-f]{20,}",
        "Dataset" + "832",
        "hardware" + r"[-\s]+" + "origin",
        "autonomous" + r"\s+" + "reasoning",
        "AOS" + "Kernel",
        "pri" + "vate" + r"\s+" + "formal",
        "pri" + "vate" + r"\s+" + "manifest",
        "pri" + "vate" + r"\s+" + "performance",
        "generated" + r"\s+" + "by" + r"\s+" + "agents",
        "built" + r"\s+" + "by" + r"\s+" + "AI",
        "agent" + r"[-\s]+" + "built",
        "with" + "held",
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

    claim_boundary = manifest["claim_boundary"]
    assert isinstance(claim_boundary, dict)
    for key in (
        "domain_validation_claim",
        "production_runtime_claim",
        "regulated_use_claim",
        "safety_approval_claim",
    ):
        assert claim_boundary[key] is False

    assert manifest["contains_domain_dataset"] is False
    assert manifest["contains_real_world_evaluation_data"] is False
    assert manifest["data_redistributed_in_repo"] is False


def test_readme_links_public_technical_docs() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    for link in (
        "SCOPE_OF_PROOF.md",
        "docs/AI_PROBLEMS_ADDRESSED.md",
        "docs/PLAIN_LANGUAGE_OVERVIEW.md",
        "docs/SDK_BOUNDARY.md",
        "docs/PUBLIC_SURFACES.md",
        "docs/FORMAL_CLAIMS_BOUNDARY.md",
        "docs/architecture.md",
        "docs/INTEGRITY_ANCHORS.md",
        "docs/APPLICATION_PROFILES.md",
        "docs/DATASET_PROVENANCE.md",
        "docs/VALUE_METRICS.md",
        "docs/CALIBRATION_AND_OPTIMIZATION.md",
        "docs/DEMONSTRATOR_COMPARISON.md",
        "examples/hello-world",
        "examples/api-gate",
    ):
        assert link in readme


def test_required_public_docs_and_examples_exist() -> None:
    for relative_path in (
        "README.md",
        "VERSION",
        "SCOPE_OF_PROOF.md",
        "docs/AI_PROBLEMS_ADDRESSED.md",
        "docs/PLAIN_LANGUAGE_OVERVIEW.md",
        "docs/SDK_BOUNDARY.md",
        "docs/PUBLIC_SURFACES.md",
        "docs/FORMAL_CLAIMS_BOUNDARY.md",
        "docs/architecture.md",
        "docs/INTEGRITY_ANCHORS.md",
        "docs/APPLICATION_PROFILES.md",
        "docs/DEMONSTRATOR_COMPARISON.md",
        "docs/CLEAN_ROOM_TEST.md",
        "docs/VALUE_METRICS.md",
        "examples/hello-world/README.md",
        "examples/hello-world/docker-compose.yml",
        "examples/hello-world/hello_world.py",
        "examples/api-gate/README.md",
        "examples/api-gate/aos_api_gate.py",
        "examples/api-gate/sample_input.json",
        "examples/api-gate/sample_evidence.json",
        "examples/gradio-sandbox/README.md",
        "examples/gradio-sandbox/app.py",
        "examples/gradio-sandbox/requirements.txt",
        "benchmarks/k6/README.md",
        "benchmarks/k6/aos_api_smoke.js",
        "docs.json",
        "sonar-project.properties",
    ):
        assert (REPO_ROOT / relative_path).is_file(), relative_path


def test_all_json_files_are_valid() -> None:
    for path in iter_repo_files():
        if path.suffix.lower() != ".json":
            continue
        with path.open(encoding="utf-8") as file:
            json.load(file)


def test_lean_sources_do_not_use_gap_terms() -> None:
    for path in (REPO_ROOT / "lean").rglob("*.lean"):
        text = path.read_text(encoding="utf-8")
        for term in FORBIDDEN_LEAN_TERMS:
            assert not re.search(rf"\b{term}\b", text), (
                f"Lean gap term {term!r} in {path.relative_to(REPO_ROOT)}"
            )


def test_no_controlled_artifacts_or_model_binaries_are_committed() -> None:
    for path in iter_repo_files():
        suffixes = "".join(path.suffixes).lower()
        assert not any(
            suffixes.endswith(extension) for extension in CONTROLLED_ARTIFACT_EXTENSIONS
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
