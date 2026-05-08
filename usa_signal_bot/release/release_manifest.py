import hashlib
import json
from pathlib import Path
from typing import List, Any
from usa_signal_bot.release.release_models import ReleaseArtifact, ReleaseManifest, ReleaseVersion, create_release_manifest_id, create_release_artifact_id, release_manifest_to_dict
from usa_signal_bot.core.enums import ReleaseArtifactType, ReleaseStatus

def calculate_file_checksum(path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def calculate_directory_checksum(paths: List[Path]) -> str:
    sha256_hash = hashlib.sha256()
    sorted_paths = sorted(paths)
    for path in sorted_paths:
        if path.is_file():
            sha256_hash.update(path.name.encode('utf-8'))
            with open(path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def build_release_artifact(source_path: Path, target_path: str, artifact_type: ReleaseArtifactType, included: bool = True) -> ReleaseArtifact:
    size = source_path.stat().st_size if source_path.exists() and source_path.is_file() else None
    checksum = calculate_file_checksum(source_path) if source_path.exists() and source_path.is_file() else None

    return ReleaseArtifact(
        artifact_id=create_release_artifact_id(source_path.name),
        artifact_type=artifact_type,
        name=source_path.name,
        source_path=str(source_path),
        target_path=target_path,
        size_bytes=size,
        checksum=checksum,
        included=included
    )

def build_release_manifest(release_name: str, version: ReleaseVersion, artifacts: List[ReleaseArtifact]) -> ReleaseManifest:
    included_artifacts = [a for a in artifacts if a.included]
    total_size = sum(a.size_bytes for a in included_artifacts if a.size_bytes)

    return ReleaseManifest(
        manifest_id=create_release_manifest_id(),
        release_name=release_name,
        version=version,
        status=ReleaseStatus.CREATED,
        created_at_utc=version.created_at_utc,
        artifacts=included_artifacts,
        artifact_count=len(included_artifacts),
        total_size_bytes=total_size,
        checksum=None, # To be computed after bundle creation if needed
        warnings=[],
        errors=[]
    )

def release_manifest_to_markdown(manifest: ReleaseManifest) -> str:
    lines = [
        f"# Release Manifest: {manifest.release_name}",
        f"**Version**: {manifest.version.version}",
        f"**Build ID**: {manifest.version.build_id}",
        f"**Date**: {manifest.created_at_utc}",
        f"**Status**: {manifest.status.value}",
        "",
        "## Included Artifacts",
        "| Type | Target Path | Size (Bytes) | Checksum |",
        "|---|---|---|---|"
    ]
    for art in manifest.artifacts:
        lines.append(f"| {art.artifact_type.value} | `{art.target_path}` | {art.size_bytes} | `{art.checksum}` |")

    lines.extend([
        "",
        "## Summary",
        f"- Total Artifacts: {manifest.artifact_count}",
        f"- Total Size (Bytes): {manifest.total_size_bytes}"
    ])
    return "\n".join(lines)

def write_release_manifest_json(path: Path, manifest: ReleaseManifest) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(release_manifest_to_dict(manifest), f, indent=2)
    return path

def write_release_manifest_markdown(path: Path, manifest: ReleaseManifest) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(release_manifest_to_markdown(manifest))
    return path

def read_release_manifest_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
