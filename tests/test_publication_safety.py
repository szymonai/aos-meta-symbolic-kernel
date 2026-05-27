from __future__ import annotations

import json
import re
import subprocess
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
    ".lean",
    ".md",
    ".properties",
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
        "Dataset" + r"[-_\s]*" + "32" + "92",
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
        "FLAG" + "SHIP_CASE_STUDY",
        "proof" + "_manifest",
        "run_" + "e3_" + "controlled_study",
        "E3" + "_PUBLIC_DATASETS",
        "E1" + "_FIXED_OUTPUT",
        "E2" + "_FIXED_OUTPUT",
        "E3" + "_EFFECTIVENESS",
        "E3" + "_PROTOCOL",
        "eliminates" + r"\s+" + "risk",
        "ensures" + r"\s+" + "safety",
        "guaranteeing" + r"\s+" + "that" + r"\s+" + "the" + r"\s+" + "model",
        "85" + r"\s*%" + r"\s+" + "reduction",
        "100" + r"\s*%" + r"\s+" + "manual" + r"\s+" + "review",
        "critical" + r"\s+" + "failure" + r"\s+" + "rate",
        "business" + r"\s+" + "impact",
        "regulatory" + r"\s+" + "readiness",
    )
]

FORBIDDEN_LEAN_TERMS = ("ax" + "iom", "sor" + "ry", "ad" + "mit", "un" + "safe")


def iter_repo_files() -> list[Path]:
    ignored_parts = {
        ".git",
        ".lake",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "datasets",
        "pytest-cache-files-operational-fixture",
    }
    ignored_top_level_dirs = {"data"}
    return [
        path
        for path in REPO_ROOT.rglob("*")
        if path.is_file()
        and not any(part in ignored_parts for part in path.relative_to(REPO_ROOT).parts)
        and path.relative_to(REPO_ROOT).parts[0] not in ignored_top_level_dirs
    ]


def load_json(relative_path: str) -> dict[str, object]:
    with (REPO_ROOT / relative_path).open(encoding="utf-8") as file:
        payload = json.load(file)
    assert isinstance(payload, dict)
    return payload


def strip_public_hashes(text: str) -> str:
    return re.sub(r"\b[0-9a-f]{64}\b", "<sha256>", text)


def test_evidence_json_files_are_valid_and_claim_flags_are_false() -> None:
    manifest = load_json("evidence/demonstrator_manifest.json")

    claim_boundary = manifest["claim_boundary"]
    assert isinstance(claim_boundary, dict)
    for key in (
        "domain_validation_claim",
        "high_quality_public_effectiveness_proof_claim",
        "public_effectiveness_proof_sufficient",
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
        "docs/CONTROL_SPEC.md",
        "docs/AI_PROBLEMS_ADDRESSED.md",
        "docs/PLAIN_LANGUAGE_OVERVIEW.md",
        "docs/RUNTIME_SUBSTRATES.md",
        "docs/SDK_BOUNDARY.md",
        "docs/PUBLIC_SURFACES.md",
        "docs/ENGINEERING_PROOF.md",
        "docs/FORMAL_CLAIMS_BOUNDARY.md",
        "docs/OPERATIONAL_CONTROL_REPLAY.md",
        "docs/PUBLIC_ASSESSMENT.md",
        "docs/TECHNICAL_DILIGENCE.md",
        "docs/architecture.md",
        "docs/INTEGRITY_ANCHORS.md",
        "docs/APPLICATION_PROFILES.md",
        "docs/DATASET_PROVENANCE.md",
        "docs/VALUE_METRICS.md",
        "docs/EVIDENCE_STATUS.md",
        "docs/CALIBRATION_AND_OPTIMIZATION.md",
        "docs/DEMONSTRATOR_COMPARISON.md",
        "examples/hello-world",
        "examples/minimal-runtime",
        "examples/application-profiles",
        "examples/api-gate",
    ):
        assert link in readme


