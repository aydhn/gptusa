import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.core.enums import PerformanceBaselineScope, PerformanceMetricName
from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample, create_current_performance_sample_id

def _redact_secrets(data: Any) -> Any:
    """Basic token/secret redaction logic for performance payload"""
    if isinstance(data, dict):
        redacted = {}
        for k, v in data.items():
            if any(sub in k.lower() for sub in ["secret", "token", "api_key", "password"]):
                redacted[k] = "***REDACTED***"
            else:
                redacted[k] = _redact_secrets(v)
        return redacted
    elif isinstance(data, list):
        return [_redact_secrets(i) for i in data]
    return data


def normalize_profile_to_sample(profile_payload: Dict[str, Any]) -> CurrentPerformanceSample:
    scope_str = profile_payload.get("scope", PerformanceBaselineScope.PROFILING.value)
    try:
        scope = PerformanceBaselineScope(scope_str)
    except ValueError:
        scope = PerformanceBaselineScope.CUSTOM

    metrics = {}
    pm_metrics = profile_payload.get("metrics", {})
    if isinstance(pm_metrics, dict):
        if "wall_time_seconds" in pm_metrics: metrics[PerformanceMetricName.WALL_TIME_SECONDS.value] = pm_metrics["wall_time_seconds"]
        if "process_time_seconds" in pm_metrics: metrics[PerformanceMetricName.PROCESS_TIME_SECONDS.value] = pm_metrics["process_time_seconds"]
        if "memory_peak_bytes" in pm_metrics: metrics[PerformanceMetricName.MEMORY_PEAK_MB.value] = pm_metrics["memory_peak_bytes"] / (1024*1024)
        if "artifact_size_bytes" in pm_metrics: metrics[PerformanceMetricName.OUTPUT_SIZE_MB.value] = pm_metrics["artifact_size_bytes"] / (1024*1024)
        if "output_growth_bytes" in pm_metrics: metrics[PerformanceMetricName.OUTPUT_GROWTH_MB.value] = pm_metrics["output_growth_bytes"] / (1024*1024)

    return CurrentPerformanceSample(
        sample_id=create_current_performance_sample_id(scope),
        scope=scope,
        created_at_utc=profile_payload.get("created_at_utc", datetime.now(timezone.utc).isoformat()),
        metrics=metrics,
        source_path=None,
        warnings=profile_payload.get("warnings", []),
        errors=profile_payload.get("errors", []),
        metadata=_redact_secrets(profile_payload.get("metadata", {}))
    )

def normalize_regression_result_to_sample(result_payload: Dict[str, Any]) -> CurrentPerformanceSample:
    metrics = {}
    if "duration_seconds" in result_payload:
        metrics[PerformanceMetricName.WALL_TIME_SECONDS.value] = result_payload["duration_seconds"]

    if "error_count" in result_payload:
        metrics[PerformanceMetricName.ERROR_COUNT.value] = result_payload["error_count"]

    return CurrentPerformanceSample(
        sample_id=create_current_performance_sample_id(PerformanceBaselineScope.REGRESSION),
        scope=PerformanceBaselineScope.REGRESSION,
        created_at_utc=result_payload.get("created_at_utc", datetime.now(timezone.utc).isoformat()),
        metrics=metrics,
        source_path=None,
        warnings=result_payload.get("warnings", []),
        errors=result_payload.get("errors", []),
        metadata=_redact_secrets(result_payload)
    )

def normalize_scheduler_result_to_sample(result_payload: Dict[str, Any]) -> CurrentPerformanceSample:
    metrics = {}
    return CurrentPerformanceSample(
        sample_id=create_current_performance_sample_id(PerformanceBaselineScope.SCHEDULER),
        scope=PerformanceBaselineScope.SCHEDULER,
        created_at_utc=result_payload.get("created_at_utc", datetime.now(timezone.utc).isoformat()),
        metrics=metrics,
        source_path=None,
        warnings=result_payload.get("warnings", []),
        errors=result_payload.get("errors", []),
        metadata=_redact_secrets(result_payload)
    )

