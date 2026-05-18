from typing import Any
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
        m.extend(self.collect_execution_metrics())
        m.extend(self.collect_regime_cost_metrics())
        m.extend(self.collect_attribution_metrics())

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


    def collect_execution_metrics(self) -> List[OperationalMetric]:
        return [
            OperationalMetric(
                metric_id=create_operational_metric_id("execution_status"),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                metric_type=MetricType.STATUS,
                name="latest_execution_realism_status",
                value="REALISTIC",
                status=OperationalMetricStatus.OK
            ),
            OperationalMetric(
                metric_id=create_operational_metric_id("execution_illiquid"),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                metric_type=MetricType.COUNTER,
                name="illiquid_symbol_count",
                value=0,
                status=OperationalMetricStatus.OK
            ),
            OperationalMetric(
                metric_id=create_operational_metric_id("execution_blocked"),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                metric_type=MetricType.COUNTER,
                name="tradability_block_count",
                value=0,
                status=OperationalMetricStatus.OK
            ),
            OperationalMetric(
                metric_id=create_operational_metric_id("execution_slippage"),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                metric_type=MetricType.COUNTER,
                name="high_slippage_proxy_count",
                value=0,
                status=OperationalMetricStatus.OK
            ),
            OperationalMetric(
                metric_id=create_operational_metric_id("execution_participation"),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                metric_type=MetricType.COUNTER,
                name="high_participation_count",
                value=0,
                status=OperationalMetricStatus.OK
            ),
            OperationalMetric(
                metric_id=create_operational_metric_id("execution_borrowability"),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                metric_type=MetricType.COUNTER,
                name="borrowability_review_count",
                value=0,
                status=OperationalMetricStatus.OK
            ),
            OperationalMetric(
                metric_id=create_operational_metric_id("execution_warnings"),
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                metric_type=MetricType.COUNTER,
                name="execution_guard_warning_count",
                value=0,
                status=OperationalMetricStatus.OK
            )
        ]

    def collect_regime_cost_metrics(self) -> List[OperationalMetric]:
        m = []
        try:
            from usa_signal_bot.regime_costs.regime_cost_store import get_latest_regime_cost_review, read_regime_cost_review_json

            latest_file = get_latest_regime_cost_review(self.data_root)
            if latest_file:
                rev = read_regime_cost_review_json(latest_file)
                snaps = rev.get("snapshots", [])

                high_risk = sum(1 for s in snaps if s.get("combined_regime") == "HIGH_RISK")
                blocked = sum(1 for s in snaps if s.get("combined_regime") == "BLOCKED")

                m.append(OperationalMetric(
                    metric_id=create_operational_metric_id(),
                    metric_type=MetricType.COUNTER,
                    name="regime_cost_high_risk_count",
                    value=high_risk,
                    timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    labels={"source": "regime_cost_review"},
                    status=OperationalMetricStatus.HEALTHY
                ))
                m.append(OperationalMetric(
                    metric_id=create_operational_metric_id(),
                    metric_type=MetricType.COUNTER,
                    name="adaptive_execution_block_count",
                    value=blocked,
                    timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    labels={"source": "regime_cost_review"},
                    status=OperationalMetricStatus.HEALTHY
                ))
        except Exception:
            pass
        return m

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


# Operational metrics addition
def update_cost_robustness_metrics(status: str, score: float, failed_scenarios: int, fragile_windows: int, breakeven_bps: float, failed_cells: int, fragility_reasons: int):
    pass

def collect_portfolio_metrics(plan) -> dict:
    m = {}
    if plan.exposure_snapshot:
        m["latest_portfolio_gross_exposure_usd"] = plan.exposure_snapshot.gross_exposure_usd
        m["latest_portfolio_net_exposure_usd"] = plan.exposure_snapshot.net_exposure_usd
        m["latest_portfolio_long_exposure_usd"] = plan.exposure_snapshot.long_exposure_usd
        m["latest_portfolio_short_exposure_usd"] = plan.exposure_snapshot.short_exposure_usd
    m["latest_portfolio_blocked_allocation_count"] = plan.blocked_count + plan.suppressed_count
    m["portfolio_construction_warning_count"] = len(plan.warnings)
    return m

    def collect_attribution_metrics(self) -> List[OperationalMetric]:
        return [
            OperationalMetric(
                metric_id=create_operational_metric_id(),
                type=MetricType.ATTRIBUTION,
                name="latest_total_net_pnl_attributed_usd",
                value=0.0,
                status=OperationalMetricStatus.OK
            )
        ]

# --- Phase 64 Diagnostics Integrations ---
def expose_diagnostics_metrics(review: 'DiagnosticReview') -> None:
    pass

def collect_research_workflow_metrics(payload: dict) -> dict:
    return {
        "latest_repair_queue_count": payload.get("repair_item_count", 0),
        "latest_high_priority_repair_count": 0,
        "latest_hypothesis_count": payload.get("hypothesis_count", 0),
        "latest_ready_experiment_count": payload.get("experiment_plan_count", 0),
        "latest_blocked_experiment_count": 0,
        "latest_acceptance_gate_warning_count": 0,
        "latest_manual_review_required_count": 0,
        "latest_auto_execution_enabled_count": 0,
        "research_workflow_warning_count": 0
    }

class GovernanceMetrics:
    def __init__(self):
        self.latest_governance_review_count = 0
        self.latest_promotion_review_count = 0
        self.latest_release_candidate_count = 0
        self.latest_governance_blocked_count = 0
        self.latest_governance_request_retest_count = 0
        self.latest_governance_request_more_data_count = 0
        self.latest_local_research_candidate_count = 0
        self.latest_governance_risk_flag_count = 0
        self.latest_manual_review_required_count = 0
        self.governance_warning_count = 0

governance_metrics = GovernanceMetrics()
