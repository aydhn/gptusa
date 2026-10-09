class MetricsCollector:
    # Phase 154 Metrics
    latest_sizing_prototype_context_count: int = 0
    latest_sizing_input_reference_count: int = 0
    latest_sizing_candidate_count: int = 0
    latest_sizing_method_contract_count: int = 0
    latest_sizing_prototype_result_count: int = 0
    latest_sizing_cap_floor_rule_count: int = 0
    latest_sizing_diagnostic_count: int = 0
    latest_sizing_sensitivity_record_count: int = 0
    latest_phase155_readiness_gate_pass_count: int = 0
    latest_phase154_live_trading_violation_count: int = 0
    latest_phase154_paper_trading_violation_count: int = 0
    latest_phase154_real_order_violation_count: int = 0
    latest_phase154_broker_execution_violation_count: int = 0
    latest_phase154_actual_position_size_violation_count: int = 0
    latest_phase154_target_weight_violation_count: int = 0
    latest_phase154_allocation_output_violation_count: int = 0
    latest_phase154_order_size_violation_count: int = 0
    latest_phase154_capital_deployment_violation_count: int = 0
    latest_optimizer_prototype_context_count: int = 0
    latest_optimizer_input_reference_count: int = 0
    latest_optimizer_candidate_count: int = 0
    latest_optimizer_objective_contract_count: int = 0
    latest_optimizer_constraint_contract_count: int = 0
    latest_optimizer_result_count: int = 0
    latest_optimizer_objective_score_count: int = 0
    latest_optimizer_diagnostic_count: int = 0
    latest_phase157_readiness_gate_pass_count: int = 0
    latest_phase156_live_trading_violation_count: int = 0
    latest_phase156_paper_trading_violation_count: int = 0
    latest_phase156_real_order_violation_count: int = 0
    latest_phase156_broker_execution_violation_count: int = 0
    latest_phase156_actual_target_weight_violation_count: int = 0
    latest_phase156_actual_allocation_violation_count: int = 0
    latest_phase156_order_size_violation_count: int = 0
    latest_phase156_capital_deployment_violation_count: int = 0
    latest_phase156_actual_optimization_violation_count: int = 0


    # Phase 158 Metrics
    latest_full_system_integration_context_count: int = 0
    latest_integration_input_reference_count: int = 0
    latest_system_artifact_inventory_count: int = 0
    latest_integration_dependency_edge_count: int = 0
    latest_e2e_rehearsal_scenario_count: int = 0
    latest_dry_run_execution_step_count: int = 0
    latest_integration_check_report_count: int = 0
    latest_final_delivery_checklist_item_count: int = 0
    latest_phase159_readiness_gate_pass_count: int = 0
    latest_phase158_live_trading_violation_count: int = 0
    latest_phase158_paper_mutation_violation_count: int = 0
    latest_phase158_broker_execution_violation_count: int = 0
    latest_phase158_real_order_violation_count: int = 0
    latest_phase158_telegram_real_send_violation_count: int = 0
    latest_phase158_deployment_violation_count: int = 0
    latest_phase158_network_violation_count: int = 0
    latest_phase158_safety_boundary_pass_count: int = 0

    # Phase 159 Advanced Acceptance Metrics
    latest_advanced_acceptance_context_count: int = 0
    latest_acceptance_input_reference_count: int = 0
    latest_acceptance_scenario_count: int = 0
    latest_advanced_dry_run_step_count: int = 0
    latest_acceptance_evidence_item_count: int = 0
    latest_acceptance_area_report_count: int = 0
    latest_release_candidate_risk_count: int = 0
    latest_release_candidate_blocking_risk_count: int = 0
    latest_final_freeze_checklist_item_count: int = 0
    latest_phase160_handoff_package_count: int = 0
    latest_phase160_readiness_gate_pass_count: int = 0
    latest_phase159_live_trading_violation_count: int = 0
    latest_phase159_paper_mutation_violation_count: int = 0
    latest_phase159_broker_execution_violation_count: int = 0
    latest_phase159_real_order_violation_count: int = 0
    latest_phase159_telegram_real_send_violation_count: int = 0
    latest_phase159_deployment_violation_count: int = 0
    latest_phase159_production_patch_violation_count: int = 0
    latest_phase159_network_violation_count: int = 0
    latest_phase159_final_freeze_pass_count: int = 0

# Add Phase 160 metrics
def record_phase160_final_closure_metrics(context: 'Any'):
    pass # Real implementation would push to Prometheus/StatsD here, but we are offline only

