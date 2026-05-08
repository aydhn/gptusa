from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import datetime
from usa_signal_bot.release.release_models import ReleaseArtifact, ReleaseBuildRequest
from usa_signal_bot.core.enums import ReleaseArtifactType
from usa_signal_bot.release.release_manifest import build_release_artifact

@dataclass
class ReleaseArtifactCollection:
    created_at_utc: str
    project_root: str
    artifacts: List[ReleaseArtifact]
    excluded_paths: List[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def is_secret_like_path(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.startswith('.env') or
        name.endswith('.key') or
        'token' in name or
        'secret' in name or
        'credentials' in name or
        'password' in name
    )

def should_exclude_path(path: Path) -> bool:
    if is_secret_like_path(path):
        return True
    parts = path.parts
    if '__pycache__' in parts or '.pytest_cache' in parts or '.git' in parts:
        return True
    return False

def collect_source_artifacts(project_root: Path) -> List[ReleaseArtifact]:
    artifacts = []
    source_dir = project_root / "usa_signal_bot"
    if source_dir.exists():
        for file in source_dir.rglob("*"):
            if file.is_file() and not should_exclude_path(file) and file.suffix == ".py":
                rel_path = file.relative_to(project_root)
                artifacts.append(build_release_artifact(file, str(rel_path), ReleaseArtifactType.SOURCE_CODE))
    return artifacts

def collect_config_artifacts(project_root: Path, include_secrets: bool = False) -> List[ReleaseArtifact]:
    artifacts = []
    config_dir = project_root / "config"
    if config_dir.exists():
        for file in config_dir.rglob("*"):
            if file.is_file():
                if not include_secrets and is_secret_like_path(file):
                    continue
                if should_exclude_path(file) and not is_secret_like_path(file):
                    continue
                rel_path = file.relative_to(project_root)
                artifacts.append(build_release_artifact(file, str(rel_path), ReleaseArtifactType.CONFIG))
    return artifacts

def collect_docs_artifacts(project_root: Path) -> List[ReleaseArtifact]:
    artifacts = []
    docs_dir = project_root / "docs"
    if docs_dir.exists():
        for file in docs_dir.rglob("*"):
            if file.is_file() and not should_exclude_path(file):
                rel_path = file.relative_to(project_root)
                artifacts.append(build_release_artifact(file, str(rel_path), ReleaseArtifactType.DOCS))
    return artifacts

def collect_tests_artifacts(project_root: Path) -> List[ReleaseArtifact]:
    artifacts = []
    tests_dir = project_root / "tests"
    if tests_dir.exists():
        for file in tests_dir.rglob("*"):
            if file.is_file() and not should_exclude_path(file):
                rel_path = file.relative_to(project_root)
                artifacts.append(build_release_artifact(file, str(rel_path), ReleaseArtifactType.TESTS))
    return artifacts

def collect_report_artifacts(project_root: Path, data_root: Optional[Path] = None) -> List[ReleaseArtifact]:
    artifacts = []
    data_dir = data_root if data_root else project_root / "data"

    # Regression
    reg_dir = data_dir / "reports/regression"
    if reg_dir.exists():
        files = list(reg_dir.glob("*.json"))
        if files:
            latest = max(files, key=lambda f: f.stat().st_mtime)
            rel_path = latest.relative_to(project_root) if data_dir.is_relative_to(project_root) else latest.name
            artifacts.append(build_release_artifact(latest, str(rel_path), ReleaseArtifactType.REGRESSION_REPORT))

    # Quality
    qual_dir = data_dir / "reports/quality"
    if qual_dir.exists():
        files = list(qual_dir.glob("scorecard_*.json"))
        if files:
            latest = max(files, key=lambda f: f.stat().st_mtime)
            rel_path = latest.relative_to(project_root) if data_dir.is_relative_to(project_root) else latest.name
            artifacts.append(build_release_artifact(latest, str(rel_path), ReleaseArtifactType.QUALITY_REPORT))

    return artifacts

def collect_release_artifacts(project_root: Path, request: ReleaseBuildRequest) -> ReleaseArtifactCollection:
    artifacts = []
    excluded_paths = []

    # Base dependencies
    req_file = project_root / "requirements.txt"
    if req_file.exists():
        artifacts.append(build_release_artifact(req_file, "requirements.txt", ReleaseArtifactType.REQUIREMENTS))

    artifacts.extend(collect_source_artifacts(project_root))
    artifacts.extend(collect_config_artifacts(project_root, request.include_secrets))

    if request.include_docs:
        artifacts.extend(collect_docs_artifacts(project_root))
    if request.include_tests:
        artifacts.extend(collect_tests_artifacts(project_root))
    if request.include_reports:
        # Note: assumes data root is project_root / "data" for now
        artifacts.extend(collect_report_artifacts(project_root))

    return ReleaseArtifactCollection(
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        project_root=str(project_root),
        artifacts=artifacts,
        excluded_paths=excluded_paths
    )

def artifact_collection_to_dict(collection: ReleaseArtifactCollection) -> dict:
    from usa_signal_bot.release.release_models import release_artifact_to_dict
    return {
        "created_at_utc": collection.created_at_utc,
        "project_root": collection.project_root,
        "artifacts": [release_artifact_to_dict(a) for a in collection.artifacts],
        "excluded_paths": collection.excluded_paths,
        "warnings": collection.warnings,
        "errors": collection.errors
    }

def artifact_collection_to_text(collection: ReleaseArtifactCollection) -> str:
    lines = [
        f"Artifact Collection (Root: {collection.project_root})",
        f"Created At: {collection.created_at_utc}",
        f"Total Artifacts: {len(collection.artifacts)}",
        f"Excluded Paths: {len(collection.excluded_paths)}"
    ]
    return "\n".join(lines)
