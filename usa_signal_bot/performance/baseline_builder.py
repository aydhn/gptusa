from datetime import datetime, timezone
import statistics
from typing import List, Optional

from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName, BaselineStatus
from usa_signal_bot.performance.baseline_models import (
    PerformanceBaseline,
    PerformanceMetricBaseline,
    CurrentPerformanceSample,
    create_performance_metric_baseline_id,
    create_performance_baseline_id
)
from usa_signal_bot.performance.baseline_versioning import create_baseline_version

def supported_metric_names_for_scope(scope: PerformanceBaselineScope) -> List[PerformanceMetricName]:
    return [
        PerformanceMetricName.WALL_TIME_SECONDS,
        PerformanceMetricName.PROCESS_TIME_SECONDS,
        PerformanceMetricName.MEMORY_PEAK_MB,
        PerformanceMetricName.MEMORY_CURRENT_MB,
        PerformanceMetricName.OUTPUT_SIZE_MB,
        PerformanceMetricName.OUTPUT_GROWTH_MB,
        PerformanceMetricName.ERROR_COUNT,
        PerformanceMetricName.WARNING_COUNT
    ]

def calculate_percentile(values: List[float], percentile: float) -> Optional[float]:
    if not values:
        return None
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    k = (n - 1) * (percentile / 100.0)
    f = int(k)
    c = min(f + 1, n - 1)
    if f == c:
        return float(sorted_vals[f])
    d0 = sorted_vals[f] * (c - k)
    d1 = sorted_vals[c] * (k - f)
    return float(d0 + d1)

def metric_values_from_samples(samples: List[CurrentPerformanceSample], metric_name: PerformanceMetricName) -> List[float]:
    values = []
    for s in samples:
        v = s.metrics.get(metric_name.value)
        if v is not None and isinstance(v, (int, float)):
            values.append(float(v))
    return values

def build_metric_baseline(scope: PerformanceBaselineScope, metric_name: PerformanceMetricName, values: List[float]) -> PerformanceMetricBaseline:
    sample_count = len(values)
    status = BaselineStatus.ACTIVE if sample_count >= 3 else BaselineStatus.INSUFFICIENT_DATA

    if not values:
        return PerformanceMetricBaseline(
            metric_id=create_performance_metric_baseline_id(metric_name, scope),
            name=metric_name,
            scope=scope,
            sample_count=0,
            mean_value=None, median_value=None, p75_value=None, p90_value=None, min_value=None, max_value=None,
            unit=None, status=BaselineStatus.INSUFFICIENT_DATA
        )

    return PerformanceMetricBaseline(
        metric_id=create_performance_metric_baseline_id(metric_name, scope),
        name=metric_name,
        scope=scope,
        sample_count=sample_count,
        mean_value=float(statistics.mean(values)),
        median_value=float(statistics.median(values)),
        p75_value=calculate_percentile(values, 75.0),
        p90_value=calculate_percentile(values, 90.0),
        min_value=float(min(values)),
        max_value=float(max(values)),
        unit=None,
        status=status
    )

def build_performance_baseline(scope: PerformanceBaselineScope, samples: List[CurrentPerformanceSample], version: Optional[str] = None) -> PerformanceBaseline:
    ver = version or create_baseline_version()
    scope_samples = [s for s in samples if s.scope == scope]

    metrics = []
    for metric_name in supported_metric_names_for_scope(scope):
        vals = metric_values_from_samples(scope_samples, metric_name)
        if vals:
            metrics.append(build_metric_baseline(scope, metric_name, vals))

    overall_status = BaselineStatus.ACTIVE if len(scope_samples) >= 3 else BaselineStatus.INSUFFICIENT_DATA

    return PerformanceBaseline(
        baseline_id=create_performance_baseline_id(scope),
        version=ver,
        scope=scope,
        status=overall_status,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_count=len(scope_samples),
        metrics=metrics,
        source_paths=[s.source_path for s in scope_samples if s.source_path],
        warnings=[], errors=[], metadata={}
    )

def build_all_performance_baselines(samples: List[CurrentPerformanceSample], version: Optional[str] = None) -> List[PerformanceBaseline]:
    scopes = set(s.scope for s in samples)
    ver = version or create_baseline_version()
    baselines = []
    for scope in scopes:
        baselines.append(build_performance_baseline(scope, samples, version=ver))
    return baselines

def baseline_builder_summary_to_text(baselines: List[PerformanceBaseline]) -> str:
    lines = ["Performance Baseline Builder Summary:"]
    lines.append(f"Total Baselines Built: {len(baselines)}")
    for b in baselines:
        lines.append(f" - Scope: {b.scope.value}, Version: {b.version}, Status: {b.status.value}, Sources: {b.source_count}, Metrics: {len(b.metrics)}")
    return "\n".join(lines)
