import pytest
from usa_signal_bot.portfolio.construction.phase155_models import (
    SizingPrototypeIngestionResult,
    PortfolioConstructionPolicy,
    PortfolioConstructionPolicyKind,
    create_portfolio_construction_policy_id,
    _now_str
)

def test_portfolio_construction_policy_creation():
    policy = PortfolioConstructionPolicy(
        policy_id=create_portfolio_construction_policy_id(),
        created_at_utc=_now_str(),
        policy_kind=PortfolioConstructionPolicyKind.CONTRACT_ONLY_SANDBOX_POLICY,
        policy_name="Test Policy",
        max_sandbox_weight_fraction=0.1,
        min_sandbox_weight_fraction=0.0,
        max_group_sandbox_weight_fraction=0.4,
        max_turnover_sandbox_fraction=0.25,
        risk_budget_weight=0.5,
        robustness_weight=0.5,
        sizing_weight=0.0,
        liquidity_weight=0.0,
        cost_weight=0.0,
        diversification_weight=0.0,
        actual_target_weights_allowed=False,
        actual_allocation_allowed=False,
        capital_deployment_allowed=False,
        portfolio_optimization_allowed=False
    )
    assert policy.actual_target_weights_allowed is False
    assert policy.policy_name == "Test Policy"
    assert policy.research_data_only is True

def test_sizing_prototype_ingestion_result():
    res = SizingPrototypeIngestionResult(
        ingestion_id="test",
        created_at_utc="2023",
        source_path=None,
        source_review_id=None,
        source_context_id=None,
        available=True,
        portfolio_foundation_ingested=True,
        inputs_resolved=True,
        sizing_policy_built=True,
        method_contracts_built=True,
        fixed_fractional_sizing_built=True,
        volatility_adjusted_sizing_built=True,
        drawdown_adjusted_sizing_built=True,
        cost_aware_sizing_built=True,
        liquidity_aware_sizing_built=True,
        robustness_adjusted_sizing_built=True,
        comparison_matrix_built=True,
        sizing_diagnostics_built=True,
        sensitivity_report_built=True,
        risk_budget_adherence_built=True,
        safety_boundary_validated=True,
        phase155_readiness_gate_built=True,
        phase155_readiness_gate_passed=True,
        ready_for_phase155=True,
        research_data_only=True,
        sizing_research_prototype_only=True,
        deterministic=True,
        live_trading_enabled=False,
        paper_trading_enabled=False,
        broker_execution_enabled=False,
        real_order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        strategy_activation_allowed=False,
        actual_portfolio_construction_executed=False,
        actual_position_sizing_executed=False,
        portfolio_optimization_enabled=False,
        rebalancing_enabled=False,
        target_weights_produced=False,
        allocation_output_produced=False,
        order_size_produced=False,
        capital_deployment_allowed=False,
        deployment_allowed=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        dashboard_started=False,
        daemon_started=False,
        scheduler_enabled=False,
        produces_live_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        valid_for_phase155=True
    )
    assert res.live_trading_enabled is False
    assert res.ready_for_phase155 is True
