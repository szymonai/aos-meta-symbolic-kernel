from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
INTEGRITY_MANIFEST = REPO_ROOT / "evidence" / "integrity_manifest.json"
DEMONSTRATOR_MANIFEST = REPO_ROOT / "evidence" / "demonstrator_manifest.json"
DOCS_CONFIG = REPO_ROOT / "docs.json"

IGNORED_PARTS = {
    ".git",
    ".lake",
    ".ruff_cache",
    ".pytest_cache",
    "__pycache__",
    "datasets",
    "pytest-cache-files-operational-fixture",
}
IGNORED_TOP_LEVEL_DIRS = {"data"}
LEAN_GAP_TERMS = ("axiom", "sorry", "admit", "unsafe")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")
EXTERNAL_LINK_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
)
REQUIRED_INTEGRITY_PATHS = {
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    ".github/workflows/aos-core-ci.yml",
    ".gitignore",
    "CONTRIBUTING.md",
    "README.md",
    "SCOPE_OF_PROOF.md",
    "benchmarks/controlled_study_manifest.example.json",
    "benchmarks/results/metrics.json",
    "benchmarks/results/operational_control_replay_metrics.json",
    "benchmarks/results/operational_control_replay_summary.md",
    "benchmarks/run_benchmarks.py",
    "benchmarks/run_controlled_study.py",
    "benchmarks/run_operational_control_replay.py",
    "core/aos_public_core.py",
    "docs/CONTROLLED_STUDY_DATASETS.md",
    "docs/CONTROL_SPEC.md",
    "docs/OPERATIONAL_CONTROL_REPLAY.md",
    "docs/PUBLIC_ASSESSMENT.md",
    "docs/RUNTIME_SUBSTRATES.md",
    "docs/TECHNICAL_DILIGENCE.md",
    "docs/architecture.md",
    "docs.json",
    "evidence/demonstrator_manifest.json",
    "examples/api-gate/aos_api_gate.py",
    "lakefile.lean",
    "lean/AOSPublicCore.lean",
    "tests/fixtures/operational_control_replay/NAB/data/realKnownCause/fixture.csv",
    "tests/fixtures/operational_control_replay/NAB/labels/combined_windows.json",
    "tests/test_benchmarks.py",
    "tests/test_public_integrity.py",
    "tests/test_publication_safety.py",
    "tests/test_runtime_correspondence.py",
    "tools/verify_public_integrity.py",
}
REQUIRED_FALSE_INTEGRITY_CLAIMS = (
    "aos_effectiveness_claim",
    "external_validation_claim",
    "high_quality_public_effectiveness_proof_claim",
    "production_runtime_claim",
    "regulated_use_claim",
    "release_signature_claim",
    "supply_chain_attestation_claim",
)


def iter_repo_files() -> list[Path]:
    return [
        path
        for path in REPO_ROOT.rglob("*")
        if path.is_file()
        and not any(part in IGNORED_PARTS for part in path.relative_to(REPO_ROOT).parts)
        and path.relative_to(REPO_ROOT).parts[0] not in IGNORED_TOP_LEVEL_DIRS
    ]


