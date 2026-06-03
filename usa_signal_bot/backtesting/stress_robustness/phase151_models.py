from dataclasses import dataclass, field
from typing import Any
import json
from pathlib import Path

from usa_signal_bot.core.enums import (
    StressRobustnessStatus, StressRobustnessDecision, StressInputKind,
    StressScenarioKind, StressSeverityLevel, ScenarioReplayStatus,
    MonteCarloMethodKind, MonteCarloPathStatus, StressMetricKind,
    MonteCarloDistributionMetricKind, TailRiskDiagnosticKind,
    StressSafetyRuleKind, Phase152ReadinessStatus, Phase152ReadinessRuleKind,
    StressRobustnessQuality, StressRobustnessRiskFlag, StressRobustnessReportType
)

@dataclass
class WalkForwardIngestionResult:
    ingestion_id: str
    created_at_utc: str
    source_path: str | None
    source_review_id: str | None
    source_context_id: str | None
    available: bool
    benchmark_comparison_ingested: bool
    window_policy_built: bool
    anchored_splits_built: bool
    rolling_splits_built: bool
    fold_replay_configs_built: bool
    fold_replays_built: bool
    fold_performance_metrics_built: bool
    fold_benchmark_comparisons_built: bool
    oos_robustness_metrics_built: bool
    temporal_stability_built: bool
    degradation_diagnostics_built: bool
    robustness_summary_built: bool
    walk_forward_validation_report_built: bool
    temporal_stability_audit_built: bool
    safety_boundary_validated: bool
    phase151_readiness_gate_built: bool
    phase151_readiness_gate_passed: bool
    ready_for_phase151: bool
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
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    dashboard_started: bool
    daemon_started: bool
    scheduler_enabled: bool
    walk_forward_executed: bool
    stress_test_executed: bool
    monte_carlo_executed: bool
    produces_live_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    valid_for_phase151: bool
    risk_flags: list[StressRobustnessRiskFlag]
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any]

