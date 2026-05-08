from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import uuid
from usa_signal_bot.core.enums import ReleaseStatus, ReleaseArtifactType, ReleaseValidationStatus

@dataclass
class ReleaseVersion:
    version: str
    build_id: str
    created_at_utc: str
    git_commit: Optional[str] = None
    git_branch: Optional[str] = None
    python_version: Optional[str] = None
    platform: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReleaseArtifact:
    artifact_id: str
    artifact_type: ReleaseArtifactType
    name: str
    source_path: str
    target_path: str
    size_bytes: Optional[int]
    checksum: Optional[str]
    included: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class ReleaseManifest:
    manifest_id: str
    release_name: str
    version: ReleaseVersion
    status: ReleaseStatus
    created_at_utc: str
    artifacts: List[ReleaseArtifact]
    artifact_count: int
    total_size_bytes: int
    checksum: Optional[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReleaseBuildRequest:
    request_id: str
    release_name: str
    output_dir: str
    include_docs: bool = True
    include_tests: bool = True
    include_reports: bool = True
    include_data_cache: bool = False
    include_backups: bool = False
    include_secrets: bool = False
    validate_after_build: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ReleaseBuildResult:
    build_id: str
    created_at_utc: str
    status: ReleaseStatus
    request: ReleaseBuildRequest
    manifest: Optional[ReleaseManifest]
    bundle_path: Optional[str]
    validation_status: ReleaseValidationStatus
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class OperatorRunbook:
    runbook_id: str
    created_at_utc: str
    title: str
    sections: Dict[str, str] = field(default_factory=dict)
    command_reference: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_release_build_id(prefix: str = "release") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_release_manifest_id(prefix: str = "manifest") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_release_artifact_id(name: str) -> str:
    return f"art_{uuid.uuid4().hex[:8]}"

def create_runbook_id(prefix: str = "runbook") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def validate_release_version(version: ReleaseVersion) -> None:
    if not version.version or not version.build_id:
        raise ValueError("version and build_id are required")

def validate_release_artifact(artifact: ReleaseArtifact) -> None:
    if not artifact.source_path or not artifact.target_path:
        raise ValueError("source_path and target_path are required")

def validate_release_manifest(manifest: ReleaseManifest) -> None:
    if not manifest.release_name:
        raise ValueError("release_name is required")

def validate_release_build_request(request: ReleaseBuildRequest) -> None:
    if request.include_secrets:
        raise ValueError("include_secrets must be False")
    if not request.release_name or not request.output_dir:
        raise ValueError("release_name and output_dir are required")

def validate_release_build_result(result: ReleaseBuildResult) -> None:
    if result.status == ReleaseStatus.BUILT and not result.bundle_path:
        raise ValueError("bundle_path is required when status is BUILT")

def release_version_to_dict(version: ReleaseVersion) -> dict:
    return {
        "version": version.version,
        "build_id": version.build_id,
        "created_at_utc": version.created_at_utc,
        "git_commit": version.git_commit,
        "git_branch": version.git_branch,
        "python_version": version.python_version,
        "platform": version.platform,
        "metadata": version.metadata
    }

def release_artifact_to_dict(artifact: ReleaseArtifact) -> dict:
    return {
        "artifact_id": artifact.artifact_id,
        "artifact_type": artifact.artifact_type.value,
        "name": artifact.name,
        "source_path": artifact.source_path,
        "target_path": artifact.target_path,
        "size_bytes": artifact.size_bytes,
        "checksum": artifact.checksum,
        "included": artifact.included,
        "warnings": artifact.warnings,
        "errors": artifact.errors
    }

def release_manifest_to_dict(manifest: ReleaseManifest) -> dict:
    return {
        "manifest_id": manifest.manifest_id,
        "release_name": manifest.release_name,
        "version": release_version_to_dict(manifest.version),
        "status": manifest.status.value,
        "created_at_utc": manifest.created_at_utc,
        "artifacts": [release_artifact_to_dict(a) for a in manifest.artifacts],
        "artifact_count": manifest.artifact_count,
        "total_size_bytes": manifest.total_size_bytes,
        "checksum": manifest.checksum,
        "warnings": manifest.warnings,
        "errors": manifest.errors,
        "metadata": manifest.metadata
    }

def release_build_request_to_dict(request: ReleaseBuildRequest) -> dict:
    return {
        "request_id": request.request_id,
        "release_name": request.release_name,
        "output_dir": request.output_dir,
        "include_docs": request.include_docs,
        "include_tests": request.include_tests,
        "include_reports": request.include_reports,
        "include_data_cache": request.include_data_cache,
        "include_backups": request.include_backups,
        "include_secrets": request.include_secrets,
        "validate_after_build": request.validate_after_build,
        "metadata": request.metadata
    }

def release_build_result_to_dict(result: ReleaseBuildResult) -> dict:
    return {
        "build_id": result.build_id,
        "created_at_utc": result.created_at_utc,
        "status": result.status.value,
        "request": release_build_request_to_dict(result.request),
        "manifest": release_manifest_to_dict(result.manifest) if result.manifest else None,
        "bundle_path": result.bundle_path,
        "validation_status": result.validation_status.value,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }

def operator_runbook_to_dict(runbook: OperatorRunbook) -> dict:
    return {
        "runbook_id": runbook.runbook_id,
        "created_at_utc": runbook.created_at_utc,
        "title": runbook.title,
        "sections": runbook.sections,
        "command_reference": runbook.command_reference,
        "warnings": runbook.warnings,
        "errors": runbook.errors
    }
