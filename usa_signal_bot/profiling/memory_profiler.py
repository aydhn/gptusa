import tracemalloc
from typing import Any, Callable

from usa_signal_bot.core.enums import ResourceMetricName, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceMetric, create_resource_metric_id
from usa_signal_bot.profiling.resource_timer import current_utc_iso

class TracemallocProfiler:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._was_tracing = False

    def start(self) -> None:
        if not self.enabled:
            return
        self._was_tracing = tracemalloc.is_tracing()
        if not self._was_tracing:
            tracemalloc.start()
        else:
            pass

    def stop(self) -> dict[str, int | None]:
        if not self.enabled:
            return {"current": None, "peak": None}

        current, peak = tracemalloc.get_traced_memory()

        if not self._was_tracing:
            tracemalloc.stop()

        return {"current": current, "peak": peak}

    def snapshot(self) -> dict[str, int | None]:
        if not self.enabled or not tracemalloc.is_tracing():
            return {"current": None, "peak": None}
        current, peak = tracemalloc.get_traced_memory()
        return {"current": current, "peak": peak}

    def is_active(self) -> bool:
        return self.enabled and tracemalloc.is_tracing()

def profile_memory_for_callable(fn: Callable, *args, **kwargs) -> tuple[Any, dict[str, int | None]]:
    profiler = TracemallocProfiler()
    profiler.start()
    try:
        result = fn(*args, **kwargs)
        memory = profiler.stop()
        return result, memory
    except Exception as e:
        memory = profiler.stop()
        raise e

def memory_metrics_from_snapshot(snapshot: dict[str, int | None], source: str) -> list[ResourceMetric]:
    metrics = []
    created_at = current_utc_iso()

    if snapshot.get("current") is not None:
        metrics.append(ResourceMetric(
            metric_id=create_resource_metric_id(),
            name=ResourceMetricName.MEMORY_CURRENT_BYTES,
            value=snapshot["current"],
            unit="bytes",
            status=ResourceProfileStatus.COMPLETED,
            source=source,
            created_at_utc=created_at
        ))

    if snapshot.get("peak") is not None:
        metrics.append(ResourceMetric(
            metric_id=create_resource_metric_id(),
            name=ResourceMetricName.MEMORY_PEAK_BYTES,
            value=snapshot["peak"],
            unit="bytes",
            status=ResourceProfileStatus.COMPLETED,
            source=source,
            created_at_utc=created_at
        ))

    return metrics

def memory_profile_to_text(snapshot: dict[str, int | None]) -> str:
    if snapshot.get("current") is None or snapshot.get("peak") is None:
        return "Memory Profile: Disabled or Unavailable"

    current_mb = snapshot["current"] / (1024 * 1024)
    peak_mb = snapshot["peak"] / (1024 * 1024)

    return f"Memory Profile (Approx) - Current: {current_mb:.2f} MB, Peak: {peak_mb:.2f} MB"
