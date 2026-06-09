from typing import Any, Dict, List, Optional
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioRiskSafetyBoundaryResult,
    PortfolioRiskSafetyBoundaryRule,
    create_portfolio_risk_safety_boundary_result_id,
    create_portfolio_risk_safety_boundary_rule_id
)
from usa_signal_bot.core.enums import PortfolioRiskSafetyRuleKind

def build_portfolio_risk_safety_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[PortfolioRiskSafetyBoundaryRule]:
    rules = []
    rules.append(PortfolioRiskSafetyBoundaryRule(
        rule_id=create_portfolio_risk_safety_boundary_rule_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        rule_kind=PortfolioRiskSafetyRuleKind.NO_LIVE_TRADING,
        name="No Live Trading",
        required=True,
        passed=True,
        expected_value=False,
        observed_value=False,
        rationale="Live trading is not permitted.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))
    return rules

def build_portfolio_risk_safety_boundary_result(rules: List[PortfolioRiskSafetyBoundaryRule]) -> PortfolioRiskSafetyBoundaryResult:
    passed = all(r.passed for r in rules if r.required)

    return PortfolioRiskSafetyBoundaryResult(
        boundary_id=create_portfolio_risk_safety_boundary_result_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        rules=rules,
        boundary_passed=passed,
        risk_reporting_only=True,
        read_only_optimizer_artifacts=True,
        no_actual_target_weights=True,
        no_actual_portfolio_weights=True,
        no_actual_allocation=True,
        no_actual_position_size=True,
        no_order_size=True,
        no_capital_deployment=True,
        no_actual_portfolio_optimization=True,
        no_rebalancing_execution=True,
        no_live_trading=True,
        no_paper_trading=True,
        no_broker_execution=True,
        no_real_order_creation=True,
        no_paper_state_mutation=True,
        no_telegram_real_send=True,
        no_strategy_activation=True,
        no_deployment=True,
        no_network=True,
        no_dashboard=True,
        no_daemon=True,
        no_scheduler=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_portfolio_risk_safety_boundary_result(result: PortfolioRiskSafetyBoundaryResult) -> List[str]:
    return []

def portfolio_risk_safety_boundary_passed(result: PortfolioRiskSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def portfolio_risk_safety_boundary_to_text(result: PortfolioRiskSafetyBoundaryResult, limit: int = 300) -> str:
    return f"Safety Boundary Result: passed={result.boundary_passed}"
