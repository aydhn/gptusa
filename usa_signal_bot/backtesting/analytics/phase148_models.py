from dataclasses import dataclass, field
from typing import Any
import uuid

from usa_signal_bot.core.enums import (
    BacktestAnalyticsStatus,
    BacktestAnalyticsDecision,
    BacktestAnalyticsInputKind,
    ReturnSeriesKind,
    RollingAnalyticsKind,
    AdvancedPerformanceMetricKind,
    TradeDiagnosticKind,
    FillDiagnosticKind,
    CostDiagnosticKind,
    ExposureDiagnosticKind,
    DrawdownDiagnosticKind,
    RunConsistencyCheckKind,
    BacktestAnalyticsSafetyRuleKind,
    Phase149ReadinessStatus,
    Phase149ReadinessRuleKind,
    BacktestAnalyticsQuality,
    BacktestAnalyticsRiskFlag,
    BacktestAnalyticsReportType
)

@dataclass
class BacktestRunIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    backtest_foundation_ingested: bool
    run_config_built: bool
    research_decision_stream_built: bool
    simulation_clock_built: bool
    price_event_stream_built: bool
    simulated_execution_built: bool
    costs_applied: bool
    liquidity_partial_fill_evaluated: bool
    exposure_timeline_built: bool
    equity_curve_built: bool
    drawdown_curve_built: bool
    ledgers_built: bool
    basic_performance_built: bool
    safety_boundary_validated: bool
    validation_gate_built: bool
    validation_gate_passed: bool
    ready_for_phase148: bool
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
    full_backtest_run_executed: bool
    walk_forward_executed: bool
    stress_test_executed: bool
    monte_carlo_executed: bool
    benchmark_comparison_executed: bool
    produces_live_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    valid_for_phase148: bool
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestAnalyticsInputReference:
    input_ref_id: str
    created_at_utc: str
    input_kind: BacktestAnalyticsInputKind
    source_artifact_name: str
    source_path: str | None
    source_hash: str | None
    available: bool
    read_only: bool
    row_count: int | None
    columns: list[str] = field(default_factory=list)
    forbidden_columns_detected: list[str] = field(default_factory=list)
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ReturnSeriesPoint:
    point_id: str
    created_at_utc: str
    run_id: str
    timestamp: str
    return_kind: ReturnSeriesKind
    simulated_equity: float
    previous_simulated_equity: float | None
    simple_return: float | None
    log_return_approx: float | None
    cumulative_return: float | None
    point_valid: bool
    research_data_only: bool = True
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RollingAnalyticsPoint:
    point_id: str
    created_at_utc: str
    run_id: str
    timestamp: str
    rolling_window: int
    rolling_return: float | None
    rolling_volatility: float | None
    rolling_drawdown: float | None
    rolling_cost_rate: float | None
    rolling_fill_rate: float | None
    rolling_exposure_rate: float | None
    point_valid: bool
    research_data_only: bool = True
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class AdvancedPerformanceMetricResult:
    metric_id: str
    created_at_utc: str
    run_id: str
    metric_kind: AdvancedPerformanceMetricKind
    metric_name: str
    value: float | int | str | None
    sample_count: int
    higher_is_better: bool | None
    non_trading_metric: bool = True
    not_investment_advice: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class TradeDiagnosticRecord:
    diagnostic_id: str
    created_at_utc: str
    run_id: str
    diagnostic_kind: TradeDiagnosticKind
    symbol: str | None
    value: float | int | str | dict[str, Any] | None
    diagnostic_notes: list[str] = field(default_factory=list)
    simulated_only: bool = True
    not_live_trade: bool = True
    not_order_recommendation: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class FillDiagnosticRecord:
    diagnostic_id: str
    created_at_utc: str
    run_id: str
    diagnostic_kind: FillDiagnosticKind
    symbol: str | None
    value: float | int | str | dict[str, Any] | None
    diagnostic_notes: list[str] = field(default_factory=list)
    simulated_only: bool = True
    real_order_created: bool = False
    broker_execution_used: bool = False
    paper_state_mutated: bool = False
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class CostDiagnosticRecord:
    diagnostic_id: str
    created_at_utc: str
    run_id: str
    diagnostic_kind: CostDiagnosticKind
    value: float | int | str | dict[str, Any] | None
    diagnostic_notes: list[str] = field(default_factory=list)
    simulated_only: bool = True
    broker_fee_sync_used: bool = False
    live_quote_used: bool = False
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ExposureDiagnosticResult:
    diagnostic_id: str
    created_at_utc: str
    run_id: str
    diagnostic_kind: ExposureDiagnosticKind
    value: float | int | str | dict[str, Any] | None
    diagnostic_notes: list[str] = field(default_factory=list)
    not_live_position: bool = True
    not_portfolio_allocation: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DrawdownDiagnosticResult:
    diagnostic_id: str
    created_at_utc: str
    run_id: str
    diagnostic_kind: DrawdownDiagnosticKind
    value: float | int | str | dict[str, Any] | None
    diagnostic_notes: list[str] = field(default_factory=list)
    non_trading_metric: bool = True
    not_investment_advice: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RunConsistencyCheck:
    check_id: str
    created_at_utc: str
    run_id: str
    check_kind: RunConsistencyCheckKind
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    diagnostic_notes: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class LedgerReconciliationResult:
    reconciliation_id: str
    created_at_utc: str
    run_id: str
    checks: list[RunConsistencyCheck]
    reconciliation_passed: bool
    equity_reconciled: bool
    cash_reconciled: bool
    cost_reconciled: bool
    fill_count_reconciled: bool
    no_real_orders_detected: bool
    no_paper_mutation_detected: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class DeterminismValidationResult:
    validation_id: str
    created_at_utc: str
    run_id: str
    original_run_hash: str | None
    recomputed_run_hash: str | None
    original_ledger_hash: str | None
    recomputed_ledger_hash: str | None
    deterministic: bool
    validation_passed: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class RunValidationReport:
    report_id: str
    created_at_utc: str
    run_id: str
    ledger_reconciliation: LedgerReconciliationResult
    determinism_validation: DeterminismValidationResult
    consistency_checks: list[RunConsistencyCheck]
    report_hash: str | None
    report_valid: bool
    quality: BacktestAnalyticsQuality
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    real_order_created: bool = False
    broker_execution_used: bool = False
    paper_state_mutated: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestAnalyticsReport:
    report_id: str
    created_at_utc: str
    run_id: str
    return_series: list[ReturnSeriesPoint]
    rolling_analytics: list[RollingAnalyticsPoint]
    performance_metrics: list[AdvancedPerformanceMetricResult]
    trade_diagnostics: list[TradeDiagnosticRecord]
    fill_diagnostics: list[FillDiagnosticRecord]
    cost_diagnostics: list[CostDiagnosticRecord]
    exposure_diagnostics: list[ExposureDiagnosticResult]
    drawdown_diagnostics: list[DrawdownDiagnosticResult]
    run_validation_report: RunValidationReport
    report_hash: str | None
    report_valid: bool
    quality: BacktestAnalyticsQuality
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    benchmark_comparison_executed: bool = False
    walk_forward_executed: bool = False
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    portfolio_optimization_enabled: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestAnalyticsSafetyBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: BacktestAnalyticsSafetyRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestAnalyticsSafetyBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: list[BacktestAnalyticsSafetyBoundaryRule]
    boundary_passed: bool
    offline_analytics_only: bool = True
    read_only_backtest_run_artifacts: bool = True
    no_live_trading: bool = True
    no_paper_trading: bool = True
    no_broker_execution: bool = True
    no_real_order_creation: bool = True
    no_paper_state_mutation: bool = True
    no_telegram_real_send: bool = True
    no_strategy_activation: bool = True
    no_portfolio_optimization: bool = True
    no_deployment: bool = True
    no_network: bool = True
    no_dashboard: bool = True
    no_daemon: bool = True
    no_scheduler: bool = True
    no_walk_forward_phase148: bool = True
    no_stress_test_phase148: bool = True
    no_monte_carlo_phase148: bool = True
    no_benchmark_comparison_phase148: bool = True
    research_data_only: bool = True
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase149ReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: Phase149ReadinessRuleKind
    name: str
    status: Phase149ReadinessStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Phase149ReadinessGate:
    gate_id: str
    created_at_utc: str
    status: Phase149ReadinessStatus
    rules: list[Phase149ReadinessRule]
    analytics_report: BacktestAnalyticsReport
    safety_boundary: BacktestAnalyticsSafetyBoundaryResult
    ready_for_phase149: bool
    research_data_only: bool = True
    offline_backtest_research_only: bool = True
    live_trading_enabled: bool = False
    paper_trading_enabled: bool = False
    broker_execution_enabled: bool = False
    real_order_creation_enabled: bool = False
    paper_state_mutation_enabled: bool = False
    benchmark_comparison_executed: bool = False
    walk_forward_executed: bool = False
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    deployment_allowed: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestAnalyticsContext:
    context_id: str
    created_at_utc: str
    status: BacktestAnalyticsStatus
    decision: BacktestAnalyticsDecision
    source_backtest_run_review_id: str | None
    ingestion: BacktestRunIngestionResult
    input_references: list[BacktestAnalyticsInputReference]
    analytics_report: BacktestAnalyticsReport
    safety_boundary: BacktestAnalyticsSafetyBoundaryResult
    phase149_readiness_gate: Phase149ReadinessGate
    backtest_run_ingested: bool
    artifacts_loaded: bool
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
    deployment_allowed: bool = False
    network_used: bool = False
    paid_api_used: bool = False
    scraping_used: bool = False
    html_parsing_used: bool = False
    dashboard_started: bool = False
    daemon_started: bool = False
    scheduler_enabled: bool = False
    benchmark_comparison_executed: bool = False
    walk_forward_executed: bool = False
    stress_test_executed: bool = False
    monte_carlo_executed: bool = False
    produces_live_signal: bool = False
    produces_order_decision: bool = False
    produces_portfolio_weights: bool = False
    investment_advice: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    risk_flags: list[BacktestAnalyticsRiskFlag] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestAnalyticsFullReview:
    review_id: str
    created_at_utc: str
    report_type: BacktestAnalyticsReportType
    ingestion: BacktestRunIngestionResult
    context: BacktestAnalyticsContext
    analytics_report: BacktestAnalyticsReport
    run_validation_report: RunValidationReport
    safety_boundary: BacktestAnalyticsSafetyBoundaryResult
    phase149_readiness_gate: Phase149ReadinessGate
    output_paths: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def create_backtest_run_ingestion_id() -> str:
    return f"BRI-{uuid.uuid4().hex[:8].upper()}"

