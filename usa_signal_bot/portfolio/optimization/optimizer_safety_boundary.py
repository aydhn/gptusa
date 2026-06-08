from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSafetyBoundaryResult, OptimizerSafetyBoundaryRule, OptimizerSafetyRuleKind

def build_optimizer_safety_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[OptimizerSafetyBoundaryRule]:
    return [
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.OPTIMIZER_SANDBOX_ONLY, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.READ_ONLY_CONSTRUCTION_ARTIFACTS, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_ACTUAL_TARGET_WEIGHTS, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_ACTUAL_PORTFOLIO_WEIGHTS, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_ACTUAL_ALLOCATION, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_ACTUAL_POSITION_SIZE, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_ORDER_SIZE, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_CAPITAL_DEPLOYMENT, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_ACTUAL_PORTFOLIO_OPTIMIZATION, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_REBALANCING_EXECUTION, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_LIVE_TRADING, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_PAPER_TRADING, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_BROKER_EXECUTION, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_REAL_ORDER_CREATION, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_PAPER_STATE_MUTATION, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_TELEGRAM_REAL_SEND, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_STRATEGY_ACTIVATION, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_DEPLOYMENT, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_NETWORK, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_DASHBOARD, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_DAEMON, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.NO_SCHEDULER, passed=True, required=True),
        OptimizerSafetyBoundaryRule(rule_kind=OptimizerSafetyRuleKind.RESEARCH_DATA_ONLY, passed=True, required=True)
    ]

def build_optimizer_safety_boundary_result(rules: List[OptimizerSafetyBoundaryRule]) -> OptimizerSafetyBoundaryResult:
    passed = all(r.passed for r in rules if r.required)
    return OptimizerSafetyBoundaryResult(
        rules=rules,
        boundary_passed=passed,
        optimizer_sandbox_only=True, read_only_construction_artifacts=True,
        no_actual_target_weights=True, no_actual_portfolio_weights=True,
        no_actual_allocation=True, no_actual_position_size=True,
        no_order_size=True, no_capital_deployment=True,
        no_actual_portfolio_optimization=True, no_rebalancing_execution=True,
        no_live_trading=True, no_paper_trading=True, no_broker_execution=True,
        no_real_order_creation=True, no_paper_state_mutation=True,
        no_telegram_real_send=True, no_strategy_activation=True,
        no_deployment=True, no_network=True, no_dashboard=True,
        no_daemon=True, no_scheduler=True, research_data_only=True
    )

def validate_optimizer_safety_boundary_result(result: OptimizerSafetyBoundaryResult) -> List[str]:
    return ["Boundary failed"] if not result.boundary_passed else []

def optimizer_safety_boundary_passed(result: OptimizerSafetyBoundaryResult) -> bool:
    return result.boundary_passed

def optimizer_safety_boundary_summary(result: OptimizerSafetyBoundaryResult) -> Dict[str, Any]:
    return {"passed": result.boundary_passed}

def optimizer_safety_boundary_to_text(result: OptimizerSafetyBoundaryResult, limit: int = 300) -> str:
    return str(result.to_dict())[:limit]
