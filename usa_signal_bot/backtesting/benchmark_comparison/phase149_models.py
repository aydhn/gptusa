from dataclasses import dataclass, field
from typing import Any, Optional, Dict, List
import uuid
import datetime

from usa_signal_bot.core.enums import (
    BenchmarkComparisonStatus,
    BenchmarkComparisonDecision,
    BenchmarkInputKind,
    BenchmarkKind,
    BenchmarkReturnKind,
    RelativePerformanceMetricKind,
    BenchmarkDiagnosticKind,
    BaselineComparisonStatus,
    RelativePerformanceValidationRuleKind,
    BenchmarkSafetyRuleKind,
    Phase150ReadinessStatus,
    Phase150ReadinessRuleKind,
    BenchmarkComparisonQuality,
    BenchmarkComparisonRiskFlag,
    BenchmarkComparisonReportType
)


@dataclass
class BacktestAnalyticsIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    backtest_run_ingested: bool
    inputs_resolved: bool
    return_series_built: bool
    rolling_analytics_built: bool
    advanced_performance_metrics_built: bool
    trade_diagnostics_built: bool
    fill_diagnostics_built: bool
    cost_diagnostics_built: bool
    exposure_diagnostics_built: bool
    drawdown_diagnostics_built: bool
    ledger_reconciliation_built: bool
    determinism_validation_built: bool
    run_validation_report_built: bool
    analytics_report_built: bool
    safety_boundary_validated: bool
    phase149_readiness_gate_built: bool
    phase149_readiness_gate_passed: bool
    ready_for_phase149: bool
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
    deployment_allowed: bool
    network_used: bool
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
    valid_for_phase149: bool
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkInputReference:
    input_ref_id: str
    created_at_utc: str
    input_kind: BenchmarkInputKind
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
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkUniverseContract:
    contract_id: str
    created_at_utc: str
    benchmark_universe_name: str
    strategy_symbols: List[str] = field(default_factory=list)
    benchmark_symbols: List[str] = field(default_factory=list)
    reference_index_label: Optional[str] = None
    cash_benchmark_enabled: bool = False
    buy_and_hold_enabled: bool = False
    equal_weight_metadata_enabled: bool = False
    market_index_reference_enabled: bool = False
    external_fetch_allowed: bool = False
    survivorship_bias_notice: str = ""
    benchmark_data_source_notice: str = ""
    contract_valid: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PassiveBenchmarkConfig:
    config_id: str
    created_at_utc: str
    benchmark_kinds: List[BenchmarkKind] = field(default_factory=list)
    initial_cash: float = 0.0
    currency: str = "USD"
    cash_rate_assumption: float = 0.0
    rebalance_enabled: bool = False
    rebalance_frequency: Optional[str] = None
    equal_weight_metadata_only: bool = True
    market_reference_label: Optional[str] = None
    external_benchmark_fetch_enabled: bool = False
    config_valid: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkCurvePoint:
    point_id: str
    created_at_utc: str
    benchmark_id: str
    benchmark_kind: BenchmarkKind
    timestamp: str
    simulated_benchmark_equity: float
    benchmark_simple_return: Optional[float] = None
    benchmark_cumulative_return: Optional[float] = None
    benchmark_valid: bool = False
    simulated_only: bool = True
    not_portfolio_allocation: bool = True
    not_investment_advice: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkReturnSeries:
    series_id: str
    created_at_utc: str
    benchmark_id: str
    benchmark_kind: BenchmarkKind
    points: List[BenchmarkCurvePoint] = field(default_factory=list)
    row_count: int = 0
    start_timestamp: Optional[str] = None
    end_timestamp: Optional[str] = None
    series_hash: Optional[str] = None
    series_valid: bool = False
    simulated_only: bool = True
    external_fetch_used: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategyBenchmarkAlignedPoint:
    point_id: str
    created_at_utc: str
    run_id: str
    benchmark_id: str
    benchmark_kind: BenchmarkKind
    timestamp: str
    strategy_equity: float
    benchmark_equity: float
    strategy_return: Optional[float] = None
    strategy_cumulative_return: Optional[float] = None
    benchmark_return: Optional[float] = None
    benchmark_cumulative_return: Optional[float] = None
    excess_return: Optional[float] = None
    tracking_difference: Optional[float] = None
    aligned: bool = False
    research_data_only: bool = True
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategyBenchmarkAlignment:
    alignment_id: str
    created_at_utc: str
    run_id: str
    benchmark_id: str
    benchmark_kind: BenchmarkKind
    aligned_points: List[StrategyBenchmarkAlignedPoint] = field(default_factory=list)
    row_count: int = 0
    coverage_ratio: float = 0.0
    missing_strategy_rows: int = 0
    missing_benchmark_rows: int = 0
    alignment_hash: Optional[str] = None
    alignment_valid: bool = False
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RelativePerformanceMetricResult:
    metric_id: str
    created_at_utc: str
    run_id: str
    benchmark_id: str
    benchmark_kind: BenchmarkKind
    metric_kind: RelativePerformanceMetricKind
    metric_name: str
    value: Any = None
    sample_count: int = 0
    higher_is_better: Optional[bool] = None
    non_trading_metric: bool = True
    not_investment_advice: bool = True
    not_strategy_activation: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkDiagnosticRecord:
    diagnostic_id: str
    created_at_utc: str
    benchmark_id: str
    benchmark_kind: BenchmarkKind
    diagnostic_kind: BenchmarkDiagnosticKind
    value: Any = None
    diagnostic_notes: List[str] = field(default_factory=list)
    diagnostic_valid: bool = False
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BaselineComparisonReport:
    report_id: str
    created_at_utc: str
    run_id: str
    benchmark_series: List[BenchmarkReturnSeries] = field(default_factory=list)
    alignments: List[StrategyBenchmarkAlignment] = field(default_factory=list)
    relative_metrics: List[RelativePerformanceMetricResult] = field(default_factory=list)
    diagnostics: List[BenchmarkDiagnosticRecord] = field(default_factory=list)
    report_hash: Optional[str] = None
    report_valid: bool = False
    quality: BenchmarkComparisonQuality = BenchmarkComparisonQuality.UNKNOWN
    benchmark_comparison_executed: bool = True
    walk_forward_executed: bool = False
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    portfolio_optimization_enabled: bool = False
    strategy_activation_allowed: bool = False
    investment_advice: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RelativePerformanceValidationRule:
    rule_id: str
    created_at_utc: str
    rule_kind: RelativePerformanceValidationRuleKind
    name: str
    status: BaselineComparisonStatus = BaselineComparisonStatus.UNKNOWN
    required: bool = True
    passed: bool = False
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RelativePerformanceValidationReport:
    validation_id: str
    created_at_utc: str
    rules: List[RelativePerformanceValidationRule] = field(default_factory=list)
    baseline_report: Optional[BaselineComparisonReport] = None
    validation_status: BaselineComparisonStatus = BaselineComparisonStatus.UNKNOWN
    validation_passed: bool = False
    benchmark_inputs_valid: bool = False
    relative_metrics_valid: bool = False
    no_live_trading: bool = True
    no_paper_trading: bool = True
    no_broker_execution: bool = True
    no_order_output: bool = True
    no_portfolio_optimization: bool = True
    no_deployment: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkSafetyBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: BenchmarkSafetyRuleKind
    name: str
    required: bool = True
    passed: bool = False
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkSafetyBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: List[BenchmarkSafetyBoundaryRule] = field(default_factory=list)
    boundary_passed: bool = False
    offline_benchmark_comparison_only: bool = True
    read_only_analytics_artifacts: bool = True
    local_benchmark_inputs_only: bool = True
    no_external_benchmark_fetch: bool = True
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
    no_walk_forward_phase149: bool = True
    no_stress_test_phase149: bool = True
    no_monte_carlo_phase149: bool = True
    research_data_only: bool = True
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Phase150ReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: Phase150ReadinessRuleKind
    name: str
    status: Phase150ReadinessStatus = Phase150ReadinessStatus.UNKNOWN
    required: bool = True
    passed: bool = False
    expected_value: Any = None
    observed_value: Any = None
    rationale: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Phase150ReadinessGate:
    gate_id: str
    created_at_utc: str
    status: Phase150ReadinessStatus = Phase150ReadinessStatus.UNKNOWN
    rules: List[Phase150ReadinessRule] = field(default_factory=list)
    baseline_report: Optional[BaselineComparisonReport] = None
    relative_validation: Optional[RelativePerformanceValidationReport] = None
    safety_boundary: Optional[BenchmarkSafetyBoundaryResult] = None
    ready_for_phase150: bool = False
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    benchmark_comparison_executed: bool = True
    walk_forward_executed: bool = False
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkComparisonContext:
    context_id: str
    created_at_utc: str
    status: BenchmarkComparisonStatus = BenchmarkComparisonStatus.UNKNOWN
    decision: BenchmarkComparisonDecision = BenchmarkComparisonDecision.UNKNOWN
    source_backtest_analytics_review_id: Optional[str] = None
    ingestion: Optional[BacktestAnalyticsIngestionResult] = None
    input_references: List[BenchmarkInputReference] = field(default_factory=list)
    universe_contract: Optional[BenchmarkUniverseContract] = None
    benchmark_config: Optional[PassiveBenchmarkConfig] = None
    baseline_report: Optional[BaselineComparisonReport] = None
    relative_validation: Optional[RelativePerformanceValidationReport] = None
    safety_boundary: Optional[BenchmarkSafetyBoundaryResult] = None
    phase150_readiness_gate: Optional[Phase150ReadinessGate] = None
    backtest_analytics_ingested: bool = False
    artifacts_loaded: bool = False
    inputs_resolved: bool = False
    benchmark_universe_contract_built: bool = False
    passive_benchmark_config_built: bool = False
    cash_benchmark_built: bool = False
    buy_and_hold_benchmark_built: bool = False
    equal_weight_metadata_benchmark_built: bool = False
    market_index_reference_benchmark_built: bool = False
    benchmark_return_series_built: bool = False
    strategy_benchmark_alignment_built: bool = False
    relative_performance_metrics_built: bool = False
    benchmark_diagnostics_built: bool = False
    baseline_comparison_report_built: bool = False
    relative_performance_validation_built: bool = False
    safety_boundary_validated: bool = False
    phase150_readiness_gate_built: bool = False
    phase150_readiness_gate_passed: bool = False
    ready_for_phase150: bool = False
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
    external_benchmark_fetch_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    dashboard_started: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    benchmark_comparison_executed: bool = True
    walk_forward_executed: bool = False
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    produces_live_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    risk_flags: List[BenchmarkComparisonRiskFlag] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkComparisonFullReview:
    review_id: str
    created_at_utc: str
    report_type: BenchmarkComparisonReportType = BenchmarkComparisonReportType.FULL_PHASE149_REVIEW
    ingestion: Optional[BacktestAnalyticsIngestionResult] = None
    context: Optional[BenchmarkComparisonContext] = None
    baseline_report: Optional[BaselineComparisonReport] = None
    relative_validation: Optional[RelativePerformanceValidationReport] = None
    safety_boundary: Optional[BenchmarkSafetyBoundaryResult] = None
    phase150_readiness_gate: Optional[Phase150ReadinessGate] = None
    output_paths: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def create_backtest_analytics_ingestion_id() -> str:
    return f"btai-{uuid.uuid4().hex[:8]}"