def create_backtest_analytics_input_reference_id() -> str:
    return f"BAIR-{uuid.uuid4().hex[:8].upper()}"

def create_return_series_point_id() -> str:
    return f"RSP-{uuid.uuid4().hex[:8].upper()}"

def create_rolling_analytics_point_id() -> str:
    return f"RAP-{uuid.uuid4().hex[:8].upper()}"

def create_advanced_performance_metric_id() -> str:
    return f"APM-{uuid.uuid4().hex[:8].upper()}"

def create_trade_diagnostic_id() -> str:
    return f"TD-{uuid.uuid4().hex[:8].upper()}"

def create_fill_diagnostic_id() -> str:
    return f"FD-{uuid.uuid4().hex[:8].upper()}"

def create_cost_diagnostic_id() -> str:
    return f"CD-{uuid.uuid4().hex[:8].upper()}"

def create_exposure_diagnostic_id() -> str:
    return f"ED-{uuid.uuid4().hex[:8].upper()}"

def create_drawdown_diagnostic_id() -> str:
    return f"DD-{uuid.uuid4().hex[:8].upper()}"

def create_run_consistency_check_id() -> str:
    return f"RCC-{uuid.uuid4().hex[:8].upper()}"

def create_ledger_reconciliation_id() -> str:
    return f"LR-{uuid.uuid4().hex[:8].upper()}"

def create_determinism_validation_id() -> str:
    return f"DV-{uuid.uuid4().hex[:8].upper()}"

def create_run_validation_report_id() -> str:
    return f"RVR-{uuid.uuid4().hex[:8].upper()}"

def create_backtest_analytics_report_id() -> str:
    return f"BAR-{uuid.uuid4().hex[:8].upper()}"

def create_backtest_analytics_safety_boundary_rule_id() -> str:
    return f"BASR-{uuid.uuid4().hex[:8].upper()}"

def create_backtest_analytics_safety_boundary_result_id() -> str:
    return f"BASB-{uuid.uuid4().hex[:8].upper()}"

def create_phase149_readiness_rule_id() -> str:
    return f"P149RR-{uuid.uuid4().hex[:8].upper()}"

def create_phase149_readiness_gate_id() -> str:
    return f"P149RG-{uuid.uuid4().hex[:8].upper()}"

def create_backtest_analytics_context_id() -> str:
    return f"BAC-{uuid.uuid4().hex[:8].upper()}"

def create_backtest_analytics_full_review_id() -> str:
    return f"BAFR-{uuid.uuid4().hex[:8].upper()}"
