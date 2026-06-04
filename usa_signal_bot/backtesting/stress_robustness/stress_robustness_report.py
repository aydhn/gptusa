import datetime

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressRobustnessContext,
    StressRobustnessFullReview,
    create_stress_robustness_context_id,
    create_stress_robustness_full_review_id
)
from usa_signal_bot.core.enums import StressRobustnessStatus, StressRobustnessDecision, StressRobustnessReportType

def build_stress_robustness_context() -> StressRobustnessContext:
    # Dummy for now. Will be populated by pipeline.
    return StressRobustnessContext(
        context_id=create_stress_robustness_context_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        status=StressRobustnessStatus.CREATED,
        decision=StressRobustnessDecision.LOAD_WALK_FORWARD_ARTIFACTS,
        source_walk_forward_review_id=None,
        ingestion=None, input_references=[], scenario_policy=None, scenarios=[],
        stress_validation_report=None, monte_carlo_report=None, robustness_scorecard=None,
        safety_boundary=None, phase152_readiness_gate=None,
        walk_forward_ingested=False, artifacts_loaded=False, inputs_resolved=False,
        scenario_policy_built=False, price_shock_scenarios_built=False, volatility_shock_scenarios_built=False,
        cost_shock_scenarios_built=False, slippage_shock_scenarios_built=False, liquidity_shock_scenarios_built=False,
        missing_data_shock_scenarios_built=False, gap_risk_scenarios_built=False, drawdown_shock_scenarios_built=False,
        scenario_paths_built=False, scenario_replays_built=False, scenario_metrics_built=False,
        scenario_drawdown_diagnostics_built=False, cost_liquidity_sensitivity_built=False,
        monte_carlo_policy_built=False, monte_carlo_paths_built=False, monte_carlo_replays_built=False,
        monte_carlo_distributions_built=False, tail_risk_diagnostics_built=False, robustness_scorecard_built=False,
        stress_validation_report_built=False, monte_carlo_robustness_report_built=False,
        safety_boundary_validated=False, phase152_readiness_gate_built=False, phase152_readiness_gate_passed=False,
        ready_for_phase152=False, research_data_only=True, offline_backtest_research_only=True, deterministic=True,
        live_trading_enabled=False, paper_trading_enabled=False, broker_execution_enabled=False,
        real_order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False,
        strategy_activation_allowed=False, portfolio_optimization_enabled=False, portfolio_allocation_output_enabled=False,
        deployment_allowed=False, network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
        dashboard_started=False, daemon_started=False, scheduler_enabled=False, stress_test_executed=False,
        monte_carlo_executed=False, produces_live_signal=False, produces_order_decision=False,
        produces_portfolio_weights=False, investment_advice=False, warnings=[], errors=[], risk_flags=[], metadata={}
    )

def build_stress_robustness_full_review(context: StressRobustnessContext) -> StressRobustnessFullReview:
    return StressRobustnessFullReview(
        review_id=create_stress_robustness_full_review_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        report_type=StressRobustnessReportType.FULL_PHASE151_REVIEW,
        ingestion=context.ingestion,
        context=context,
        stress_validation_report=context.stress_validation_report,
        monte_carlo_report=context.monte_carlo_report,
        robustness_scorecard=context.robustness_scorecard,
        safety_boundary=context.safety_boundary,
        phase152_readiness_gate=context.phase152_readiness_gate,
        output_paths={},
        warnings=context.warnings,
        errors=context.errors
    )
