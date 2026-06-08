from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    PortfolioConstructionPolicy,
    PortfolioConstructionPolicyKind,
    create_portfolio_construction_policy_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_default_portfolio_construction_policy() -> PortfolioConstructionPolicy:
    return PortfolioConstructionPolicy(
        policy_id=create_portfolio_construction_policy_id(),
        created_at_utc=_now_str(),
        policy_kind=PortfolioConstructionPolicyKind.CONTRACT_ONLY_SANDBOX_POLICY,
        policy_name="Default Phase155 Sandbox Policy",
        max_sandbox_weight_fraction=0.10,
        min_sandbox_weight_fraction=0.0,
        max_group_sandbox_weight_fraction=0.40,
        max_turnover_sandbox_fraction=0.25,
        risk_budget_weight=0.25,
        robustness_weight=0.25,
        sizing_weight=0.25,
        liquidity_weight=0.10,
        cost_weight=0.10,
        diversification_weight=0.05,
        deterministic=True,
        policy_valid=True,
        research_data_only=True,
        allocation_sandbox_only=True,
        actual_target_weights_allowed=False,
        actual_allocation_allowed=False,
        capital_deployment_allowed=False,
        portfolio_optimization_allowed=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"source": "default"}
    )

def build_conservative_portfolio_construction_policy() -> PortfolioConstructionPolicy:
    policy = build_default_portfolio_construction_policy()
    policy.policy_kind = PortfolioConstructionPolicyKind.CONSERVATIVE_SANDBOX_POLICY
    policy.policy_name = "Conservative Sandbox Policy"
    policy.max_sandbox_weight_fraction = 0.05
    policy.max_group_sandbox_weight_fraction = 0.20
    return policy

def build_risk_budget_first_portfolio_construction_policy() -> PortfolioConstructionPolicy:
    policy = build_default_portfolio_construction_policy()
    policy.policy_kind = PortfolioConstructionPolicyKind.RISK_BUDGET_FIRST_SANDBOX_POLICY
    policy.policy_name = "Risk Budget First Sandbox Policy"
    policy.risk_budget_weight = 0.50
    policy.robustness_weight = 0.10
    policy.sizing_weight = 0.10
    return policy

def build_robustness_first_portfolio_construction_policy() -> PortfolioConstructionPolicy:
    policy = build_default_portfolio_construction_policy()
    policy.policy_kind = PortfolioConstructionPolicyKind.ROBUSTNESS_FIRST_SANDBOX_POLICY
    policy.policy_name = "Robustness First Sandbox Policy"
    policy.robustness_weight = 0.50
    policy.risk_budget_weight = 0.10
    policy.sizing_weight = 0.10
    return policy

def validate_portfolio_construction_policy(policy: PortfolioConstructionPolicy) -> List[str]:
    errors = []

    if policy.max_sandbox_weight_fraction < policy.min_sandbox_weight_fraction:
        errors.append("Max sandbox weight cannot be less than min sandbox weight.")
    if policy.max_sandbox_weight_fraction > 1.0 or policy.max_sandbox_weight_fraction < 0.0:
        errors.append("Max sandbox weight must be between 0.0 and 1.0.")
    if policy.min_sandbox_weight_fraction > 1.0 or policy.min_sandbox_weight_fraction < 0.0:
        errors.append("Min sandbox weight must be between 0.0 and 1.0.")
    if policy.max_group_sandbox_weight_fraction > 1.0 or policy.max_group_sandbox_weight_fraction < 0.0:
        errors.append("Max group sandbox weight must be between 0.0 and 1.0.")
    if policy.max_turnover_sandbox_fraction < 0.0:
        errors.append("Max turnover sandbox fraction cannot be negative.")

    weight_sum = (
        policy.risk_budget_weight + policy.robustness_weight +
        policy.sizing_weight + policy.liquidity_weight +
        policy.cost_weight + policy.diversification_weight
    )
    if abs(weight_sum - 1.0) > 1e-5:
        errors.append(f"Composite weights sum to {weight_sum}, expected 1.0.")

    if policy.actual_target_weights_allowed:
        errors.append("actual_target_weights_allowed is True.")
        policy.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK)
    if policy.actual_allocation_allowed:
        errors.append("actual_allocation_allowed is True.")
        policy.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK)
    if policy.capital_deployment_allowed:
        errors.append("capital_deployment_allowed is True.")
        policy.risk_flags.append(PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK)
    if policy.portfolio_optimization_allowed:
        errors.append("portfolio_optimization_allowed is True.")
        policy.risk_flags.append(PortfolioConstructionRiskFlag.PORTFOLIO_OPTIMIZATION_RISK)

    return errors

def portfolio_construction_policy_summary(policy: PortfolioConstructionPolicy) -> Dict[str, Any]:
    return {
        "policy_id": policy.policy_id,
        "policy_name": policy.policy_name,
        "max_sandbox_weight": policy.max_sandbox_weight_fraction,
        "actual_target_weights_allowed": policy.actual_target_weights_allowed
    }

def portfolio_construction_policy_to_text(policy: PortfolioConstructionPolicy, limit: int = 300) -> str:
    summary = portfolio_construction_policy_summary(policy)
    return (
        f"Portfolio Construction Policy: {summary['policy_name']} ({summary['policy_id']})\n"
        f"Max Sandbox Weight: {summary['max_sandbox_weight']}\n"
        f"Actual Target Weights Allowed: {summary['actual_target_weights_allowed']}"
    )
