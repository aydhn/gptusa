from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from usa_signal_bot.core.enums import (
    ObservabilityEventType, ObservabilitySeverity, MetricType,
    OperationalMetricStatus, LogRotationStatus, OperationalHealthStatus,
    DiskUsageStatus, SafetyMonitorStatus
)
import uuid
import datetime

@dataclass
class ObservabilityEvent:
    event_id: str
    event_type: ObservabilityEventType
    severity: ObservabilitySeverity
    timestamp_utc: str
    source: str
    message: str
    run_id: Optional[str] = None
    command: Optional[str] = None
    step_name: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OperationalMetric:
    metric_id: str
    name: str
    metric_type: MetricType
    value: Any
    status: OperationalMetricStatus
    timestamp_utc: str
    unit: Optional[str] = None
    source: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LogFileSummary:
    path: str
    exists: bool
    size_bytes: int
    line_count: Optional[int]
    warning_count: Optional[int]
    error_count: Optional[int]
    last_modified_utc: Optional[str]
    checksum: Optional[str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class LogRotationResult:
    result_id: str
    created_at_utc: str
    status: LogRotationStatus
    original_path: str
    rotated_path: Optional[str]
    original_size_bytes: Optional[int]
    rotated_size_bytes: Optional[int]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class OperationalMetricsSnapshot:
    snapshot_id: str
    created_at_utc: str
    status: OperationalMetricStatus
    metrics: List[OperationalMetric]
    log_summaries: List[LogFileSummary]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

@dataclass
class OperationalHealthReport:
    report_id: str
    created_at_utc: str
    status: OperationalHealthStatus
    metrics_snapshot: OperationalMetricsSnapshot
    safety_status: SafetyMonitorStatus
    disk_status: DiskUsageStatus
    warning_count: int
    error_count: int
    critical_count: int
    required_actions: List[str]
    optional_actions: List[str]
    output_paths: Dict[str, str]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def create_observability_event_id(prefix: str = "obs_event") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_operational_metric_id(prefix: str = "metric") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_log_rotation_result_id(prefix: str = "logrot") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_operational_snapshot_id(prefix: str = "opsnap") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_operational_health_report_id(prefix: str = "ophealth") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def observability_event_to_dict(event: ObservabilityEvent) -> dict:
    from dataclasses import asdict
    return asdict(event)

def operational_metric_to_dict(metric: OperationalMetric) -> dict:
    from dataclasses import asdict
    return asdict(metric)

def log_file_summary_to_dict(summary: LogFileSummary) -> dict:
    from dataclasses import asdict
    return asdict(summary)

def log_rotation_result_to_dict(result: LogRotationResult) -> dict:
    from dataclasses import asdict
    return asdict(result)

def operational_metrics_snapshot_to_dict(snapshot: OperationalMetricsSnapshot) -> dict:
    from dataclasses import asdict
    d = asdict(snapshot)
    d["metrics"] = [operational_metric_to_dict(m) for m in snapshot.metrics]
    d["log_summaries"] = [log_file_summary_to_dict(ls) for ls in snapshot.log_summaries]
    return d

def operational_health_report_to_dict(report: OperationalHealthReport) -> dict:
    from dataclasses import asdict
    d = asdict(report)
    d["metrics_snapshot"] = operational_metrics_snapshot_to_dict(report.metrics_snapshot)
    return d

def validate_observability_event(event: ObservabilityEvent) -> None:
    if not event.source:
        raise ValueError("Event source cannot be empty")
    if not event.message:
        raise ValueError("Event message cannot be empty")
    for k in event.payload.keys():
        kl = str(k).lower()
        if any(bad in kl for bad in ["token", "secret", "password", "credential", "api_key"]):
            raise ValueError(f"Payload contains potentially sensitive key: {k}")

def validate_operational_metric(metric: OperationalMetric) -> None:
    if not metric.name:
        raise ValueError("Metric name cannot be empty")

def validate_log_file_summary(summary: LogFileSummary) -> None:
    if ".." in summary.path:
        raise ValueError("Log path must not contain traversal characters")

def validate_operational_health_report(report: OperationalHealthReport) -> None:
    pass
