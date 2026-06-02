from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from usa_signal_bot.core.enums import (
    BacktestRunStatus, BacktestRunDecision, ResearchDecisionKind,
    ResearchExposureSide, SimulationClockKind, PriceEventKind,
    SimulatedFillKind, CostApplicationKind, BacktestRunMetricKind,
    BacktestRunSafetyRuleKind, BacktestRunValidationStatus,
    BacktestRunValidationRuleKind, BacktestRunQuality, BacktestRunRiskFlag,
    BacktestRunReportType, BacktestTimeModelKind
)
import uuid
import datetime

def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_backtest_foundation_ingestion_id() -> str: return generate_id("bfin")
def create_backtest_run_config_id() -> str: return generate_id("brcf")
def create_research_decision_record_id() -> str: return generate_id("rdr")
def create_research_decision_stream_id() -> str: return generate_id("rds")
def create_simulation_clock_id() -> str: return generate_id("sclk")
def create_price_event_id() -> str: return generate_id("pevt")
def create_price_event_stream_id() -> str: return generate_id("pest")
def create_simulated_fill_record_id() -> str: return generate_id("sfr")
def create_cost_ledger_record_id() -> str: return generate_id("clr")
def create_exposure_state_record_id() -> str: return generate_id("esr")
def create_equity_curve_point_id() -> str: return generate_id("ecp")
def create_drawdown_point_id() -> str: return generate_id("ddp")
def create_backtest_ledger_id() -> str: return generate_id("bl")
def create_basic_performance_summary_id() -> str: return generate_id("bps")
def create_backtest_run_artifact_id() -> str: return generate_id("bra")
def create_backtest_run_safety_boundary_rule_id() -> str: return generate_id("sbr")
def create_backtest_run_safety_boundary_result_id() -> str: return generate_id("sbrs")
def create_backtest_run_validation_rule_id() -> str: return generate_id("vru")
def create_backtest_run_validation_gate_id() -> str: return generate_id("vg")
def create_backtest_run_context_id() -> str: return generate_id("brc")
def create_backtest_run_full_review_id() -> str: return generate_id("brfr")

@dataclass
class BacktestFoundationIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: Optional[str]
    source_review_id: Optional[str]
    source_context_id: Optional[str]
    available: bool
    advanced_ml_closure_ingested: bool
    inputs_resolved: bool
    dataset_contract_built: bool
    research_input_boundary_built: bool
    event_timeline_built: bool
    execution_assumptions_built: bool
    transaction_cost_model_built: bool
    commission_model_built: bool
    spread_model_built: bool
    slippage_model_built: bool
    liquidity_guard_built: bool
    partial_fill_assumptions_built: bool
    execution_latency_assumptions_built: bool
    market_simulation_contract_built: bool
    safety_boundary_validated: bool
    readiness_gate_built: bool
    readiness_gate_passed: bool
    ready_for_phase147: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    strategy_activation_allowed: bool
    portfolio_allocation_allowed: bool
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
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    valid_for_phase147: bool
    risk_flags: List[BacktestRunRiskFlag]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any]

