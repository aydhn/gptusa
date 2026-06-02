from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.enums import (
    BacktestInputKind,
    BacktestDatasetContractStatus,
    BacktestTimeModelKind,
    ExecutionAssumptionKind,
    TransactionCostKind,
    SpreadModelKind,
    SlippageModelKind,
    LiquidityGuardKind,
    PartialFillAssumptionKind,
    ExecutionLatencyKind,
    MarketSimulationContractKind,
    BacktestSafetyRuleKind,
    BacktestReadinessStatus,
    BacktestReadinessRuleKind,
    BacktestFoundationRiskFlag,
    BacktestFoundationStatus,
    BacktestFoundationDecision,
    BacktestFoundationReportType
)

@dataclass
class AdvancedMLClosureIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    drift_monitoring_ingested: bool
    explainability_report_built: bool
    artifact_lineage_built: bool
    ml_governance_closure_built: bool
    advanced_ml_final_audit_built: bool
    non_activation_boundary_validated: bool
    final_model_cards_updated: bool
    acceptance_gate_built: bool
    acceptance_gate_passed: bool
    ready_for_phase146: bool
    phase136_to_145_closed: bool
    research_data_only: bool
    offline_ml_research_only: bool
    activation_allowed: bool
    strategy_activation_allowed: bool
    deployment_allowed: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    telegram_real_send_enabled: bool
    scraping_enabled: bool
    html_parse_enabled: bool
    paid_api_enabled: bool
    dashboard_enabled: bool
    network_default_enabled: bool
    daemon_started: bool
    scheduler_enabled: bool
    live_inference_enabled: bool
    online_inference_enabled: bool
    live_monitoring_enabled: bool
    backtest_executed: bool
    produces_trade_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    valid_for_phase146: bool
    risk_flags: list[BacktestFoundationRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class BacktestInputReference:
    input_ref_id: str
    created_at_utc: str
    input_kind: BacktestInputKind
    source_artifact_name: str
    source_path: str | None
    source_hash: str | None
    available: bool
    read_only: bool
    required: bool
    row_count: int | None
    columns: list[str]
    forbidden_columns_detected: list[str]
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestDatasetContract:
    contract_id: str
    created_at_utc: str
    status: BacktestDatasetContractStatus
    required_inputs: list[BacktestInputKind]
    optional_inputs: list[BacktestInputKind]
    required_columns_by_input: dict[str, list[str]]
    time_column: str
    symbol_column: str
    price_columns: list[str]
    volume_columns: list[str]
    adjusted_price_required: bool
    corporate_actions_supported: bool
    market_calendar_supported: bool
    min_rows_per_symbol: int
    timezone_policy: str
    survivorship_bias_notice: str
    lookahead_bias_notice: str
    contract_valid: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestResearchInputContract:
    contract_id: str
    created_at_utc: str
    allowed_research_columns: list[str]
    forbidden_active_trading_columns: list[str]
    signal_activation_allowed: bool
    order_decision_allowed: bool
    paper_mutation_allowed: bool
    portfolio_allocation_allowed: bool
    strategy_activation_allowed: bool
    contract_valid: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestEventTimelineContract:
    timeline_id: str
    created_at_utc: str
    time_model_kind: BacktestTimeModelKind
    bar_timestamp_policy: str
    feature_available_time_policy: str
    research_prediction_available_time_policy: str
    execution_decision_time_policy: str
    fill_time_policy: str
    prevents_lookahead_bias: bool
    event_order: list[str]
    timeline_valid: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ExecutionAssumptionContract:
    assumption_id: str
    created_at_utc: str
    execution_kind: ExecutionAssumptionKind
    description: str
    execution_price_source: str
    fill_price_policy: str
    allow_same_bar_execution: bool
    allow_next_bar_execution: bool
    allow_live_execution: bool
    order_creation_allowed: bool
    broker_execution_allowed: bool
    assumption_valid: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class TransactionCostModel:
    model_id: str
    created_at_utc: str
    cost_kind: TransactionCostKind
    flat_bps: float | None
    flat_per_share: float | None
    min_cost: float | None
    max_cost: float | None
    applies_to_buy_side: bool
    applies_to_sell_side: bool
    cost_model_valid: bool
    live_broker_fee_sync_enabled: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class CommissionModel:
    model_id: str
    created_at_utc: str
    cost_kind: TransactionCostKind
    per_share_commission: float | None
    flat_ticket_fee: float | None
    bps_commission: float | None
    min_commission: float | None
    commission_model_valid: bool
    live_broker_fee_sync_enabled: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class SpreadModel:
    model_id: str
    created_at_utc: str
    spread_kind: SpreadModelKind
    fixed_bps: float | None
    price_bucket_rules: list[dict[str, Any]]
    volume_bucket_rules: list[dict[str, Any]]
    spread_model_valid: bool
    live_quote_required: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class SlippageModel:
    model_id: str
    created_at_utc: str
    slippage_kind: SlippageModelKind
    fixed_bps: float | None
    volume_participation_rate: float | None
    volatility_multiplier: float | None
    conservative_buffer_bps: float | None
    slippage_model_valid: bool
    live_quote_required: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class LiquidityGuard:
    guard_id: str
    created_at_utc: str
    guard_kinds: list[LiquidityGuardKind]
    min_dollar_volume: float | None
    min_share_volume: float | None
    max_volume_participation: float | None
    min_price: float | None
    missing_volume_blocks_execution: bool
    guard_valid: bool
    order_creation_allowed: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class PartialFillAssumption:
    assumption_id: str
    created_at_utc: str
    assumption_kind: PartialFillAssumptionKind
    volume_cap_rate: float | None
    allow_partial_fill_metadata: bool
    no_fill_if_illiquid: bool
    live_fill_tracking_enabled: bool
    assumption_valid: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ExecutionLatencyAssumption:
    assumption_id: str
    created_at_utc: str
    latency_kind: ExecutionLatencyKind
    latency_bars: int
    latency_sessions: int
    configurable_metadata_only: bool
    live_latency_tracking_enabled: bool
    assumption_valid: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class MarketSimulationContract:
    contract_id: str
    created_at_utc: str
    simulation_kind: MarketSimulationContractKind
    dataset_contract_id: str
    event_timeline_id: str
    execution_assumption_id: str
    transaction_cost_model_id: str
    commission_model_id: str
    spread_model_id: str
    slippage_model_id: str
    liquidity_guard_id: str
    partial_fill_assumption_id: str
    execution_latency_assumption_id: str
    supports_adjusted_prices: bool
    supports_corporate_actions: bool
    supports_market_calendar: bool
    allows_live_execution: bool
    allows_order_creation: bool
    allows_paper_mutation: bool
    simulation_contract_valid: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestSafetyBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: BacktestSafetyRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestSafetyBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: list[BacktestSafetyBoundaryRule]
    boundary_passed: bool
    offline_backtest_research_only: bool
    no_live_trading: bool
    no_paper_trading: bool
    no_broker_execution: bool
    no_order_creation: bool
    no_paper_state_mutation: bool
    no_telegram_real_send: bool
    no_strategy_activation: bool
    no_portfolio_allocation: bool
    no_deployment: bool
    no_network: bool
    no_dashboard: bool
    no_daemon: bool
    no_scheduler: bool
    no_full_backtest_run_phase146: bool
    no_walk_forward_phase146: bool
    no_stress_test_phase146: bool
    no_monte_carlo_phase146: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: BacktestReadinessRuleKind
    name: str
    status: BacktestReadinessStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestReadinessGate:
    gate_id: str
    created_at_utc: str
    status: BacktestReadinessStatus
    rules: list[BacktestReadinessRule]
    dataset_contract: BacktestDatasetContract
    research_input_contract: BacktestResearchInputContract
    market_simulation_contract: MarketSimulationContract
    safety_boundary: BacktestSafetyBoundaryResult
    ready_for_phase147: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    broker_execution_enabled: bool
    order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    full_backtest_run_executed: bool
    walk_forward_executed: bool
    stress_test_executed: bool
    monte_carlo_executed: bool
    deployment_allowed: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestFoundationContext:
    context_id: str
    created_at_utc: str
    status: BacktestFoundationStatus
    decision: BacktestFoundationDecision
    source_advanced_ml_closure_review_id: str | None
    ingestion: AdvancedMLClosureIngestionResult
    input_references: list[BacktestInputReference]
    dataset_contract: BacktestDatasetContract
    research_input_contract: BacktestResearchInputContract
    event_timeline: BacktestEventTimelineContract
    execution_assumption: ExecutionAssumptionContract
    transaction_cost_model: TransactionCostModel
    commission_model: CommissionModel
    spread_model: SpreadModel
    slippage_model: SlippageModel
    liquidity_guard: LiquidityGuard
    partial_fill_assumption: PartialFillAssumption
    execution_latency_assumption: ExecutionLatencyAssumption
    market_simulation_contract: MarketSimulationContract
    safety_boundary: BacktestSafetyBoundaryResult
    readiness_gate: BacktestReadinessGate
    advanced_ml_closure_ingested: bool
    artifacts_loaded: bool
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
    warnings: list[str]
    errors: list[str]
    risk_flags: list[BacktestFoundationRiskFlag]
    metadata: dict[str, Any]

@dataclass
class BacktestFoundationFullReview:
    review_id: str
    created_at_utc: str
    report_type: BacktestFoundationReportType
    ingestion: AdvancedMLClosureIngestionResult
    context: BacktestFoundationContext
    dataset_contract: BacktestDatasetContract
    research_input_contract: BacktestResearchInputContract
    market_simulation_contract: MarketSimulationContract
    safety_boundary: BacktestSafetyBoundaryResult
    readiness_gate: BacktestReadinessGate
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

import uuid

def create_advanced_ml_closure_ingestion_id() -> str:
    return f"ingest_{uuid.uuid4().hex[:8]}"

def create_backtest_input_reference_id() -> str:
    return f"input_{uuid.uuid4().hex[:8]}"

def create_backtest_dataset_contract_id() -> str:
    return f"dscontract_{uuid.uuid4().hex[:8]}"

def create_backtest_research_input_contract_id() -> str:
    return f"rincontract_{uuid.uuid4().hex[:8]}"

def create_backtest_event_timeline_contract_id() -> str:
    return f"timeline_{uuid.uuid4().hex[:8]}"

def create_execution_assumption_contract_id() -> str:
    return f"execassm_{uuid.uuid4().hex[:8]}"

def create_transaction_cost_model_id() -> str:
    return f"txcost_{uuid.uuid4().hex[:8]}"

def create_commission_model_id() -> str:
    return f"comm_{uuid.uuid4().hex[:8]}"

def create_spread_model_id() -> str:
    return f"spread_{uuid.uuid4().hex[:8]}"

def create_slippage_model_id() -> str:
    return f"slip_{uuid.uuid4().hex[:8]}"

def create_liquidity_guard_id() -> str:
    return f"liq_{uuid.uuid4().hex[:8]}"

def create_partial_fill_assumption_id() -> str:
    return f"pfill_{uuid.uuid4().hex[:8]}"

def create_execution_latency_assumption_id() -> str:
    return f"lat_{uuid.uuid4().hex[:8]}"

def create_market_simulation_contract_id() -> str:
    return f"mktsim_{uuid.uuid4().hex[:8]}"

def create_backtest_safety_boundary_rule_id() -> str:
    return f"srule_{uuid.uuid4().hex[:8]}"

def create_backtest_safety_boundary_result_id() -> str:
    return f"sbound_{uuid.uuid4().hex[:8]}"

def create_backtest_readiness_rule_id() -> str:
    return f"rrule_{uuid.uuid4().hex[:8]}"

def create_backtest_readiness_gate_id() -> str:
    return f"rgate_{uuid.uuid4().hex[:8]}"

def create_backtest_foundation_context_id() -> str:
    return f"bfctx_{uuid.uuid4().hex[:8]}"

def create_backtest_foundation_full_review_id() -> str:
    return f"bfrev_{uuid.uuid4().hex[:8]}"
