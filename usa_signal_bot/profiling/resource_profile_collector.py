import time
from pathlib import Path
from typing import Any

from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus, ResourceMetricName
from usa_signal_bot.profiling.profiling_models import ResourceProfile, ResourceMetric, create_resource_profile_id, create_resource_metric_id
from usa_signal_bot.profiling.resource_timer import current_utc_iso
from usa_signal_bot.profiling.artifact_growth import measure_artifact_footprint

class ResourceProfileCollector:
    def __init__(self, data_root: Path, project_root: Path | None = None):
        self.data_root = data_root
        self.project_root = project_root

    def profile_noop(self, scope: ResourceProfileScope = ResourceProfileScope.CUSTOM) -> ResourceProfile:
        started = current_utc_iso()

        time.sleep(0.001)

        return ResourceProfile(
            profile_id=create_resource_profile_id(),
            scope=scope,
            target_name="noop",
            status=ResourceProfileStatus.COMPLETED,
            started_at_utc=started,
            completed_at_utc=current_utc_iso(),
            wall_time_seconds=0.001,
            process_time_seconds=0.001,
            memory_current_bytes=None,
            memory_peak_bytes=None,
            artifact_size_bytes=0,
            artifact_file_count=0,
            output_growth_bytes=0,
            output_growth_files=0,
            metrics=[],
            warnings=[],
            errors=[],
            metadata={"collector": "ResourceProfileCollector"}
        )

    def profile_artifact_path(self, path: Path, scope: ResourceProfileScope, target_name: str) -> ResourceProfile:
        started = current_utc_iso()
        footprint = measure_artifact_footprint(path)
        completed = current_utc_iso()

        metrics = []
        if footprint.exists:
            metrics.append(ResourceMetric(
                metric_id=create_resource_metric_id(),
                name=ResourceMetricName.ARTIFACT_SIZE_BYTES,
                value=footprint.size_bytes,
                unit="bytes",
                status=ResourceProfileStatus.COMPLETED,
                source="profile_artifact_path",
                created_at_utc=completed
            ))

            metrics.append(ResourceMetric(
                metric_id=create_resource_metric_id(),
                name=ResourceMetricName.ARTIFACT_FILE_COUNT,
                value=footprint.file_count,
                unit="files",
                status=ResourceProfileStatus.COMPLETED,
                source="profile_artifact_path",
                created_at_utc=completed
            ))

        return ResourceProfile(
            profile_id=create_resource_profile_id(),
            scope=scope,
            target_name=target_name,
            status=ResourceProfileStatus.COMPLETED if footprint.exists else ResourceProfileStatus.WARNING,
            started_at_utc=started,
            completed_at_utc=completed,
            wall_time_seconds=0.0,
            process_time_seconds=0.0,
            memory_current_bytes=None,
            memory_peak_bytes=None,
            artifact_size_bytes=footprint.size_bytes if footprint.exists else None,
            artifact_file_count=footprint.file_count if footprint.exists else None,
            output_growth_bytes=None,
            output_growth_files=None,
            metrics=metrics,
            warnings=footprint.warnings,
            errors=footprint.errors,
            metadata={"path": footprint.path}
        )

    def profile_existing_run_artifacts(self, scope: ResourceProfileScope | None = None) -> list[ResourceProfile]:
        return []

    def profile_task_simulation(self, task: Any) -> ResourceProfile:
        return self.profile_noop(ResourceProfileScope.TASK)

    def profile_command_dry_run(self, command_name: str) -> ResourceProfile:
        profile = self.profile_noop(ResourceProfileScope.COMMAND)
        profile.target_name = command_name
        profile.warnings.append("Dry-run execution - true resource bounds are estimates.")
        return profile

    def collect_lightweight_snapshot(self) -> list[ResourceProfile]:
        profiles = []
        profiles.append(self.profile_noop(ResourceProfileScope.OBSERVABILITY))

        if self.data_root.exists():
            profiles.append(self.profile_artifact_path(self.data_root, ResourceProfileScope.OBSERVABILITY, "data_root"))

        return profiles