@dataclass
class BacktestRunConfig:
    config_id: str
    created_at_utc: str
    run_name: str
    initial_cash: float
    currency: str
    exposure_side: ResearchExposureSide
    max_single_symbol_exposure_fraction: float
    allow_fractional_shares: bool
    allow_short_exposure: bool
    allow_leverage: bool
    deterministic_seed: int
    time_model_kind: BacktestTimeModelKind
    execution_assumption_id: Optional[str]
    market_simulation_contract_id: Optional[str]
    run_config_valid: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    broker_execution_enabled: bool
    real_order_creation_enabled: bool
    strategy_activation_allowed: bool
    portfolio_optimization_enabled: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ResearchDecisionRecord:
    decision_id: str
    created_at_utc: str
    symbol: str
    timestamp: str
    decision_kind: ResearchDecisionKind
    exposure_side: ResearchExposureSide
    research_score: Optional[float]
    research_label: Optional[str]
    source_prediction_id: Optional[str]
    deterministic_rank: Optional[int]
    not_live_signal: bool
    not_order_decision: bool
    not_investment_advice: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ResearchDecisionStream:
    stream_id: str
    created_at_utc: str
    records: List[ResearchDecisionRecord]
    row_count: int
    symbols: List[str]
    start_timestamp: Optional[str]
    end_timestamp: Optional[str]
    stream_hash: Optional[str]
    stream_valid: bool
    deterministic: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    produces_live_signal: bool
    produces_order_decision: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class SimulationClock:
    clock_id: str
    created_at_utc: str
    clock_kind: SimulationClockKind
    timestamps: List[str]
    event_count: int
    timezone_policy: str
    deterministic: bool
    clock_valid: bool
    no_scheduler: bool
    no_daemon: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class PriceEvent:
    event_id: str
    created_at_utc: str
    symbol: str
    timestamp: str
    event_kind: PriceEventKind
    open_price: Optional[float]
    high_price: Optional[float]
    low_price: Optional[float]
    close_price: Optional[float]
    adjusted_close: Optional[float]
    volume: Optional[float]
    event_valid: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class PriceEventStream:
    stream_id: str
    created_at_utc: str
    events: List[PriceEvent]
    row_count: int
    symbols: List[str]
    start_timestamp: Optional[str]
    end_timestamp: Optional[str]
    stream_hash: Optional[str]
    stream_valid: bool
    deterministic: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class SimulatedFillRecord:
    fill_id: str
    created_at_utc: str
    run_id: str
    symbol: str
    decision_timestamp: str
    fill_timestamp: str
    fill_kind: SimulatedFillKind
    exposure_side: ResearchExposureSide
    requested_quantity: float
    simulated_filled_quantity: float
    reference_price: Optional[float]
    simulated_fill_price_before_costs: Optional[float]
    simulated_fill_price_after_costs: Optional[float]
    simulated_notional_before_costs: Optional[float]
    simulated_notional_after_costs: Optional[float]
    liquidity_blocked: bool
    missing_price_blocked: bool
    partial_fill: bool
    simulated_only: bool
    real_order_created: bool
    broker_execution_used: bool
    paper_state_mutated: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class CostLedgerRecord:
    cost_id: str
    created_at_utc: str
    run_id: str
    fill_id: Optional[str]
    symbol: str
    timestamp: str
    cost_kind: CostApplicationKind
    transaction_cost_amount: float
    commission_amount: float
    spread_cost_amount: float
    slippage_cost_amount: float
    total_cost_amount: float
    cost_bps_effective: Optional[float]
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class ExposureStateRecord:
    state_id: str
    created_at_utc: str
    run_id: str
    symbol: str
    timestamp: str
    exposure_side: ResearchExposureSide
    simulated_quantity: float
    simulated_cash: float
    simulated_market_value: float
    simulated_equity: float
    simulated_cost_basis: Optional[float]
    simulated_unrealized_return: Optional[float]
    state_valid: bool
    not_live_position: bool
    not_portfolio_allocation: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class EquityCurvePoint:
    point_id: str
    created_at_utc: str
    run_id: str
    timestamp: str
    simulated_equity: float
    simulated_cash: float
    simulated_market_value: float
    cumulative_simulated_return: float
    point_valid: bool
    research_data_only: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class DrawdownPoint:
    point_id: str
    created_at_utc: str
    run_id: str
    timestamp: str
    simulated_equity: float
    running_peak_equity: float
    drawdown_fraction: float
    drawdown_percent: float
    point_valid: bool
    research_data_only: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BacktestLedger:
    ledger_id: str
    created_at_utc: str
    run_id: str
    fills: List[SimulatedFillRecord]
    costs: List[CostLedgerRecord]
    exposure_states: List[ExposureStateRecord]
    fill_count: int
    cost_record_count: int
    exposure_state_count: int
    ledger_hash: Optional[str]
    ledger_valid: bool
    simulated_only: bool
    real_order_created: bool
    broker_execution_used: bool
    paper_state_mutated: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BasicPerformanceSummary:
    summary_id: str
    created_at_utc: str
    run_id: str
    metric_values: Dict[str, Any]
    total_return: Optional[float]
    annualized_return_approx: Optional[float]
    volatility_approx: Optional[float]
    max_drawdown: Optional[float]
    hit_rate_approx: Optional[float]
    simulated_turnover: Optional[float]
    simulated_total_cost: Optional[float]
    simulated_fill_count: int
    simulated_no_fill_count: int
    summary_hash: Optional[str]
    summary_valid: bool
    non_trading_metric: bool
    not_investment_advice: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BacktestRunArtifact:
    run_id: str
    created_at_utc: str
    run_name: str
    config: BacktestRunConfig
    research_decision_stream: ResearchDecisionStream
    price_event_stream: PriceEventStream
    ledger: BacktestLedger
    equity_curve: List[EquityCurvePoint]
    drawdown_curve: List[DrawdownPoint]
    performance_summary: BasicPerformanceSummary
    output_paths: Dict[str, str]
    run_hash: Optional[str]
    run_valid: bool
    deterministic: bool
    offline_backtest_research_only: bool
    full_backtest_run_executed: bool
    walk_forward_executed: bool
    stress_test_executed: bool
    monte_carlo_executed: bool
    benchmark_comparison_executed: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    broker_execution_enabled: bool
    real_order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    strategy_activation_allowed: bool
    portfolio_optimization_enabled: bool
    deployment_allowed: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BacktestRunSafetyBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: BacktestRunSafetyRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BacktestRunSafetyBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: List[BacktestRunSafetyBoundaryRule]
    boundary_passed: bool
    offline_backtest_only: bool
    deterministic_run_only: bool
    no_live_trading: bool
    no_paper_trading: bool
    no_broker_execution: bool
    no_real_order_creation: bool
    no_paper_state_mutation: bool
    no_telegram_real_send: bool
    no_strategy_activation: bool
    no_portfolio_optimization: bool
    no_deployment: bool
    no_network: bool
    no_dashboard: bool
    no_daemon: bool
    no_scheduler: bool
    no_walk_forward_phase147: bool
    no_stress_test_phase147: bool
    no_monte_carlo_phase147: bool
    no_benchmark_comparison_phase147: bool
    research_data_only: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BacktestRunValidationRule:
    rule_id: str
    created_at_utc: str
    rule_kind: BacktestRunValidationRuleKind
    name: str
    status: BacktestRunValidationStatus
    required: bool
    passed: bool
    expected_value: Optional[Any]
    observed_value: Optional[Any]
    rationale: str
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BacktestRunValidationGate:
    gate_id: str
    created_at_utc: str
    status: BacktestRunValidationStatus
    rules: List[BacktestRunValidationRule]
    run_artifact: BacktestRunArtifact
    safety_boundary: BacktestRunSafetyBoundaryResult
    ready_for_phase148: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    broker_execution_enabled: bool
    real_order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    deployment_allowed: bool
    investment_advice: bool
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BacktestRunContext:
    context_id: str
    created_at_utc: str
    status: BacktestRunStatus
    decision: BacktestRunDecision
    source_backtest_foundation_review_id: Optional[str]
    ingestion: BacktestFoundationIngestionResult
    config: BacktestRunConfig
    research_decision_stream: ResearchDecisionStream
    simulation_clock: SimulationClock
    price_event_stream: PriceEventStream
    run_artifact: Optional[BacktestRunArtifact]
    safety_boundary: Optional[BacktestRunSafetyBoundaryResult]
    validation_gate: Optional[BacktestRunValidationGate]
    backtest_foundation_ingested: bool
    artifacts_loaded: bool
    inputs_resolved: bool
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
    warnings: List[str]
    errors: List[str]
    risk_flags: List[BacktestRunRiskFlag]
    metadata: Dict[str, Any]

@dataclass
class BacktestRunFullReview:
    review_id: str
    created_at_utc: str
    report_type: BacktestRunReportType
    ingestion: BacktestFoundationIngestionResult
    context: BacktestRunContext
    run_artifact: Optional[BacktestRunArtifact]
    performance_summary: Optional[BasicPerformanceSummary]
    safety_boundary: Optional[BacktestRunSafetyBoundaryResult]
    validation_gate: Optional[BacktestRunValidationGate]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]
