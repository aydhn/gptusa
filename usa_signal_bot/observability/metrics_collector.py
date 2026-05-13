from pathlib import Path
from typing import List, Optional
import datetime

from usa_signal_bot.core.enums import OperationalMetricStatus, MetricType
from usa_signal_bot.observability.observability_models import (
    OperationalMetric, OperationalMetricsSnapshot, LogFileSummary,
    create_operational_metric_id, create_operational_snapshot_id
)
from usa_signal_bot.observability.log_rotation import LogRotationManager, default_log_rotation_config

class OperationalMetricsCollector:
    def __init__(self, data_root: Path, project_root: Optional[Path] = None):
        self.data_root = data_root
        self.project_root = project_root

    def collect_all(self) -> OperationalMetricsSnapshot:
        m = []
        m.extend(self.collect_runtime_metrics())
        m.extend(self.collect_scan_metrics())
        m.extend(self.collect_backtest_metrics())
        m.extend(self.collect_paper_metrics())
        m.extend(self.collect_comparison_metrics())
        m.extend(self.collect_quality_metrics())
        m.extend(self.collect_regression_metrics())
        m.extend(self.collect_release_metrics())
        m.extend(self.collect_notification_metrics())

        sums = self.collect_log_summaries()

        status = OperationalMetricStatus.OK
        for x in m:
            if x.status in [OperationalMetricStatus.CRITICAL, OperationalMetricStatus.CRITICAL]:
                status = OperationalMetricStatus.CRITICAL
                break
            elif x.status == OperationalMetricStatus.WARNING:
                if status != OperationalMetricStatus.CRITICAL:
                    status = OperationalMetricStatus.WARNING

        return OperationalMetricsSnapshot(
            snapshot_id=create_operational_snapshot_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            status=status,
            metrics=m,
            log_summaries=sums
        )

    def _collect_dir_count_metric(self, name: str, d: Path, status_missing: OperationalMetricStatus = OperationalMetricStatus.WARNING) -> OperationalMetric:
        v = 0
        s = OperationalMetricStatus.OK
        if d.exists() and d.is_dir():
            v = len([x for x in d.iterdir() if x.is_dir()])
            if v == 0:
                s = OperationalMetricStatus.WARNING
        else:
            s = status_missing

        return OperationalMetric(
            metric_id=create_operational_metric_id(),
            name=name,
            metric_type=MetricType.COUNTER,
            value=v,
            status=s,
            timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            source="collector"
        )

    def collect_runtime_metrics(self) -> List[OperationalMetric]:
        return []

    def collect_scan_metrics(self) -> List[OperationalMetric]:
        p = self.data_root / "runtime" / "scans"
        return [self._collect_dir_count_metric("scan_run_count", p, OperationalMetricStatus.MISSING)]

    def collect_backtest_metrics(self) -> List[OperationalMetric]:
        p = self.data_root / "backtesting" / "runs"
        return [self._collect_dir_count_metric("backtest_run_count", p)]

    def collect_paper_metrics(self) -> List[OperationalMetric]:
        p = self.data_root / "paper" / "runs"
        return [self._collect_dir_count_metric("paper_run_count", p)]

    def collect_comparison_metrics(self) -> List[OperationalMetric]:
        p = self.data_root / "comparison" / "runs"
        return [self._collect_dir_count_metric("comparison_run_count", p)]

    def collect_quality_metrics(self) -> List[OperationalMetric]:
        p = self.data_root / "quality" / "runs"
        return [self._collect_dir_count_metric("quality_run_count", p)]

    def collect_regression_metrics(self) -> List[OperationalMetric]:
        p = self.data_root / "regression" / "runs"
        return [self._collect_dir_count_metric("regression_run_count", p)]

    def collect_release_metrics(self) -> List[OperationalMetric]:
        p = self.data_root / "release" / "builds"
        return [self._collect_dir_count_metric("release_build_count", p)]

    def collect_notification_metrics(self) -> List[OperationalMetric]:
        return []

    def collect_log_summaries(self) -> List[LogFileSummary]:
        res = []
        lm = LogRotationManager(default_log_rotation_config())

        log_dir = self.data_root / "observability" / "logs"
        j = log_dir / "events.jsonl"
        t = log_dir / "events.log"

        if j.exists(): res.append(lm.summarize_log_file(j))
        if t.exists(): res.append(lm.summarize_log_file(t))
        return res

    def record_calendar_metrics(self, calendar_summary: dict, corporate_action_summary: dict):
        pass