@dataclass
class StressInputReference:
    input_ref_id: str
    created_at_utc: str
    input_kind: StressInputKind
    source_artifact_name: str
    source_path: str | None
    source_hash: str | None
    available: bool
    read_only: bool
    row_count: int | None
    columns: list[str]
    forbidden_columns_detected: list[str]
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class StressScenarioPolicy:
    policy_id: str
    created_at_utc: str
    policy_name: str
    scenario_kinds: list[StressScenarioKind]
    severity_levels: list[StressSeverityLevel]
    deterministic_seed: int
    max_scenarios: int
    price_shock_enabled: bool
    volatility_shock_enabled: bool
    cost_shock_enabled: bool
    slippage_shock_enabled: bool
    liquidity_shock_enabled: bool
    missing_data_shock_enabled: bool
    gap_risk_shock_enabled: bool
    drawdown_shock_enabled: bool
    combined_adverse_shock_enabled: bool
    policy_valid: bool
    deterministic: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class StressScenario:
    scenario_id: str
    created_at_utc: str
    scenario_kind: StressScenarioKind
    severity_level: StressSeverityLevel
    scenario_name: str
    return_shock_multiplier: float | None
    volatility_multiplier: float | None
    cost_multiplier: float | None
    slippage_multiplier: float | None
    liquidity_haircut: float | None
    missing_data_fraction: float | None
    gap_return_shock: float | None
    drawdown_shock_floor: float | None
    combined: bool
    scenario_valid: bool
    deterministic: bool
    not_investment_advice: bool
    not_strategy_activation: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ScenarioPathPoint:
    point_id: str
    created_at_utc: str
    scenario_id: str
    timestamp: str
    original_return: float | None
    stressed_return: float | None
    original_equity: float | None
    stressed_equity: float | None
    cost_multiplier_applied: float | None
    liquidity_haircut_applied: float | None
    point_valid: bool
    research_data_only: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ScenarioReplayResult:
    result_id: str
    created_at_utc: str
    scenario_id: str
    scenario_kind: StressScenarioKind
    severity_level: StressSeverityLevel
    replay_status: ScenarioReplayStatus
    path_points: list[ScenarioPathPoint]
    final_stressed_equity: float | None
    stressed_total_return: float | None
    stressed_max_drawdown: float | None
    stressed_total_cost: float | None
    replay_hash: str | None
    deterministic: bool
    simulated_only: bool
    real_order_created: bool
    broker_execution_used: bool
    paper_state_mutated: bool
    strategy_activation_allowed: bool
    investment_advice: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ScenarioPerformanceMetric:
    metric_id: str
    created_at_utc: str
    scenario_id: str
    scenario_kind: StressScenarioKind
    severity_level: StressSeverityLevel
    metric_kind: StressMetricKind
    metric_name: str
    value: float | int | str | None
    baseline_value: float | int | str | None
    degradation_value: float | int | str | None
    non_trading_metric: bool
    not_investment_advice: bool
    not_strategy_activation: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class ScenarioDrawdownDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    scenario_id: str
    max_drawdown: float | None
    min_equity: float | None
    drawdown_duration_approx: int | None
    recovery_detected: bool
    diagnostic_notes: list[str]
    diagnostic_valid: bool
    not_investment_advice: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class CostLiquiditySensitivityResult:
    sensitivity_id: str
    created_at_utc: str
    scenario_count: int
    cost_sensitivity_score: float | None
    slippage_sensitivity_score: float | None
    liquidity_sensitivity_score: float | None
    combined_sensitivity_score: float | None
    sensitivity_notes: list[str]
    sensitivity_valid: bool
    not_strategy_activation: bool
    not_investment_advice: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class MonteCarloPolicy:
    policy_id: str
    created_at_utc: str
    method_kinds: list[MonteCarloMethodKind]
    deterministic_seed: int
    path_count: int
    block_size: int | None
    perturb_costs: bool
    perturb_slippage: bool
    perturb_liquidity: bool
    max_return_perturbation_abs: float | None
    max_cost_multiplier: float | None
    max_slippage_multiplier: float | None
    policy_valid: bool
    deterministic: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class MonteCarloPath:
    path_id: str
    created_at_utc: str
    method_kind: MonteCarloMethodKind
    path_index: int
    deterministic_seed: int
    path_status: MonteCarloPathStatus
    returns: list[float]
    cost_multipliers: list[float]
    slippage_multipliers: list[float]
    liquidity_haircuts: list[float]
    path_hash: str | None
    deterministic: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class MonteCarloReplayResult:
    result_id: str
    created_at_utc: str
    path_id: str
    method_kind: MonteCarloMethodKind
    path_index: int
    final_equity: float | None
    total_return: float | None
    max_drawdown: float | None
    total_cost: float | None
    min_equity: float | None
    replay_hash: str | None
    deterministic: bool
    simulated_only: bool
    real_order_created: bool
    broker_execution_used: bool
    paper_state_mutated: bool
    strategy_activation_allowed: bool
    investment_advice: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class MonteCarloDistributionSummary:
    summary_id: str
    created_at_utc: str
    path_count: int
    metric_values: dict[str, float | int | str | None]
    return_mean: float | None
    return_median: float | None
    return_std: float | None
    return_min: float | None
    return_max: float | None
    return_p05: float | None
    return_p95: float | None
    drawdown_mean: float | None
    drawdown_p95: float | None
    loss_probability: float | None
    ruin_probability_approx: float | None
    summary_hash: str | None
    summary_valid: bool
    non_trading_metric: bool
    not_investment_advice: bool
    not_strategy_activation: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class TailRiskDiagnostic:
    diagnostic_id: str
    created_at_utc: str
    diagnostic_kind: TailRiskDiagnosticKind
    value: float | int | str | dict[str, Any] | None
    severity_label: str
    diagnostic_notes: list[str]
    diagnostic_valid: bool
    not_investment_advice: bool
    not_strategy_activation: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class RobustnessScorecard:
    scorecard_id: str
    created_at_utc: str
    scenario_count: int
    monte_carlo_path_count: int
    scenario_pass_rate: float | None
    monte_carlo_loss_probability: float | None
    monte_carlo_ruin_probability_approx: float | None
    tail_risk_score: float | None
    cost_liquidity_sensitivity_score: float | None
    overall_robustness_score: float | None
    quality: StressRobustnessQuality
    scorecard_hash: str | None
    scorecard_valid: bool
    not_investment_advice: bool
    not_strategy_activation: bool
    not_deployment_approval: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class StressValidationReport:
    report_id: str
    created_at_utc: str
    scenarios: list[StressScenario]
    scenario_results: list[ScenarioReplayResult]
    scenario_metrics: list[ScenarioPerformanceMetric]
    drawdown_diagnostics: list[ScenarioDrawdownDiagnostic]
    cost_liquidity_sensitivity: CostLiquiditySensitivityResult
    robustness_scorecard: RobustnessScorecard
    report_hash: str | None
    report_valid: bool
    stress_test_executed: bool
    monte_carlo_executed: bool
    portfolio_optimization_enabled: bool
    strategy_activation_allowed: bool
    investment_advice: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class MonteCarloRobustnessReport:
    report_id: str
    created_at_utc: str
    policy: MonteCarloPolicy
    paths: list[MonteCarloPath]
    replay_results: list[MonteCarloReplayResult]
    distribution_summary: MonteCarloDistributionSummary
    tail_risk_diagnostics: list[TailRiskDiagnostic]
    report_hash: str | None
    report_valid: bool
    monte_carlo_executed: bool
    deterministic: bool
    simulated_only: bool
    real_order_created: bool
    broker_execution_used: bool
    paper_state_mutated: bool
    strategy_activation_allowed: bool
    investment_advice: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class StressSafetyBoundaryRule:
    rule_id: str
    created_at_utc: str
    rule_kind: StressSafetyRuleKind
    name: str
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class StressSafetyBoundaryResult:
    boundary_id: str
    created_at_utc: str
    rules: list[StressSafetyBoundaryRule]
    boundary_passed: bool
    offline_stress_monte_carlo_only: bool
    read_only_walk_forward_artifacts: bool
    local_inputs_only: bool
    deterministic_random_seed_required: bool
    no_live_trading: bool
    no_paper_trading: bool
    no_broker_execution: bool
    no_real_order_creation: bool
    no_paper_state_mutation: bool
    no_telegram_real_send: bool
    no_strategy_activation: bool
    no_portfolio_optimization: bool
    no_portfolio_allocation_output: bool
    no_deployment: bool
    no_network: bool
    no_dashboard: bool
    no_daemon: bool
    no_scheduler: bool
    research_data_only: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class Phase152ReadinessRule:
    rule_id: str
    created_at_utc: str
    rule_kind: Phase152ReadinessRuleKind
    name: str
    status: Phase152ReadinessStatus
    required: bool
    passed: bool
    expected_value: Any | None
    observed_value: Any | None
    rationale: str
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class Phase152ReadinessGate:
    gate_id: str
    created_at_utc: str
    status: Phase152ReadinessStatus
    rules: list[Phase152ReadinessRule]
    stress_validation_report: StressValidationReport
    monte_carlo_report: MonteCarloRobustnessReport
    robustness_scorecard: RobustnessScorecard
    safety_boundary: StressSafetyBoundaryResult
    ready_for_phase152: bool
    research_data_only: bool
    offline_backtest_research_only: bool
    live_trading_enabled: bool
    paper_trading_enabled: bool
    broker_execution_enabled: bool
    real_order_creation_enabled: bool
    paper_state_mutation_enabled: bool
    stress_test_executed: bool
    monte_carlo_executed: bool
    deployment_allowed: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class StressRobustnessContext:
    context_id: str
    created_at_utc: str
    status: StressRobustnessStatus
    decision: StressRobustnessDecision
    source_walk_forward_review_id: str | None
    ingestion: WalkForwardIngestionResult
    input_references: list[StressInputReference]
    scenario_policy: StressScenarioPolicy
    scenarios: list[StressScenario]
    stress_validation_report: StressValidationReport
    monte_carlo_report: MonteCarloRobustnessReport
    robustness_scorecard: RobustnessScorecard
    safety_boundary: StressSafetyBoundaryResult
    phase152_readiness_gate: Phase152ReadinessGate
    walk_forward_ingested: bool
    artifacts_loaded: bool
    inputs_resolved: bool
    scenario_policy_built: bool
    price_shock_scenarios_built: bool
    volatility_shock_scenarios_built: bool
    cost_shock_scenarios_built: bool
    slippage_shock_scenarios_built: bool
    liquidity_shock_scenarios_built: bool
    missing_data_shock_scenarios_built: bool
    gap_risk_scenarios_built: bool
    drawdown_shock_scenarios_built: bool
    scenario_paths_built: bool
    scenario_replays_built: bool
    scenario_metrics_built: bool
    scenario_drawdown_diagnostics_built: bool
    cost_liquidity_sensitivity_built: bool
    monte_carlo_policy_built: bool
    monte_carlo_paths_built: bool
    monte_carlo_replays_built: bool
    monte_carlo_distributions_built: bool
    tail_risk_diagnostics_built: bool
    robustness_scorecard_built: bool
    stress_validation_report_built: bool
    monte_carlo_robustness_report_built: bool
    safety_boundary_validated: bool
    phase152_readiness_gate_built: bool
    phase152_readiness_gate_passed: bool
    ready_for_phase152: bool
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
    paid_api_used: bool
    scraping_used: bool
    html_parsing_used: bool
    dashboard_started: bool
    daemon_started: bool
    scheduler_enabled: bool
    stress_test_executed: bool
    monte_carlo_executed: bool
    produces_live_signal: bool
    produces_order_decision: bool
    produces_portfolio_weights: bool
    investment_advice: bool
    warnings: list[str]
    errors: list[str]
    risk_flags: list[StressRobustnessRiskFlag]
    metadata: dict[str, Any]