def load_json_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} must contain a JSON object")
    return payload


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_index_bytes(relative_path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show", f":{relative_path}"],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def sha256_public_artifact(relative_path: str, path: Path) -> str:
    content = git_index_bytes(relative_path)
    if content is None:
        content = path.read_bytes()
    return hashlib.sha256(content).hexdigest()


def validate_all_json(errors: list[str]) -> None:
    for path in iter_repo_files():
        if path.suffix.lower() != ".json":
            continue
        try:
            with path.open(encoding="utf-8") as file:
                json.load(file)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON: {path.relative_to(REPO_ROOT)}: {exc}")


def validate_docs_navigation(errors: list[str]) -> None:
    docs_config = load_json_object(DOCS_CONFIG)
    navigation = docs_config.get("navigation")
    if not isinstance(navigation, dict):
        errors.append("docs.json navigation must be an object")
        return

    tabs = navigation.get("tabs")
    if not isinstance(tabs, list):
        errors.append("docs.json navigation.tabs must be a list")
        return

    for tab in tabs:
        if not isinstance(tab, dict):
            errors.append("docs.json tab must be an object")
            continue
        groups = tab.get("groups")
        if not isinstance(groups, list):
            errors.append("docs.json tab.groups must be a list")
            continue
        for group in groups:
            if not isinstance(group, dict):
                errors.append("docs.json group must be an object")
                continue
            pages = group.get("pages")
            if not isinstance(pages, list):
                errors.append("docs.json group.pages must be a list")
                continue
            for page in pages:
                page_name = str(page)
                expected = REPO_ROOT / "README.md"
                if page_name != "README":
                    expected = REPO_ROOT / f"{page_name}.md"
                if not expected.is_file():
                    errors.append(f"docs.json points to missing page: {page_name}")


def markdown_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if not target or target.startswith("#"):
        return None
    if target.startswith(EXTERNAL_LINK_PREFIXES):
        return None
    if target.startswith("<"):
        target = target[1:].split(">", 1)[0]
    else:
        target = target.split(maxsplit=1)[0]
    target = target.split("#", 1)[0].split("?", 1)[0]
    return target or None


def validate_markdown_links(errors: list[str]) -> None:
    for path in iter_repo_files():
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_PATTERN.finditer(text):
            target = markdown_link_target(match.group(1))
            if target is None:
                continue
            candidate = (path.parent / target).resolve()
            try:
                candidate.relative_to(REPO_ROOT.resolve())
            except ValueError:
                errors.append(
                    f"markdown link leaves repository: "
                    f"{path.relative_to(REPO_ROOT)} -> {target}"
                )
                continue
            if not candidate.exists():
                errors.append(
                    f"broken markdown link: "
                    f"{path.relative_to(REPO_ROOT)} -> {target}"
                )


def validate_claim_flags(errors: list[str]) -> None:
    manifest = load_json_object(DEMONSTRATOR_MANIFEST)
    claim_boundary = manifest.get("claim_boundary")
    if not isinstance(claim_boundary, dict):
        errors.append("demonstrator manifest claim_boundary must be an object")
        return

    required_false = (
        "domain_validation_claim",
        "external_validation_completed",
        "high_quality_public_effectiveness_proof_claim",
        "public_effectiveness_proof_sufficient",
        "production_runtime_claim",
        "regulated_use_claim",
        "safety_approval_claim",
    )
    for key in required_false:
        if claim_boundary.get(key) is not False:
            errors.append(f"claim flag must remain false: {key}")


def validate_integrity_manifest(errors: list[str]) -> None:
    manifest = load_json_object(INTEGRITY_MANIFEST)
    claim_boundary = manifest.get("claim_boundary")
    if not isinstance(claim_boundary, dict):
        errors.append("integrity_manifest claim_boundary must be an object")
    else:
        for key in REQUIRED_FALSE_INTEGRITY_CLAIMS:
            if claim_boundary.get(key) is not False:
                errors.append(f"integrity manifest claim flag must remain false: {key}")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("integrity_manifest artifacts must be a non-empty list")
        return
    if manifest.get("artifact_count") != len(artifacts):
        errors.append(
            "integrity_manifest artifact_count does not match artifacts length"
        )

    seen_paths: set[str] = set()
    for item in artifacts:
        if not isinstance(item, dict):
            errors.append("integrity_manifest artifact entry must be an object")
            continue
        relative_path = item.get("path")
        expected_sha = item.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(expected_sha, str):
            errors.append("integrity_manifest artifact path and sha256 must be strings")
            continue
        if "\\" in relative_path or ":" in relative_path:
            errors.append(
                "integrity_manifest path must be repo-relative: "
                f"{relative_path}"
            )
            continue
        parsed_path = PurePosixPath(relative_path)
        if parsed_path.is_absolute() or ".." in parsed_path.parts:
            errors.append(
                "integrity_manifest path must stay inside repo: "
                f"{relative_path}"
            )
            continue
        if not SHA256_PATTERN.fullmatch(expected_sha):
            errors.append(f"integrity_manifest sha256 is invalid: {relative_path}")
            continue
        if relative_path in seen_paths:
            errors.append(f"duplicate integrity_manifest artifact: {relative_path}")
        seen_paths.add(relative_path)

        path = REPO_ROOT / relative_path
        if not path.is_file():
            errors.append(f"integrity_manifest path is missing: {relative_path}")
            continue
        observed_sha = sha256_public_artifact(relative_path, path)
        if observed_sha != expected_sha:
            errors.append(
                "integrity_manifest hash mismatch for "
                f"{relative_path}: expected {expected_sha}, observed {observed_sha}"
            )

    missing_required = REQUIRED_INTEGRITY_PATHS - seen_paths
    for relative_path in sorted(missing_required):
        errors.append(
            "required public artifact missing from manifest: "
            f"{relative_path}"
        )


def git_check(
    args: list[str],
    *,
    path: str,
    expected_returncode: int,
) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args, "--", path],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == expected_returncode:
        return None
    stderr = result.stderr.strip()
    stdout = result.stdout.strip()
    detail = stderr or stdout or f"exit {result.returncode}"
    return detail