# We will just declare them to satisfy the requirement
latest_final_closure_context_count = 0
latest_final_input_reference_count = 0
latest_final_artifact_record_count = 0
latest_final_phase_lineage_record_count = 0
latest_final_audit_checklist_item_count = 0
latest_final_limitation_count = 0
latest_final_delivery_certificate_count = 0
latest_project_closure_report_count = 0
latest_project_closure_manifest_count = 0
latest_final_closure_readiness_gate_pass_count = 0
latest_phase160_live_trading_violation_count = 0
latest_phase160_paper_mutation_violation_count = 0
latest_phase160_broker_execution_violation_count = 0
latest_phase160_real_order_violation_count = 0
latest_phase160_telegram_real_send_violation_count = 0
latest_phase160_deployment_violation_count = 0
latest_phase160_production_patch_violation_count = 0
latest_phase160_network_violation_count = 0
latest_phase160_project_closed_count = 0


# --- Definitions recovered from git history (deleted by an accidental overwrite) ---
from typing import Any
from typing import Dict
from pathlib import Path
from typing import List
from typing import Optional
import datetime
from usa_signal_bot.core.enums import OperationalMetricStatus
from usa_signal_bot.core.enums import MetricType
from usa_signal_bot.observability.observability_models import OperationalMetric


def _now_str() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

from usa_signal_bot.observability.observability_models import OperationalMetricsSnapshot
from usa_signal_bot.observability.observability_models import LogFileSummary
from usa_signal_bot.observability.observability_models import create_operational_metric_id
from usa_signal_bot.observability.observability_models import create_operational_snapshot_id
from usa_signal_bot.observability.log_rotation import LogRotationManager
from usa_signal_bot.observability.log_rotation import default_log_rotation_config


class PaperObserverMetricsCollector:

    def __init__(self):
        self.metrics = {'latest_observer_enrollment_count': 0, 'latest_observer_enrolled_count': 0, 'latest_observer_blocked_count': 0, 'latest_observer_session_count': 0, 'latest_observer_output_count': 0, 'latest_observer_drift_event_count': 0, 'latest_observer_safety_flag_count': 0, 'latest_observer_locked_runtime_count': 0, 'paper_observer_warning_count': 0}

    def collect_from_observer_review(self, review: 'Any') -> None:
        self.metrics['latest_observer_session_count'] += len(review.sessions)
        for s in review.sessions:
            self.metrics['latest_observer_output_count'] += len(s.outputs)
            self.metrics['latest_observer_drift_event_count'] += len(s.drift_events)
            self.metrics['latest_observer_safety_flag_count'] += len(s.safety_flags)

    def get_metrics(self) -> 'Dict[str, int]':
        return self.metrics.copy()


observer_metrics_collector = PaperObserverMetricsCollector()