def create_benchmark_input_reference_id() -> str:
    return f"bmin-{uuid.uuid4().hex[:8]}"

def create_benchmark_universe_contract_id() -> str:
    return f"bmuc-{uuid.uuid4().hex[:8]}"

def create_passive_benchmark_config_id() -> str:
    return f"pbmc-{uuid.uuid4().hex[:8]}"

def create_benchmark_curve_point_id() -> str:
    return f"bmcp-{uuid.uuid4().hex[:8]}"

def create_benchmark_return_series_id() -> str:
    return f"bmrs-{uuid.uuid4().hex[:8]}"

def create_strategy_benchmark_aligned_point_id() -> str:
    return f"sbap-{uuid.uuid4().hex[:8]}"

def create_strategy_benchmark_alignment_id() -> str:
    return f"sbal-{uuid.uuid4().hex[:8]}"

def create_relative_performance_metric_id() -> str:
    return f"rpm-{uuid.uuid4().hex[:8]}"

def create_benchmark_diagnostic_id() -> str:
    return f"bmd-{uuid.uuid4().hex[:8]}"

def create_baseline_comparison_report_id() -> str:
    return f"blcr-{uuid.uuid4().hex[:8]}"

def create_relative_performance_validation_rule_id() -> str:
    return f"rpvr-{uuid.uuid4().hex[:8]}"

def create_relative_performance_validation_report_id() -> str:
    return f"rpvp-{uuid.uuid4().hex[:8]}"

def create_benchmark_safety_boundary_rule_id() -> str:
    return f"bsbr-{uuid.uuid4().hex[:8]}"

def create_benchmark_safety_boundary_result_id() -> str:
    return f"bsbres-{uuid.uuid4().hex[:8]}"

def create_phase150_readiness_rule_id() -> str:
    return f"p150rr-{uuid.uuid4().hex[:8]}"

def create_phase150_readiness_gate_id() -> str:
    return f"p150rg-{uuid.uuid4().hex[:8]}"

def create_benchmark_comparison_context_id() -> str:
    return f"bmctx-{uuid.uuid4().hex[:8]}"

def create_benchmark_comparison_full_review_id() -> str:
    return f"bmrev-{uuid.uuid4().hex[:8]}"