def validate_required_artifacts_are_git_visible(errors: list[str]) -> None:
    manifest = load_json_object(INTEGRITY_MANIFEST)
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return

    for item in artifacts:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            continue
        relative_path = item["path"]
        tracking_error = git_check(
            ["ls-files", "--error-unmatch"],
            path=relative_path,
            expected_returncode=0,
        )
        if tracking_error is not None:
            errors.append(
                "integrity_manifest artifact is not tracked by git: "
                f"{relative_path}"
            )
        ignore_error = git_check(
            ["check-ignore", "--no-index", "-q"],
            path=relative_path,
            expected_returncode=1,
        )
        if ignore_error is not None:
            errors.append(
                "integrity_manifest artifact matches .gitignore: "
                f"{relative_path}"
            )


def validate_operational_replay_artifact(errors: list[str]) -> None:
    metrics_path = (
        REPO_ROOT / "benchmarks/results/operational_control_replay_metrics.json"
    )
    summary_path = (
        REPO_ROOT / "benchmarks/results/operational_control_replay_summary.md"
    )
    metrics = load_json_object(metrics_path)
    summary = summary_path.read_text(encoding="utf-8")

    if metrics.get("schema_version") != "operational-control-replay/v1":
        errors.append("operational replay metrics schema mismatch")
    if "Production-Relevant Proof Profile" not in summary:
        errors.append("operational replay summary missing proof profile")
    if "Falsification Criteria" not in summary:
        errors.append("operational replay summary missing falsification criteria")

    claim_boundary = metrics.get("claim_boundary")
    if not isinstance(claim_boundary, dict):
        errors.append("operational replay claim_boundary must be an object")
    else:
        for key in (
            "production_deployment_claim",
            "production_sla_claim",
            "regulated_use_claim",
            "domain_validation_claim",
            "external_validation_claim",
            "general_aos_effectiveness_claim",
        ):
            if claim_boundary.get(key) is not False:
                errors.append(f"operational replay claim flag must remain false: {key}")

    for profile in (
        "production_relevance_profile",
        "scalability_profile",
        "auditability_profile",
        "falsification_profile",
    ):
        if not isinstance(metrics.get(profile), dict):
            errors.append(f"operational replay metrics missing {profile}")

    production_relevance = metrics.get("production_relevance_profile", {})
    if isinstance(production_relevance, dict):
        if production_relevance.get("claim_type") != (
            "production_relevant_offline_replay"
        ):
            errors.append("operational replay claim type changed")
        if production_relevance.get("labels_used_as_aos_input_signals") is not False:
            errors.append("operational replay must not use labels as AOS input signals")

    scalability = metrics.get("scalability_profile", {})
    if isinstance(scalability, dict):
        if scalability.get("evaluated_record_count") != metrics.get(
            "evaluated_record_count"
        ):
            errors.append("operational replay scalability record count mismatch")
        if scalability.get("gate_complexity_per_signal") != "O(1)":
            errors.append("operational replay gate complexity changed")

    guards = metrics.get("guards")
    aos_guard = None
    if isinstance(guards, list):
        aos_guard = next(
            (
                guard
                for guard in guards
                if isinstance(guard, dict) and guard.get("name") == "aos_control_gate"
            ),
            None,
        )
    if not isinstance(aos_guard, dict):
        errors.append("operational replay missing aos_control_gate metrics")
        return
    if aos_guard.get("audit_coverage_rate") != 1.0:
        errors.append("operational replay AOS audit coverage must be 1.0")
    if aos_guard.get("replay_success_rate") != 1.0:
        errors.append("operational replay AOS replay success must be 1.0")
    if float(aos_guard.get("anomaly_window_review_or_block_rate", 0.0)) < 0.9:
        errors.append("operational replay AOS review/block rate below threshold")
    if float(aos_guard.get("anomaly_window_silent_pass_rate", 1.0)) > 0.1:
        errors.append("operational replay AOS silent pass rate above threshold")


def validate_lean_sources(errors: list[str]) -> None:
    lean_paths = [REPO_ROOT / "lakefile.lean", *(REPO_ROOT / "lean").rglob("*.lean")]
    for path in lean_paths:
        text = path.read_text(encoding="utf-8")
        for term in LEAN_GAP_TERMS:
            if re.search(rf"\b{term}\b", text):
                errors.append(
                    f"Lean gap term {term!r} in {path.relative_to(REPO_ROOT)}"
                )


def main() -> int:
    errors: list[str] = []
    validate_all_json(errors)
    validate_docs_navigation(errors)
    validate_markdown_links(errors)
    validate_claim_flags(errors)
    validate_integrity_manifest(errors)
    validate_required_artifacts_are_git_visible(errors)
    validate_operational_replay_artifact(errors)
    validate_lean_sources(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("public integrity check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