@dataclass
class StressRobustnessFullReview:
    review_id: str
    created_at_utc: str
    report_type: StressRobustnessReportType
    ingestion: WalkForwardIngestionResult
    context: StressRobustnessContext
    stress_validation_report: StressValidationReport
    monte_carlo_report: MonteCarloRobustnessReport
    robustness_scorecard: RobustnessScorecard
    safety_boundary: StressSafetyBoundaryResult
    phase152_readiness_gate: Phase152ReadinessGate
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

import uuid
import datetime

def _create_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"

def create_walk_forward_ingestion_id() -> str:
    return _create_id("wfingest")

def create_stress_input_reference_id() -> str:
    return _create_id("stresin")

def create_stress_scenario_policy_id() -> str:
    return _create_id("strespol")

def create_stress_scenario_id() -> str:
    return _create_id("stressce")

def create_scenario_path_point_id() -> str:
    return _create_id("scepath")

def create_scenario_replay_result_id() -> str:
    return _create_id("scerep")

def create_scenario_performance_metric_id() -> str:
    return _create_id("scemetr")

def create_scenario_drawdown_diagnostic_id() -> str:
    return _create_id("scedraw")

def create_cost_liquidity_sensitivity_id() -> str:
    return _create_id("stresens")

def create_monte_carlo_policy_id() -> str:
    return _create_id("mcpol")

def create_monte_carlo_path_id() -> str:
    return _create_id("mcpath")

def create_monte_carlo_replay_result_id() -> str:
    return _create_id("mcrep")

def create_monte_carlo_distribution_summary_id() -> str:
    return _create_id("mcdist")

def create_tail_risk_diagnostic_id() -> str:
    return _create_id("tailrisk")

def create_robustness_scorecard_id() -> str:
    return _create_id("robscore")

def create_stress_validation_report_id() -> str:
    return _create_id("stresval")

def create_monte_carlo_robustness_report_id() -> str:
    return _create_id("mcreport")

def create_stress_safety_boundary_rule_id() -> str:
    return _create_id("stresrule")

def create_stress_safety_boundary_result_id() -> str:
    return _create_id("stresbound")

def create_phase152_readiness_rule_id() -> str:
    return _create_id("p152rule")

def create_phase152_readiness_gate_id() -> str:
    return _create_id("p152gate")

def create_stress_robustness_context_id() -> str:
    return _create_id("stresctx")

def create_stress_robustness_full_review_id() -> str:
    return _create_id("stresrev")
