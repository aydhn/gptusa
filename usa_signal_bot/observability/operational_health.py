import datetime
from pathlib import Path
from typing import List, Optional

from usa_signal_bot.core.enums import OperationalHealthStatus, OperationalMetricStatus, SafetyMonitorStatus, DiskUsageStatus
from usa_signal_bot.observability.observability_models import (
    OperationalHealthReport, OperationalMetricsSnapshot, create_operational_health_report_id
)
from usa_signal_bot.observability.metrics_collector import OperationalMetricsCollector
from usa_signal_bot.observability.disk_usage import collect_disk_usage_summary, DiskUsageSummary
from usa_signal_bot.observability.safety_monitor import build_safety_monitor_report, SafetyMonitorReport
from usa_signal_bot.observability.error_trends import build_error_trend_summary, ErrorTrendSummary
from usa_signal_bot.observability.local_logger import read_observability_events_jsonl

class OperationalHealthEvaluator:
    def __init__(self, data_root: Path, project_root: Optional[Path] = None):
        self.data_root = data_root
        self.project_root = project_root

    def build_report(self) -> OperationalHealthReport:
        mc = OperationalMetricsCollector(self.data_root, self.project_root)
        snap = mc.collect_all()

        disk = collect_disk_usage_summary(self.data_root)
        safety = build_safety_monitor_report()

        events_path = self.data_root / "observability" / "logs" / "events.jsonl"
        events = read_observability_events_jsonl(events_path, limit=5000)
        err_trend = build_error_trend_summary(events)

        st = self.decide_status(snap, safety, disk, err_trend)
        req = self.build_required_actions(snap, safety, disk)
        opt = self.build_optional_actions(snap, disk)

        return OperationalHealthReport(
            report_id=create_operational_health_report_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status=st,
            metrics_snapshot=snap,
            safety_status=safety.status,
            disk_status=disk.status,
            warning_count=err_trend.warning_count,
            error_count=err_trend.error_count,
            critical_count=err_trend.critical_count,
            required_actions=req,
            optional_actions=opt,
            output_paths={},
            warnings=[],
            errors=[]
        )

    def decide_status(self, snap: OperationalMetricsSnapshot, safety: SafetyMonitorReport,
                      disk: DiskUsageSummary, error_summary: Optional[ErrorTrendSummary] = None) -> OperationalHealthStatus:
        if safety.status == SafetyMonitorStatus.BLOCKED:
            return OperationalHealthStatus.FAILED

        if disk.status == DiskUsageStatus.CRITICAL:
            return OperationalHealthStatus.CRITICAL

        if error_summary and error_summary.status == OperationalMetricStatus.CRITICAL:
            return OperationalHealthStatus.CRITICAL

        if snap.status == OperationalMetricStatus.CRITICAL:
            return OperationalHealthStatus.CRITICAL

        if safety.status == SafetyMonitorStatus.WARNING or disk.status == DiskUsageStatus.WARNING or            snap.status == OperationalMetricStatus.WARNING or            (error_summary and error_summary.status == OperationalMetricStatus.WARNING):
            return OperationalHealthStatus.WARNING

        return OperationalHealthStatus.HEALTHY

    def build_required_actions(self, snap: OperationalMetricsSnapshot, safety: SafetyMonitorReport, disk: DiskUsageSummary) -> List[str]:
        req = []
        if safety.status == SafetyMonitorStatus.BLOCKED:
            req.append("Disable broker/live/demo flags in configuration immediately.")
        if disk.status == DiskUsageStatus.CRITICAL:
            req.append("Free up disk space immediately. System may crash.")
        if snap.status == OperationalMetricStatus.CRITICAL:
            req.append("Investigate critical operational metrics.")
        return req

    def build_optional_actions(self, snap: OperationalMetricsSnapshot, disk: DiskUsageSummary) -> List[str]:
        opt = []
        if disk.status == DiskUsageStatus.WARNING:
            opt.append("Consider archiving old runs to free up disk space.")
        if snap.status == OperationalMetricStatus.WARNING:
            opt.append("Review warning metrics and logs.")
        return opt

    def write_report(self, report: OperationalHealthReport) -> List[Path]:
        from usa_signal_bot.observability.observability_store import write_operational_health_report_json
        from usa_signal_bot.observability.observability_reporting import write_observability_report_json

        p = self.data_root / "observability" / "reports" / f"health_{report.report_id}.json"
        write_operational_health_report_json(p, report)
        write_observability_report_json(self.data_root / "observability" / "reports" / "latest_health.json", report)
        report.output_paths["health_report_json"] = str(p)
        return [p, self.data_root / "observability" / "reports" / "latest_health.json"]