def normalize_taskqueue_result_to_sample(result_payload: Dict[str, Any]) -> CurrentPerformanceSample:
    metrics = {}
    return CurrentPerformanceSample(
        sample_id=create_current_performance_sample_id(PerformanceBaselineScope.TASKQUEUE),
        scope=PerformanceBaselineScope.TASKQUEUE,
        created_at_utc=result_payload.get("created_at_utc", datetime.now(timezone.utc).isoformat()),
        metrics=metrics,
        source_path=None,
        warnings=result_payload.get("warnings", []),
        errors=result_payload.get("errors", []),
        metadata=_redact_secrets(result_payload)
    )

def normalize_quality_result_to_sample(result_payload: Dict[str, Any]) -> CurrentPerformanceSample:
    metrics = {}
    return CurrentPerformanceSample(
        sample_id=create_current_performance_sample_id(PerformanceBaselineScope.QUALITY),
        scope=PerformanceBaselineScope.QUALITY,
        created_at_utc=result_payload.get("created_at_utc", datetime.now(timezone.utc).isoformat()),
        metrics=metrics,
        source_path=None,
        warnings=result_payload.get("warnings", []),
        errors=result_payload.get("errors", []),
        metadata=_redact_secrets(result_payload)
    )


def collect_samples_from_profiling_store(data_root: Path, scope: Optional[PerformanceBaselineScope] = None, limit: Optional[int] = None) -> List[CurrentPerformanceSample]:
    store_dir = data_root / "profiling" / "runs"
    if not store_dir.exists():
        return []

    samples = []
    # simplistic listing
    for f in sorted(store_dir.rglob("*.json"), reverse=True):
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                sample = normalize_profile_to_sample(data)
                sample.source_path = str(f)
                if scope and sample.scope != scope:
                    continue
                samples.append(sample)
                if limit and len(samples) >= limit:
                    break
        except Exception:
            continue
    return samples

def collect_samples_from_regression_store(data_root: Path, limit: Optional[int] = None) -> List[CurrentPerformanceSample]:
    store_dir = data_root / "regression" / "runs"
    if not store_dir.exists():
        return []

    samples = []
    for f in sorted(store_dir.rglob("*.json"), reverse=True):
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                sample = normalize_regression_result_to_sample(data)
                sample.source_path = str(f)
                samples.append(sample)
                if limit and len(samples) >= limit:
                    break
        except Exception:
            continue
    return samples

def collect_samples_from_scheduler_store(data_root: Path, limit: Optional[int] = None) -> List[CurrentPerformanceSample]:
    store_dir = data_root / "scheduler" / "runs"
    if not store_dir.exists():
        return []

    samples = []
    for f in sorted(store_dir.rglob("*.json"), reverse=True):
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                sample = normalize_scheduler_result_to_sample(data)
                sample.source_path = str(f)
                samples.append(sample)
                if limit and len(samples) >= limit:
                    break
        except Exception:
            continue
    return samples

def collect_samples_from_taskqueue_store(data_root: Path, limit: Optional[int] = None) -> List[CurrentPerformanceSample]:
    store_dir = data_root / "taskqueue" / "runs"
    if not store_dir.exists():
        return []

    samples = []
    for f in sorted(store_dir.rglob("*.json"), reverse=True):
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                sample = normalize_taskqueue_result_to_sample(data)
                sample.source_path = str(f)
                samples.append(sample)
                if limit and len(samples) >= limit:
                    break
        except Exception:
            continue
    return samples

def collect_samples_from_quality_store(data_root: Path, limit: Optional[int] = None) -> List[CurrentPerformanceSample]:
    store_dir = data_root / "quality" / "runs"
    if not store_dir.exists():
        return []

    samples = []
    for f in sorted(store_dir.rglob("*.json"), reverse=True):
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                sample = normalize_quality_result_to_sample(data)
                sample.source_path = str(f)
                samples.append(sample)
                if limit and len(samples) >= limit:
                    break
        except Exception:
            continue
    return samples

def collect_current_operational_sample(data_root: Path) -> CurrentPerformanceSample:
    # A generic current stack sample, mostly mocked from the environment locally since we lack a full active runner hook here
    # No psutil or heavy monitoring tool permitted.
    return CurrentPerformanceSample(
        sample_id=create_current_performance_sample_id(PerformanceBaselineScope.FULL_LOCAL_STACK),
        scope=PerformanceBaselineScope.FULL_LOCAL_STACK,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        metrics={},
        source_path=None,
        warnings=[],
        errors=[],
        metadata={"info": "Local simulated operational sample"}
    )