def test_required_public_docs_and_examples_exist() -> None:
    for relative_path in (
        "README.md",
        "VERSION",
        "SCOPE_OF_PROOF.md",
        "docs/CONTROL_SPEC.md",
        "docs/AI_PROBLEMS_ADDRESSED.md",
        "docs/PLAIN_LANGUAGE_OVERVIEW.md",
        "docs/RUNTIME_SUBSTRATES.md",
        "docs/SDK_BOUNDARY.md",
        "docs/PUBLIC_SURFACES.md",
        "docs/ENGINEERING_PROOF.md",
        "docs/FORMAL_CLAIMS_BOUNDARY.md",
        "docs/architecture.md",
        "docs/INTEGRITY_ANCHORS.md",
        "docs/APPLICATION_PROFILES.md",
        "docs/DEMONSTRATOR_COMPARISON.md",
        "docs/CLEAN_ROOM_TEST.md",
        "docs/VALUE_METRICS.md",
        "docs/EVIDENCE_STATUS.md",
        "docs/PUBLIC_ASSESSMENT.md",
        "docs/TECHNICAL_DILIGENCE.md",
        "docs/LLM_ASSURANCE_EVALUATION.md",
        "docs/CONTROLLED_STUDY_DATASETS.md",
        "examples/hello-world/README.md",
        "examples/hello-world/docker-compose.yml",
        "examples/hello-world/hello_world.py",
        "examples/minimal-runtime/README.md",
        "examples/minimal-runtime/minimal_runtime.py",
        "examples/application-profiles/README.md",
        "examples/application-profiles/profile_cases.json",
        "examples/application-profiles/run_profiles.py",
        "examples/api-gate/README.md",
        "examples/api-gate/aos_api_gate.py",
        "examples/api-gate/sample_input.json",
        "examples/api-gate/sample_evidence.json",
        "examples/gradio-sandbox/README.md",
        "examples/gradio-sandbox/app.py",
        "examples/gradio-sandbox/requirements.txt",
        "benchmarks/k6/README.md",
        "benchmarks/k6/aos_api_smoke.js",
        "benchmarks/run_ragtruth_public_benchmark.py",
        "benchmarks/run_operational_control_replay.py",
        "benchmarks/results/operational_control_replay_metrics.json",
        "benchmarks/results/operational_control_replay_summary.md",
        "evidence/integrity_manifest.json",
        "tests/fixtures/operational_control_replay/NAB/data/realKnownCause/fixture.csv",
        "tests/fixtures/operational_control_replay/NAB/labels/combined_windows.json",
        "tools/verify_public_integrity.py",
        "docs.json",
        "sonar-project.properties",
    ):
        assert (REPO_ROOT / relative_path).is_file(), relative_path


def test_docs_navigation_points_to_existing_files() -> None:
    docs_config = load_json("docs.json")
    navigation = docs_config["navigation"]
    assert isinstance(navigation, dict)

    tabs = navigation["tabs"]
    assert isinstance(tabs, list)
    pages: list[str] = []
    for tab in tabs:
        assert isinstance(tab, dict)
        groups = tab["groups"]
        assert isinstance(groups, list)
        for group in groups:
            assert isinstance(group, dict)
            group_pages = group["pages"]
            assert isinstance(group_pages, list)
            pages.extend(str(page) for page in group_pages)

    for page in pages:
        if page == "README":
            assert (REPO_ROOT / "README.md").is_file()
        else:
            assert (REPO_ROOT / f"{page}.md").is_file()


def test_public_docs_avoid_internal_evidence_labels() -> None:
    labels = (r"\bE1\b", r"\bE2\b", r"\bE3\b", r"\bE4\b")
    for path in [REPO_ROOT / "README.md", *(REPO_ROOT / "docs").glob("*.md")]:
        text = path.read_text(encoding="utf-8")
        for label in labels:
            assert not re.search(label, text), path.relative_to(REPO_ROOT)


def test_public_validation_docs_use_benchmark_check_mode() -> None:
    for relative_path in (
        "README.md",
        "docs/CLEAN_ROOM_TEST.md",
        "CONTRIBUTING.md",
        ".github/pull_request_template.md",
    ):
        text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        assert "python benchmarks/run_benchmarks.py --check" in text
        assert "python benchmarks/run_operational_control_replay.py --check" in text
        assert "python tools/verify_public_integrity.py" in text


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


def test_lean_surface_links_json_input_shape_to_verdict_model() -> None:
    text = (REPO_ROOT / "lean" / "AOSPublicCore.lean").read_text(encoding="utf-8")

    for symbol in (
        "JsonGateInput",
        "jsonGateVerdict",
        "jsonCompleteInputUsesIntervalVerdict",
        "jsonIncompleteInputBlocks",
        "jsonCompleteBlockCorrect",
        "jsonCompleteWarnCorrect",
        "jsonCompletePassCorrect",
        "AuditDecision",
        "auditDecisionReady",
        "exactBlockDecisionNotSilent",
        "StudyCriteria",
        "EffectivenessCriteria",
        "controlledStudyReady",
        "studyDesignReady",
        "studyAuditReady",
        "studyEvidenceLevel",
        "publicEvidenceLevel",
        "effectivenessReady",
        "controlledStudyAssessmentDoesNotOverclaim",
        "publicEffectivenessEvidenceRequiresProtocol",
        "publicEffectivenessEvidenceRequiresEffectivenessReady",
        "labelMappingBlocksEffectivenessReady",
        "controlledStudyReadyRequiresAudit",
        "controlledStudyReadyRequiresDesign",
        "missingMinimumCasesBlocksControlledStudy",
    ):
        assert symbol in text


