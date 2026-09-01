import logging
import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.enums import ResourceProfileScope, ResourceMetricName, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceProfile, ResourceMetric
from usa_signal_bot.profiling.profiling_store import resource_profiles_dir, read_resource_profile_json

def load_profiles_from_store(data_root: Path, scope: ResourceProfileScope | None = None, limit: int | None = None) -> list[ResourceProfile]:
    profiles_dir = resource_profiles_dir(data_root)
    if not profiles_dir.exists():
        return []

    profiles = []
    for profile_path in profiles_dir.glob("*.json"):
        try:
            profile_dict = read_resource_profile_json(profile_path)

            metrics = []
            for m in profile_dict.get("metrics", []):
                metrics.append(ResourceMetric(
                    metric_id=m["metric_id"],
                    name=ResourceMetricName(m["name"]),
                    value=m["value"],
                    unit=m["unit"],
                    status=ResourceProfileStatus(m["status"]),
                    source=m["source"],
                    created_at_utc=m["created_at_utc"],
                    metadata=m.get("metadata", {})
                ))

            profile = ResourceProfile(
                profile_id=profile_dict["profile_id"],
                scope=ResourceProfileScope(profile_dict["scope"]),
                target_name=profile_dict["target_name"],
                status=ResourceProfileStatus(profile_dict["status"]),
                started_at_utc=profile_dict.get("started_at_utc"),
                completed_at_utc=profile_dict.get("completed_at_utc"),
                wall_time_seconds=profile_dict.get("wall_time_seconds"),
                process_time_seconds=profile_dict.get("process_time_seconds"),
                memory_current_bytes=profile_dict.get("memory_current_bytes"),
                memory_peak_bytes=profile_dict.get("memory_peak_bytes"),
                artifact_size_bytes=profile_dict.get("artifact_size_bytes"),
                artifact_file_count=profile_dict.get("artifact_file_count"),
                output_growth_bytes=profile_dict.get("output_growth_bytes"),
                output_growth_files=profile_dict.get("output_growth_files"),
                metrics=metrics,
                warnings=profile_dict.get("warnings", []),
                errors=profile_dict.get("errors", []),
                metadata=profile_dict.get("metadata", {})
            )

            if scope is None or profile.scope == scope:
                profiles.append(profile)
        except Exception as e:
            logging.warning(f"Failed to load profile {profile_path}: {e}")

    profiles.sort(key=lambda p: p.started_at_utc or "", reverse=True)
    if limit is not None:
        profiles = profiles[:limit]

    return profiles

def load_runtime_duration_metrics(data_root: Path) -> list[dict[str, Any]]:
    return []

def load_taskqueue_run_metrics(data_root: Path) -> list[dict[str, Any]]:
    return []

def load_scheduler_run_metrics(data_root: Path) -> list[dict[str, Any]]:
    return []

def load_observability_metrics(data_root: Path) -> list[dict[str, Any]]:
    return []

def extract_duration_values(records: list[dict[str, Any]]) -> list[float]:
    values = []
    for r in records:
        val = r.get("duration_seconds")
        if isinstance(val, (int, float)):
            values.append(float(val))
    return values

def extract_artifact_growth_values(records: list[dict[str, Any]]) -> list[int]:
    values = []
    for r in records:
        val = r.get("output_growth_bytes")
        if isinstance(val, int):
            values.append(val)
    return values

def summarize_historical_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(records),
        "has_records": len(records) > 0
    }