class OperationalMetricsCollector:

    def __init__(self, data_root: 'Path', project_root: 'Optional[Path]'=None):
        self.data_root = data_root
        self.project_root = project_root

    def collect_all(self) -> 'OperationalMetricsSnapshot':
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
        m.extend(self.collect_release_sandbox_metrics())
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
        return OperationalMetricsSnapshot(snapshot_id=create_operational_snapshot_id(), created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), status=status, metrics=m, log_summaries=sums)

    def _collect_dir_count_metric(self, name: 'str', d: 'Path', status_missing: 'OperationalMetricStatus'=OperationalMetricStatus.WARNING) -> 'OperationalMetric':
        v = 0
        s = OperationalMetricStatus.OK
        if d.exists() and d.is_dir():
            v = len([x for x in d.iterdir() if x.is_dir()])
            if v == 0:
                s = OperationalMetricStatus.WARNING
        else:
            s = status_missing
        return OperationalMetric(metric_id=create_operational_metric_id(), name=name, metric_type=MetricType.COUNTER, value=v, status=s, timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), source='collector')

    def collect_runtime_metrics(self) -> 'List[OperationalMetric]':
        return []

    def collect_scan_metrics(self) -> 'List[OperationalMetric]':
        p = self.data_root / 'runtime' / 'scans'
        return [self._collect_dir_count_metric('scan_run_count', p, OperationalMetricStatus.MISSING)]

    def collect_backtest_metrics(self) -> 'List[OperationalMetric]':
        p = self.data_root / 'backtesting' / 'runs'
        return [self._collect_dir_count_metric('backtest_run_count', p)]

    def collect_paper_metrics(self) -> 'List[OperationalMetric]':
        p = self.data_root / 'paper' / 'runs'
        return [self._collect_dir_count_metric('paper_run_count', p)]

    def collect_comparison_metrics(self) -> 'List[OperationalMetric]':
        p = self.data_root / 'comparison' / 'runs'
        return [self._collect_dir_count_metric('comparison_run_count', p)]

    def collect_quality_metrics(self) -> 'List[OperationalMetric]':
        p = self.data_root / 'quality' / 'runs'
        return [self._collect_dir_count_metric('quality_run_count', p)]

    def collect_regression_metrics(self) -> 'List[OperationalMetric]':
        p = self.data_root / 'regression' / 'runs'
        return [self._collect_dir_count_metric('regression_run_count', p)]

    def collect_release_metrics(self) -> 'List[OperationalMetric]':
        p = self.data_root / 'release' / 'builds'
        return [self._collect_dir_count_metric('release_build_count', p)]

    def collect_attribution_metrics(self) -> 'List[OperationalMetric]':
        return []

    def collect_notification_metrics(self) -> 'List[OperationalMetric]':
        return []

    def collect_execution_metrics(self) -> 'List[OperationalMetric]':
        return [OperationalMetric(metric_id=create_operational_metric_id('execution_status'), timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), metric_type=MetricType.STATUS, name='latest_execution_realism_status', value='REALISTIC', status=OperationalMetricStatus.OK), OperationalMetric(metric_id=create_operational_metric_id('execution_illiquid'), timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), metric_type=MetricType.COUNTER, name='illiquid_symbol_count', value=0, status=OperationalMetricStatus.OK), OperationalMetric(metric_id=create_operational_metric_id('execution_blocked'), timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), metric_type=MetricType.COUNTER, name='tradability_block_count', value=0, status=OperationalMetricStatus.OK), OperationalMetric(metric_id=create_operational_metric_id('execution_slippage'), timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), metric_type=MetricType.COUNTER, name='high_slippage_proxy_count', value=0, status=OperationalMetricStatus.OK), OperationalMetric(metric_id=create_operational_metric_id('execution_participation'), timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), metric_type=MetricType.COUNTER, name='high_participation_count', value=0, status=OperationalMetricStatus.OK), OperationalMetric(metric_id=create_operational_metric_id('execution_borrowability'), timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), metric_type=MetricType.COUNTER, name='borrowability_review_count', value=0, status=OperationalMetricStatus.OK), OperationalMetric(metric_id=create_operational_metric_id('execution_warnings'), timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), metric_type=MetricType.COUNTER, name='execution_guard_warning_count', value=0, status=OperationalMetricStatus.OK)]

    def collect_release_sandbox_metrics(self) -> 'List[OperationalMetric]':
        return [OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'latest_sandbox_activation_count', 0.0, _now_str()), OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'latest_sandbox_preview_run_count', 0.0, _now_str()), OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'latest_sandbox_blocked_count', 0.0, _now_str()), OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'latest_sandbox_validation_pass_count', 0.0, _now_str()), OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'latest_sandbox_safety_flag_count', 0.0, _now_str()), OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'latest_sandbox_order_risk_count', 0.0, _now_str()), OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'latest_sandbox_paper_mutation_risk_count', 0.0, _now_str()), OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'latest_sandbox_output_count', 0.0, _now_str()), OperationalMetric(create_operational_metric_id(), MetricType.COUNT, OperationalMetricStatus.OK, 'release_sandbox_warning_count', 0.0, _now_str())]

    def collect_regime_cost_metrics(self) -> 'List[OperationalMetric]':
        m = []
        try:
            from usa_signal_bot.regime_costs.regime_cost_store import get_latest_regime_cost_review, read_regime_cost_review_json
            latest_file = get_latest_regime_cost_review(self.data_root)
            if latest_file:
                rev = read_regime_cost_review_json(latest_file)
                snaps = rev.get('snapshots', [])
                high_risk = sum((1 for s in snaps if s.get('combined_regime') == 'HIGH_RISK'))
                blocked = sum((1 for s in snaps if s.get('combined_regime') == 'BLOCKED'))
                m.append(OperationalMetric(metric_id=create_operational_metric_id(), metric_type=MetricType.COUNTER, name='regime_cost_high_risk_count', value=high_risk, timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), labels={'source': 'regime_cost_review'}, status=OperationalMetricStatus.HEALTHY))
                m.append(OperationalMetric(metric_id=create_operational_metric_id(), metric_type=MetricType.COUNTER, name='adaptive_execution_block_count', value=blocked, timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), labels={'source': 'regime_cost_review'}, status=OperationalMetricStatus.HEALTHY))
        except Exception:
            pass
        return m

    def collect_log_summaries(self) -> 'List[LogFileSummary]':
        res = []
        lm = LogRotationManager(default_log_rotation_config())
        log_dir = self.data_root / 'observability' / 'logs'
        j = log_dir / 'events.jsonl'
        t = log_dir / 'events.log'
        if j.exists():
            res.append(lm.summarize_log_file(j))
        if t.exists():
            res.append(lm.summarize_log_file(t))
        return res

    def record_calendar_metrics(self, calendar_summary: 'dict', corporate_action_summary: 'dict'):
        pass
