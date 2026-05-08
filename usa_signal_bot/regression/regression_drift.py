from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.regression.regression_models import (
    SnapshotComparisonStatus,
    RegressionDriftSeverity
)

@dataclass
class RegressionDriftItem:
    name: str
    status: SnapshotComparisonStatus
    severity: RegressionDriftSeverity
    baseline_checksum: Optional[str] = None
    current_checksum: Optional[str] = None
    changed_fields: List[str] = field(default_factory=list)
    message: str = ""

@dataclass
class RegressionDriftReport:
    report_id: str
    created_at_utc: str
    status: SnapshotComparisonStatus
    max_severity: RegressionDriftSeverity
    items: List[RegressionDriftItem] = field(default_factory=list)
    drift_count: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def build_regression_drift_report(snapshot_results: Dict[str, Dict[str, Any]]) -> RegressionDriftReport:
    import uuid
    report = RegressionDriftReport(
        report_id=f"drift_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=SnapshotComparisonStatus.MATCH,
        max_severity=RegressionDriftSeverity.NONE
    )

    max_sev = RegressionDriftSeverity.NONE
    overall_status = SnapshotComparisonStatus.MATCH

    for name, comp in snapshot_results.items():
        st_str = comp.get("status", "INVALID")
        try:
             status = SnapshotComparisonStatus(st_str)
        except ValueError:
             status = SnapshotComparisonStatus.INVALID

        diff_summary = comp.get("diff_summary", {})
        severity = classify_regression_drift_severity(diff_summary) if status == SnapshotComparisonStatus.DRIFT else RegressionDriftSeverity.NONE

        item = RegressionDriftItem(
            name=name,
            status=status,
            severity=severity,
            baseline_checksum=comp.get("baseline_checksum"),
            current_checksum=comp.get("current_checksum"),
            changed_fields=diff_summary.get("details", []),
            message=comp.get("message", "")
        )
        report.items.append(item)

        if status == SnapshotComparisonStatus.DRIFT:
            report.drift_count += 1
            if overall_status == SnapshotComparisonStatus.MATCH:
                overall_status = SnapshotComparisonStatus.DRIFT

            # Update max severity logic (simple ordering)
            sev_order = {
                RegressionDriftSeverity.NONE: 0,
                RegressionDriftSeverity.LOW: 1,
                RegressionDriftSeverity.MODERATE: 2,
                RegressionDriftSeverity.HIGH: 3,
                RegressionDriftSeverity.CRITICAL: 4,
                RegressionDriftSeverity.UNKNOWN: -1
            }
            if sev_order.get(severity, -1) > sev_order.get(max_sev, -1):
                max_sev = severity

        elif status in (SnapshotComparisonStatus.MISSING_BASELINE, SnapshotComparisonStatus.MISSING_CURRENT):
            report.warnings.append(f"Missing snapshot for {name}: {status.value}")

    report.status = overall_status
    report.max_severity = max_sev
    return report

def classify_regression_drift_severity(diff_summary: Dict[str, Any]) -> RegressionDriftSeverity:
    details = diff_summary.get("details", [])
    if not details:
        return RegressionDriftSeverity.NONE

    critical_keywords = ["status", "count", "approved", "rejected", "decision"]

    for d in details:
        lower_d = d.lower()
        for kw in critical_keywords:
            if kw in lower_d:
                return RegressionDriftSeverity.HIGH

    return RegressionDriftSeverity.LOW

def regression_drift_item_to_dict(item: RegressionDriftItem) -> dict:
    return {
        "name": item.name,
        "status": item.status.value,
        "severity": item.severity.value,
        "baseline_checksum": item.baseline_checksum,
        "current_checksum": item.current_checksum,
        "changed_fields": item.changed_fields,
        "message": item.message
    }

def regression_drift_report_to_dict(report: RegressionDriftReport) -> dict:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "status": report.status.value,
        "max_severity": report.max_severity.value,
        "items": [regression_drift_item_to_dict(i) for i in report.items],
        "drift_count": report.drift_count,
        "warnings": report.warnings,
        "errors": report.errors
    }

def regression_drift_report_to_text(report: RegressionDriftReport) -> str:
    lines = [
        "=== Regression Drift Report ===",
        f"ID: {report.report_id}",
        f"Status: {report.status.value}",
        f"Max Severity: {report.max_severity.value}",
        f"Total Drifts: {report.drift_count}",
        "-" * 30
    ]
    for item in report.items:
        lines.append(f"{item.name}: {item.status.value} (Severity: {item.severity.value})")
        if item.changed_fields:
            lines.append("  Changed fields: " + ", ".join(item.changed_fields[:3]) + ("..." if len(item.changed_fields) > 3 else ""))
    return "\n".join(lines)
