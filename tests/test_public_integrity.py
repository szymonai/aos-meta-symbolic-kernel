from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def public_artifact_bytes(relative_path: str, path: Path) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show", f":{relative_path}"],
        check=False,
        capture_output=True,
    )
    if result.returncode == 0:
        return result.stdout
    return path.read_bytes()


def test_integrity_manifest_hashes_match_current_artifacts() -> None:
    manifest_path = REPO_ROOT / "evidence" / "integrity_manifest.json"
    with manifest_path.open(encoding="utf-8") as file:
        manifest = json.load(file)

    assert manifest["schema_version"] == "aos-public-integrity-manifest/v1"
    assert manifest["repository_role"] == "limited_public_demonstrator"

    artifacts = manifest["artifacts"]
    assert isinstance(artifacts, list)
    assert artifacts

    seen_paths: set[str] = set()
    for artifact in artifacts:
        relative_path = artifact["path"]
        expected_sha = artifact["sha256"]
        assert relative_path not in seen_paths
        seen_paths.add(relative_path)

        path = REPO_ROOT / relative_path
        assert path.is_file(), relative_path
        observed_sha = hashlib.sha256(
            public_artifact_bytes(relative_path, path)
        ).hexdigest()
        assert observed_sha == expected_sha, relative_path


def test_public_integrity_script_passes() -> None:
    subprocess.run(
        [sys.executable, "tools/verify_public_integrity.py"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