def test_formal_claim_boundary_states_lean_sufficiency_limits() -> None:
    text = (REPO_ROOT / "docs" / "FORMAL_CLAIMS_BOUNDARY.md").read_text(
        encoding="utf-8"
    )

    required_phrases = (
        "Abstract verdict-integrity claim",
        "Sufficient for selected invariants",
        "Runtime equivalence claim",
        "Real-world effectiveness claim",
        "Not sufficient",
        "lake build AOSPublicCore",
        "python tools/verify_public_integrity.py",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_public_architecture_includes_signal_extraction_boundary() -> None:
    architecture = (REPO_ROOT / "docs" / "architecture.md").read_text(
        encoding="utf-8"
    )
    abstraction_map = (REPO_ROOT / "docs" / "ABSTRACTION_MAP.md").read_text(
        encoding="utf-8"
    )

    for text in (architecture, abstraction_map):
        assert "signal extraction / normalization" in text
        assert "bounded" in text

    assert "Operational control replay" in architecture
    assert "operational replay measures control behavior after" in abstraction_map
    assert "does not prove the correctness of signal extraction" in architecture


def test_runtime_substrate_boundary_does_not_overclaim() -> None:
    text = (REPO_ROOT / "docs" / "RUNTIME_SUBSTRATES.md").read_text(
        encoding="utf-8"
    )
    architecture = (REPO_ROOT / "docs" / "architecture.md").read_text(
        encoding="utf-8"
    )
    abstraction_map = (REPO_ROOT / "docs" / "ABSTRACTION_MAP.md").read_text(
        encoding="utf-8"
    )

    for term in ("C++", "Rust", "CUDA", "PTX", "Assembly", "WASM", "eBPF"):
        assert term in text

    for phrase in (
        "implementation options only",
        "do not change the public AOS semantics",
        "does not claim production latency",
        "native-runtime equivalence",
    ):
        assert phrase in text

    assert "Substrate Independence" in architecture
    assert "Runtime substrate boundary" in abstraction_map


def test_public_assessment_binds_usefulness_scale_and_evidence() -> None:
    text = (REPO_ROOT / "docs" / "PUBLIC_ASSESSMENT.md").read_text(
        encoding="utf-8"
    )

    for phrase in (
        "Usefulness",
        "Scalability",
        "Evidence",
        "362,774",
        "96.55%",
        "3.45%",
        "12.76%",
        "bounded production-relevant replay claim",
        "insufficient for production effectiveness",
        "cannot yet support",
    ):
        assert phrase in text

    assert "AOS is production ready" in text
    assert "AOS is clinically ready" in text


def test_engineering_proof_surface_is_executable_and_concrete() -> None:
    text = (REPO_ROOT / "docs" / "ENGINEERING_PROOF.md").read_text(
        encoding="utf-8"
    )

    for phrase in (
        "python examples/minimal-runtime/minimal_runtime.py",
        "python examples/application-profiles/run_profiles.py --check",
        "python benchmarks/run_operational_control_replay.py --check",
        "362,774 records",
        "Minimal Runtime",
        "Concrete Application Cases",
        "Quantum job gate",
        "Hard Failure Conditions",
    ):
        assert phrase in text


def test_technical_diligence_boundary_is_bounded() -> None:
    text = (REPO_ROOT / "docs" / "TECHNICAL_DILIGENCE.md").read_text(
        encoding="utf-8"
    )

    for phrase in (
        "investment decision",
        "production-relevant offline replay evidence",
        "Investor-Grade Diligence Needs A Separate Data Room",
        "customer validation",
        "public technical evidence: credible but bounded",
        "commercial proof: not established in this repository",
    ):
        assert phrase in text


def test_committed_test_fixtures_are_not_git_ignored() -> None:
    for relative_path in (
        "tests/fixtures/operational_control_replay/NAB/data/realKnownCause/fixture.csv",
        "tests/fixtures/operational_control_replay/NAB/labels/combined_windows.json",
    ):
        result = subprocess.run(
            ["git", "check-ignore", "-q", relative_path],
            cwd=REPO_ROOT,
            check=False,
        )
        assert result.returncode == 1, f"fixture is git-ignored: {relative_path}"


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
        text = strip_public_hashes(path.read_text(encoding="utf-8"))
        for pattern in FORBIDDEN_TEXT_PATTERNS:
            assert not pattern.search(text), (
                f"forbidden pattern {pattern.pattern!r} in "
                f"{path.relative_to(REPO_ROOT)}"
            )
