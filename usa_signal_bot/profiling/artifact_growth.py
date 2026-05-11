from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from usa_signal_bot.core.enums import ResourceMetricName, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceMetric, create_resource_metric_id
from usa_signal_bot.profiling.resource_timer import current_utc_iso

@dataclass
class ArtifactFootprint:
    path: str
    exists: bool
    size_bytes: int
    file_count: int
    dir_count: int
    measured_at_utc: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def measure_artifact_footprint(path: Path, max_files: int | None = None) -> ArtifactFootprint:
    resolved_path = path.resolve()
    path_str = str(resolved_path)

    if "secret" in path_str.lower() or "token" in path_str.lower():
        path_str = "***REDACTED***"

    footprint = ArtifactFootprint(
        path=path_str,
        exists=resolved_path.exists(),
        size_bytes=0,
        file_count=0,
        dir_count=0,
        measured_at_utc=current_utc_iso()
    )

    if not footprint.exists:
        return footprint

    try:
        if resolved_path.is_file():
            footprint.size_bytes = resolved_path.stat().st_size
            footprint.file_count = 1
            return footprint

        for item in resolved_path.rglob("*"):
            if max_files is not None and footprint.file_count + footprint.dir_count >= max_files:
                footprint.warnings.append(f"Max files limit ({max_files}) reached. Measurement is incomplete.")
                break

            try:
                if item.is_file():
                    footprint.size_bytes += item.stat().st_size
                    footprint.file_count += 1
                elif item.is_dir():
                    footprint.dir_count += 1
            except Exception as e:
                footprint.warnings.append(f"Could not stat {item.name}: {str(e)}")
    except Exception as e:
        footprint.errors.append(f"Failed to measure footprint: {str(e)}")

    return footprint

def compare_artifact_footprints(before: ArtifactFootprint, after: ArtifactFootprint) -> dict[str, Any]:
    diff = {
        "path": before.path,
        "size_bytes_diff": after.size_bytes - before.size_bytes,
        "file_count_diff": after.file_count - before.file_count,
        "dir_count_diff": after.dir_count - before.dir_count,
        "measured_interval": f"{before.measured_at_utc} to {after.measured_at_utc}",
        "warnings": list(set(before.warnings + after.warnings)),
        "errors": list(set(before.errors + after.errors))
    }
    return diff

def artifact_footprint_to_dict(footprint: ArtifactFootprint) -> dict:
    return {
        "path": footprint.path,
        "exists": footprint.exists,
        "size_bytes": footprint.size_bytes,
        "file_count": footprint.file_count,
        "dir_count": footprint.dir_count,
        "measured_at_utc": footprint.measured_at_utc,
        "warnings": footprint.warnings,
        "errors": footprint.errors
    }

def artifact_growth_metrics(before: ArtifactFootprint, after: ArtifactFootprint, source: str) -> list[ResourceMetric]:
    diff = compare_artifact_footprints(before, after)
    metrics = []
    created_at = current_utc_iso()
    status = ResourceProfileStatus.COMPLETED if not diff["errors"] else ResourceProfileStatus.FAILED

    metrics.append(ResourceMetric(
        metric_id=create_resource_metric_id(),
        name=ResourceMetricName.OUTPUT_GROWTH_BYTES,
        value=diff["size_bytes_diff"],
        unit="bytes",
        status=status,
        source=source,
        created_at_utc=created_at
    ))

    metrics.append(ResourceMetric(
        metric_id=create_resource_metric_id(),
        name=ResourceMetricName.OUTPUT_GROWTH_FILES,
        value=diff["file_count_diff"],
        unit="files",
        status=status,
        source=source,
        created_at_utc=created_at
    ))

    return metrics

def artifact_footprint_to_text(footprint: ArtifactFootprint) -> str:
    if not footprint.exists:
        return f"Artifact Footprint ({footprint.path}): Path does not exist."

    size_mb = footprint.size_bytes / (1024 * 1024)
    return (
        f"Artifact Footprint ({footprint.path}): "
        f"{size_mb:.2f} MB across {footprint.file_count} files and {footprint.dir_count} dirs."
    )

def artifact_growth_to_text(diff: dict[str, Any]) -> str:
    size_mb = diff['size_bytes_diff'] / (1024 * 1024)
    return (
        f"Artifact Growth ({diff['path']}): "
        f"{size_mb:+.2f} MB, {diff['file_count_diff']:+} files."
    )
