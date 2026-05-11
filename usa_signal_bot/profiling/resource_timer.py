import time
from datetime import datetime, timezone
from typing import Any, Callable

from usa_signal_bot.core.enums import (
    ResourceProfileStatus,
    ResourceProfileScope,
    ResourceMetricName
)
from usa_signal_bot.profiling.profiling_models import (
    ResourceMetric,
    ResourceProfile,
    create_resource_metric_id,
    create_resource_profile_id
)

def current_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class ResourceTimer:
    def __init__(
        self,
        scope: ResourceProfileScope,
        target_name: str,
        metadata: dict[str, Any] | None = None
    ):
        self.scope = scope
        self.target_name = target_name

        # Redact secrets from metadata if present
        safe_metadata = dict(metadata) if metadata else {}
        for key in ["token", "secret", "api_key", "password"]:
            for k in list(safe_metadata.keys()):
                if key in k.lower():
                    safe_metadata[k] = "***REDACTED***"

        self.metadata = safe_metadata
        self.profile_id = create_resource_profile_id()
        self.status = ResourceProfileStatus.CREATED
        self.started_at_utc: str | None = None
        self.completed_at_utc: str | None = None
        self.wall_time_seconds: float | None = None
        self.process_time_seconds: float | None = None
        self.warnings: list[str] = []
        self.errors: list[str] = []

        self._start_perf: float | None = None
        self._start_process: float | None = None

    def __enter__(self):
        self.status = ResourceProfileStatus.RUNNING
        self.started_at_utc = current_utc_iso()
        self._start_perf = time.perf_counter()
        self._start_process = time.process_time()
        return self

    def __exit__(self, exc_type, exc, tb):
        end_perf = time.perf_counter()
        end_process = time.process_time()

        if self._start_perf is not None:
            self.wall_time_seconds = end_perf - self._start_perf
        if self._start_process is not None:
            self.process_time_seconds = end_process - self._start_process

        self.completed_at_utc = current_utc_iso()

        if exc_type is not None:
            self.status = ResourceProfileStatus.FAILED
            self.errors.append(f"Execution failed with {exc_type.__name__}: {str(exc)}")
        else:
            self.status = ResourceProfileStatus.COMPLETED

    def to_profile(self) -> ResourceProfile:
        metrics = build_timing_metrics(self)

        return ResourceProfile(
            profile_id=self.profile_id,
            scope=self.scope,
            target_name=self.target_name,
            status=self.status,
            started_at_utc=self.started_at_utc,
            completed_at_utc=self.completed_at_utc,
            wall_time_seconds=self.wall_time_seconds,
            process_time_seconds=self.process_time_seconds,
            memory_current_bytes=None,
            memory_peak_bytes=None,
            artifact_size_bytes=None,
            artifact_file_count=None,
            output_growth_bytes=None,
            output_growth_files=None,
            metrics=metrics,
            warnings=list(self.warnings),
            errors=list(self.errors),
            metadata=dict(self.metadata)
        )

def build_timing_metrics(timer: ResourceTimer) -> list[ResourceMetric]:
    metrics = []
    created_at = current_utc_iso()

    if timer.wall_time_seconds is not None:
        metrics.append(ResourceMetric(
            metric_id=create_resource_metric_id(),
            name=ResourceMetricName.WALL_TIME_SECONDS,
            value=timer.wall_time_seconds,
            unit="seconds",
            status=timer.status,
            source="ResourceTimer",
            created_at_utc=created_at
        ))

    if timer.process_time_seconds is not None:
        metrics.append(ResourceMetric(
            metric_id=create_resource_metric_id(),
            name=ResourceMetricName.PROCESS_TIME_SECONDS,
            value=timer.process_time_seconds,
            unit="seconds",
            status=timer.status,
            source="ResourceTimer",
            created_at_utc=created_at
        ))

    return metrics

def measure_callable(fn: Callable, scope: ResourceProfileScope, target_name: str, *args, **kwargs) -> tuple[Any, ResourceProfile]:
    with ResourceTimer(scope, target_name, metadata={"fn_name": fn.__name__}) as timer:
        result = fn(*args, **kwargs)
    return result, timer.to_profile()

def resource_timer_summary_to_text(profile: ResourceProfile) -> str:
    lines = [
        f"Profile: {profile.target_name} ({profile.scope.value})",
        f"Status: {profile.status.value}",
        f"Wall Time: {profile.wall_time_seconds:.4f}s" if profile.wall_time_seconds is not None else "Wall Time: N/A",
        f"Process Time: {profile.process_time_seconds:.4f}s" if profile.process_time_seconds is not None else "Process Time: N/A"
    ]
    if profile.errors:
        lines.append(f"Errors: {len(profile.errors)}")
    return "\n".join(lines)
