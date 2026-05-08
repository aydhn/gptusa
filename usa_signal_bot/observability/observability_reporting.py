import json
from pathlib import Path
from typing import Dict, Any, Optional

from usa_signal_bot.observability.observability_models import (
    ObservabilityEvent, OperationalMetric, LogFileSummary, LogRotationResult,
    OperationalMetricsSnapshot, OperationalHealthReport, operational_health_report_to_dict
)
from usa_signal_bot.observability.observability_validation import ObservabilityValidationReport

def observability_event_to_text(event: ObservabilityEvent) -> str:
    return f"[{event.timestamp_utc}] [{event.severity.value}] [{event.event_type.value}] [{event.source}] {event.message}"

def operational_metric_to_text(metric: OperationalMetric) -> str:
    return f"{metric.name}: {metric.value} (Status: {metric.status.value})"

def log_file_summary_to_text(summary: LogFileSummary) -> str:
    return f"{summary.path} - Size: {summary.size_bytes} bytes | Warnings: {summary.warning_count} | Errors: {summary.error_count}"

def log_rotation_result_to_text(result: LogRotationResult) -> str:
    return f"Rotation Result [{result.status.value}]: {result.original_path} -> {result.rotated_path or 'N/A'}"

def operational_metrics_snapshot_to_text(snapshot: OperationalMetricsSnapshot, limit: int = 40) -> str:
    lines = [f"--- Operational Metrics Snapshot ({snapshot.status.value}) ---"]
    for i, m in enumerate(snapshot.metrics):
        if i >= limit:
            lines.append("... more metrics truncated ...")
            break
        lines.append(f"  - {operational_metric_to_text(m)}")
    return "\n".join(lines)

def operational_health_report_to_text(report: OperationalHealthReport, limit: int = 40) -> str:
    lines = [
        f"--- Operational Health Report ({report.status.value}) ---",
        f"Safety: {report.safety_status.value} | Disk: {report.disk_status.value}",
        f"Errors: {report.error_count} | Critical: {report.critical_count}"
    ]
    if report.required_actions:
        lines.append("\nRequired Actions:")
        for a in report.required_actions: lines.append(f"  - [REQUIRED] {a}")
    if report.optional_actions:
        lines.append("\nOptional Actions:")
        for a in report.optional_actions: lines.append(f"  - [OPTIONAL] {a}")

    lines.append("\n" + observability_limitations_text())
    return "\n".join(lines)

def observability_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: Logs: {summary.get('logs', 0)} | Metrics: {summary.get('metrics', 0)} | Reports: {summary.get('reports', 0)} | Rotations: {summary.get('rotations', 0)}"

def observability_limitations_text() -> str:
    return (
        "OBSERVABILITY LIMITATIONS:\n"
        "1. This is a local observability system.\n"
        "2. No external telemetry or remote dashboard is used.\n"
        "3. Metrics snapshot is not real-time monitoring.\n"
        "4. This report is NOT an investment advice and NOT a live execution approval.\n"
    )

def write_observability_report_json(path: Path, report: OperationalHealthReport, validation_report: Optional[ObservabilityValidationReport] = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    d = operational_health_report_to_dict(report)
    if validation_report:
        d["validation_valid"] = validation_report.valid
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)
    return path
