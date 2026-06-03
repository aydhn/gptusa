import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import (
    WalkForwardStatus,
    WalkForwardDecision,
    WalkForwardInputKind,
    WalkForwardWindowKind,
    WalkForwardFoldKind,
    WalkForwardFoldStatus,
    FoldReplayStatus,
    OOSMetricKind,
    TemporalStabilityMetricKind,
    DegradationDiagnosticKind,
    WalkForwardSafetyRuleKind,
    Phase151ReadinessStatus,
    Phase151ReadinessRuleKind,
    WalkForwardQuality,
    WalkForwardRiskFlag,
    WalkForwardReportType
)


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class BenchmarkComparisonIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    backtest_analytics_ingested: bool
    inputs_resolved: bool
    benchmark_universe_contract_built: bool
    passive_benchmark_config_built: bool
    cash_benchmark_built: bool
    buy_and_hold_benchmark_built: bool
    equal_weight_metadata_benchmark_built: bool
    market_index_reference_benchmark_built: bool
    benchmark_return_series_built: bool
    strategy_benchmark_alignment_built: bool
    relative_performance_metrics_built: bool
    benchmark_diagnostics_built: bool
    baseline_comparison_report_built: bool
    relative_performance_validation_built: bool
    safety_boundary_validated: bool
    phase150_readiness_gate_built: bool
    phase150_readiness_gate_passed: bool
    ready_for_phase150: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    deterministic: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    broker_execution_enabled: bool
    real_order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    strategy_activation_allowed: bool
    portfolio_optimization_enabled: bool
    portfolio_allocation_output_enabled: bool
    deployment_allowed: bool
    network_used: bool
    external_benchmark_fetch_used: bool
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    dashboard_started: bool
    daemon_started: bool
    scheduler_enabled: bool
    benchmark_comparison_executed: bool
    walk_forward_executed: bool
    stress_test_executed: bool
    monte_carlo_executed: bool
    produces_live_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    valid_for_phase150: bool
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalkForwardInputReference:
    input_ref_id: str
    created_at_utc: str
    input_kind: WalkForwardInputKind
    source_artifact_name: str
    source_path: Optional[str]
    source_hash: Optional[str]
    available: bool
    read_only: bool
    row_count: Optional[int]
    columns: List[str] = field(default_factory=list)
    forbidden_columns_detected: List[str] = field(default_factory=list)
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalkForwardWindowPolicy:
    policy_id: str
    created_at_utc: str
    policy_name: str
    window_kinds: List[WalkForwardWindowKind] = field(default_factory=list)
    min_train_periods: int = 60
    oos_periods: int = 20
    step_periods: int = 20
    max_folds: int = 10
    anchored_enabled: bool = True
    rolling_enabled: bool = True
    holdout_enabled: bool = False
    uses_future_data: bool = False
    same_window_reuse_allowed: bool = False
    policy_valid: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalkForwardFold:
    fold_id: str
    created_at_utc: str
    fold_kind: WalkForwardFoldKind
    fold_index: int
    train_start: str
    train_end: str
    oos_start: str
    oos_end: str
    train_row_count: int
    oos_row_count: int
    fold_status: WalkForwardFoldStatus
    no_lookahead: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FoldReplayConfig:
    config_id: str
    created_at_utc: str
    fold_id: str
    fold_index: int
    deterministic_seed: int
    initial_cash: float
    cost_model_ref: Optional[str]
    benchmark_ref: Optional[str]
    replay_valid: bool
    offline_replay_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    strategy_activation_allowed: bool = False
    portfolio_optimization_enabled: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FoldReplayResult:
    result_id: str
    created_at_utc: str
    fold_id: str
    fold_index: int
    replay_status: FoldReplayStatus
    run_hash: Optional[str]
    train_metric_values: Dict[str, Any] = field(default_factory=dict)
    oos_metric_values: Dict[str, Any] = field(default_factory=dict)
    simulated_fill_count: int = 0
    simulated_no_fill_count: int = 0
    simulated_total_cost: Optional[float] = None
    deterministic: bool = True
    offline_replay_only: bool = True
    real_order_created: bool = False
    broker_execution_used: bool = False
    paper_state_mutated: bool = False
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FoldPerformanceMetric:
    metric_id: str
    created_at_utc: str
    fold_id: str
    fold_index: int
    metric_kind: OOSMetricKind
    metric_name: str
    in_sample_value: Any
    oos_value: Any
    degradation_value: Any
    sample_count: int
    non_trading_metric: bool = True
    not_investment_advice: bool = True
    not_strategy_activation: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FoldBenchmarkComparison:
    comparison_id: str
    created_at_utc: str
    fold_id: str
    fold_index: int
    benchmark_label: str
    strategy_oos_return: Optional[float]
    benchmark_oos_return: Optional[float]
    excess_oos_return: Optional[float]
    tracking_difference_mean: Optional[float]
    relative_drawdown: Optional[float]
    comparison_valid: bool
    not_strategy_activation: bool = True
    not_investment_advice: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OOSRobustnessMetrics:
    metrics_id: str
    created_at_utc: str
    fold_count: int
    passed_fold_count: int
    failed_fold_count: int
    oos_return_mean: Optional[float]
    oos_return_median: Optional[float]
    oos_return_min: Optional[float]
    oos_return_max: Optional[float]
    oos_return_std: Optional[float]
    oos_max_drawdown_mean: Optional[float]
    oos_excess_return_mean: Optional[float]
    oos_cost_drag_mean: Optional[float]
    fold_pass_rate: Optional[float]
    robustness_score: Optional[float]
    metrics_valid: bool
    non_trading_metric: bool = True
    not_investment_advice: bool = True
    not_strategy_activation: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TemporalStabilityMetric:
    metric_id: str
    created_at_utc: str
    metric_kind: TemporalStabilityMetricKind
    metric_name: str
    value: Any
    stability_label: str
    sample_count: int
    non_trading_metric: bool = True
    not_investment_advice: bool = True
    not_strategy_activation: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DegradationDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    diagnostic_kind: DegradationDiagnosticKind
    value: Any
    severity_label: str
    diagnostic_notes: List[str] = field(default_factory=list)
    diagnostic_valid: bool = False
    not_strategy_activation: bool = True
    not_investment_advice: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RobustnessSummary:
    summary_id: str
    created_at_utc: str
    fold_count: int
    oos_metrics: OOSRobustnessMetrics
    temporal_stability_metrics: List[TemporalStabilityMetric]
    degradation_diagnostics: List[DegradationDiagnostic]
    summary_hash: Optional[str]
    summary_valid: bool
    robustness_quality: WalkForwardQuality
    not_investment_advice: bool = True
    not_strategy_activation: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalkForwardValidationReport:
    report_id: str
    created_at_utc: str
    folds: List[WalkForwardFold]
    fold_replay_results: List[FoldReplayResult]
    fold_metrics: List[FoldPerformanceMetric]
    fold_benchmark_comparisons: List[FoldBenchmarkComparison]
    robustness_summary: RobustnessSummary
    report_hash: Optional[str]
    report_valid: bool
    walk_forward_executed: bool = True
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    portfolio_optimization_enabled: bool = False
    strategy_activation_allowed: bool = False
    investment_advice: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TemporalStabilityAuditReport:
    audit_id: str
    created_at_utc: str
    robustness_summary: RobustnessSummary
    stability_metrics: List[TemporalStabilityMetric]
    degradation_diagnostics: List[DegradationDiagnostic]
    audit_passed: bool
    audit_quality: WalkForwardQuality
    audit_hash: Optional[str]
    no_strategy_activation: bool = True
    no_investment_advice: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalkForwardSafetyBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: WalkForwardSafetyRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalkForwardSafetyBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: List[WalkForwardSafetyBoundaryRule]
    boundary_passed: bool
    offline_walk_forward_only: bool = True
    read_only_benchmark_artifacts: bool = True
    local_inputs_only: bool = True
    no_live_trading: bool = True
    no_paper_trading: bool = True
    no_broker_execution: bool = True
    no_real_order_creation: bool = True
    no_paper_state_mutation: bool = True
    no_telegram_real_send: bool = True
    no_strategy_activation: bool = True
    no_portfolio_optimization: bool = True
    no_portfolio_allocation_output: bool = True
    no_deployment: bool = True
    no_network: bool = True
    no_dashboard: bool = True
    no_daemon: bool = True
    no_scheduler: bool = True
    no_stress_test_phase150: bool = True
    no_monte_carlo_phase150: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Phase151ReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: Phase151ReadinessRuleKind
    name: str
    status: Phase151ReadinessStatus
    required: bool
    passed: bool
    expected_value: Any
    observed_value: Any
    rationale: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Phase151ReadinessGate:
    gate_id: str
    created_at_utc: str
    status: Phase151ReadinessStatus
    rules: List[Phase151ReadinessRule]
    validation_report: WalkForwardValidationReport
    temporal_stability_audit: TemporalStabilityAuditReport
    safety_boundary: WalkForwardSafetyBoundaryResult
    ready_for_phase151: bool
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    walk_forward_executed: bool = True
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalkForwardContext:
    context_id: str
    created_at_utc: str
    status: WalkForwardStatus
    decision: WalkForwardDecision
    source_benchmark_comparison_review_id: Optional[str]
    ingestion: BenchmarkComparisonIngestionResult
    input_references: List[WalkForwardInputReference]
    window_policy: WalkForwardWindowPolicy
    folds: List[WalkForwardFold]
    validation_report: WalkForwardValidationReport
    temporal_stability_audit: TemporalStabilityAuditReport
    safety_boundary: WalkForwardSafetyBoundaryResult
    phase151_readiness_gate: Phase151ReadinessGate
    benchmark_comparison_ingested: bool = False
    artifacts_loaded: bool = False
    inputs_resolved: bool = False
    window_policy_built: bool = False
    anchored_splits_built: bool = False
    rolling_splits_built: bool = False
    fold_replay_configs_built: bool = False
    fold_replays_built: bool = False
    fold_performance_metrics_built: bool = False
    fold_benchmark_comparisons_built: bool = False
    oos_robustness_metrics_built: bool = False
    temporal_stability_built: bool = False
    degradation_diagnostics_built: bool = False
    robustness_summary_built: bool = False
    walk_forward_validation_report_built: bool = False
    temporal_stability_audit_built: bool = False
    safety_boundary_validated: bool = False
    phase151_readiness_gate_built: bool = False
    phase151_readiness_gate_passed: bool = False
    ready_for_phase151: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    deterministic: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    telegram_real_send_enabled: bool = False
    strategy_activation_allowed: bool = False
    portfolio_optimization_enabled: bool = False
    portfolio_allocation_output_enabled: bool = False
    deployment_allowed: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    dashboard_started: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    walk_forward_executed: bool = True
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    produces_live_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[WalkForwardRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WalkForwardFullReview:
    review_id: str
    created_at_utc: str
    report_type: WalkForwardReportType
    ingestion: BenchmarkComparisonIngestionResult
    context: WalkForwardContext
    validation_report: WalkForwardValidationReport
    temporal_stability_audit: TemporalStabilityAuditReport
    safety_boundary: WalkForwardSafetyBoundaryResult
    phase151_readiness_gate: Phase151ReadinessGate
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


# Creation functions

def create_benchmark_comparison_ingestion_id() -> str:
    return f"bm_ingest_{uuid.uuid4().hex[:12]}"

def create_walk_forward_input_reference_id() -> str:
    return f"wfi_{uuid.uuid4().hex[:12]}"

def create_walk_forward_window_policy_id() -> str:
    return f"wfp_{uuid.uuid4().hex[:12]}"

def create_walk_forward_fold_id() -> str:
    return f"wff_{uuid.uuid4().hex[:12]}"

def create_fold_replay_config_id() -> str:
    return f"frc_{uuid.uuid4().hex[:12]}"

def create_fold_replay_result_id() -> str:
    return f"frr_{uuid.uuid4().hex[:12]}"

def create_fold_performance_metric_id() -> str:
    return f"fpm_{uuid.uuid4().hex[:12]}"

def create_fold_benchmark_comparison_id() -> str:
    return f"fbc_{uuid.uuid4().hex[:12]}"

def create_oos_robustness_metrics_id() -> str:
    return f"oos_{uuid.uuid4().hex[:12]}"

def create_temporal_stability_metric_id() -> str:
    return f"tsm_{uuid.uuid4().hex[:12]}"

def create_degradation_diagnostic_id() -> str:
    return f"dd_{uuid.uuid4().hex[:12]}"

def create_robustness_summary_id() -> str:
    return f"rs_{uuid.uuid4().hex[:12]}"

def create_walk_forward_validation_report_id() -> str:
    return f"wfvr_{uuid.uuid4().hex[:12]}"

def create_temporal_stability_audit_id() -> str:
    return f"tsa_{uuid.uuid4().hex[:12]}"

def create_walk_forward_safety_boundary_rule_id() -> str:
    return f"wfsbr_{uuid.uuid4().hex[:12]}"

def create_walk_forward_safety_boundary_result_id() -> str:
    return f"wfsb_{uuid.uuid4().hex[:12]}"

def create_phase151_readiness_rule_id() -> str:
    return f"p151r_{uuid.uuid4().hex[:12]}"

def create_phase151_readiness_gate_id() -> str:
    return f"p151g_{uuid.uuid4().hex[:12]}"

def create_walk_forward_context_id() -> str:
    return f"wfc_{uuid.uuid4().hex[:12]}"

def create_walk_forward_full_review_id() -> str:
    return f"wffr_{uuid.uuid4().hex[:12]}"

# _to_dict functions

def benchmark_comparison_ingestion_result_to_dict(obj: BenchmarkComparisonIngestionResult) -> Dict[str, Any]:
    d = asdict(obj)
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def walk_forward_input_reference_to_dict(obj: WalkForwardInputReference) -> Dict[str, Any]:
    d = asdict(obj)
    d["input_kind"] = obj.input_kind.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def walk_forward_window_policy_to_dict(obj: WalkForwardWindowPolicy) -> Dict[str, Any]:
    d = asdict(obj)
    d["window_kinds"] = [k.value for k in obj.window_kinds]
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def walk_forward_fold_to_dict(obj: WalkForwardFold) -> Dict[str, Any]:
    d = asdict(obj)
    d["fold_kind"] = obj.fold_kind.value
    d["fold_status"] = obj.fold_status.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def fold_replay_config_to_dict(obj: FoldReplayConfig) -> Dict[str, Any]:
    d = asdict(obj)
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def fold_replay_result_to_dict(obj: FoldReplayResult) -> Dict[str, Any]:
    d = asdict(obj)
    d["replay_status"] = obj.replay_status.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def fold_performance_metric_to_dict(obj: FoldPerformanceMetric) -> Dict[str, Any]:
    d = asdict(obj)
    d["metric_kind"] = obj.metric_kind.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def fold_benchmark_comparison_to_dict(obj: FoldBenchmarkComparison) -> Dict[str, Any]:
    d = asdict(obj)
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def oos_robustness_metrics_to_dict(obj: OOSRobustnessMetrics) -> Dict[str, Any]:
    d = asdict(obj)
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def temporal_stability_metric_to_dict(obj: TemporalStabilityMetric) -> Dict[str, Any]:
    d = asdict(obj)
    d["metric_kind"] = obj.metric_kind.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def degradation_diagnostic_to_dict(obj: DegradationDiagnostic) -> Dict[str, Any]:
    d = asdict(obj)
    d["diagnostic_kind"] = obj.diagnostic_kind.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def robustness_summary_to_dict(obj: RobustnessSummary) -> Dict[str, Any]:
    d = asdict(obj)
    d["oos_metrics"] = oos_robustness_metrics_to_dict(obj.oos_metrics)
    d["temporal_stability_metrics"] = [temporal_stability_metric_to_dict(m) for m in obj.temporal_stability_metrics]
    d["degradation_diagnostics"] = [degradation_diagnostic_to_dict(dg) for dg in obj.degradation_diagnostics]
    d["robustness_quality"] = obj.robustness_quality.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def walk_forward_validation_report_to_dict(obj: WalkForwardValidationReport) -> Dict[str, Any]:
    d = asdict(obj)
    d["folds"] = [walk_forward_fold_to_dict(f) for f in obj.folds]
    d["fold_replay_results"] = [fold_replay_result_to_dict(r) for r in obj.fold_replay_results]
    d["fold_metrics"] = [fold_performance_metric_to_dict(m) for m in obj.fold_metrics]
    d["fold_benchmark_comparisons"] = [fold_benchmark_comparison_to_dict(c) for c in obj.fold_benchmark_comparisons]
    d["robustness_summary"] = robustness_summary_to_dict(obj.robustness_summary)
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def temporal_stability_audit_report_to_dict(obj: TemporalStabilityAuditReport) -> Dict[str, Any]:
    d = asdict(obj)
    d["robustness_summary"] = robustness_summary_to_dict(obj.robustness_summary)
    d["stability_metrics"] = [temporal_stability_metric_to_dict(m) for m in obj.stability_metrics]
    d["degradation_diagnostics"] = [degradation_diagnostic_to_dict(dg) for dg in obj.degradation_diagnostics]
    d["audit_quality"] = obj.audit_quality.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def walk_forward_safety_boundary_rule_to_dict(obj: WalkForwardSafetyBoundaryRule) -> Dict[str, Any]:
    d = asdict(obj)
    d["rule_kind"] = obj.rule_kind.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def walk_forward_safety_boundary_result_to_dict(obj: WalkForwardSafetyBoundaryResult) -> Dict[str, Any]:
    d = asdict(obj)
    d["rules"] = [walk_forward_safety_boundary_rule_to_dict(r) for r in obj.rules]
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def phase151_readiness_rule_to_dict(obj: Phase151ReadinessRule) -> Dict[str, Any]:
    d = asdict(obj)
    d["rule_kind"] = obj.rule_kind.value
    d["status"] = obj.status.value
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def phase151_readiness_gate_to_dict(obj: Phase151ReadinessGate) -> Dict[str, Any]:
    d = asdict(obj)
    d["status"] = obj.status.value
    d["rules"] = [phase151_readiness_rule_to_dict(r) for r in obj.rules]
    d["validation_report"] = walk_forward_validation_report_to_dict(obj.validation_report)
    d["temporal_stability_audit"] = temporal_stability_audit_report_to_dict(obj.temporal_stability_audit)
    d["safety_boundary"] = walk_forward_safety_boundary_result_to_dict(obj.safety_boundary)
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def walk_forward_context_to_dict(obj: WalkForwardContext) -> Dict[str, Any]:
    d = asdict(obj)
    d["status"] = obj.status.value
    d["decision"] = obj.decision.value
    d["ingestion"] = benchmark_comparison_ingestion_result_to_dict(obj.ingestion)
    d["input_references"] = [walk_forward_input_reference_to_dict(i) for i in obj.input_references]
    d["window_policy"] = walk_forward_window_policy_to_dict(obj.window_policy)
    d["folds"] = [walk_forward_fold_to_dict(f) for f in obj.folds]
    d["validation_report"] = walk_forward_validation_report_to_dict(obj.validation_report)
    d["temporal_stability_audit"] = temporal_stability_audit_report_to_dict(obj.temporal_stability_audit)
    d["safety_boundary"] = walk_forward_safety_boundary_result_to_dict(obj.safety_boundary)
    d["phase151_readiness_gate"] = phase151_readiness_gate_to_dict(obj.phase151_readiness_gate)
    d["risk_flags"] = [f.value for f in obj.risk_flags]
    return d

def walk_forward_full_review_to_dict(obj: WalkForwardFullReview) -> Dict[str, Any]:
    d = asdict(obj)
    d["report_type"] = obj.report_type.value
    d["ingestion"] = benchmark_comparison_ingestion_result_to_dict(obj.ingestion)
    d["context"] = walk_forward_context_to_dict(obj.context)
    d["validation_report"] = walk_forward_validation_report_to_dict(obj.validation_report)
    d["temporal_stability_audit"] = temporal_stability_audit_report_to_dict(obj.temporal_stability_audit)
    d["safety_boundary"] = walk_forward_safety_boundary_result_to_dict(obj.safety_boundary)
    d["phase151_readiness_gate"] = phase151_readiness_gate_to_dict(obj.phase151_readiness_gate)
    return d
