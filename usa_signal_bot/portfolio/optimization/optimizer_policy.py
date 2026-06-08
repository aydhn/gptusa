from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerPolicy, OptimizerPolicyKind

def build_default_optimizer_policy() -> OptimizerPolicy:
    return OptimizerPolicy(
        policy_kind=OptimizerPolicyKind.CONTRACT_ONLY_OPTIMIZER_SANDBOX_POLICY,
        policy_name="default_sandbox_policy",
        max_sandbox_optimizer_weight=0.10,
        min_sandbox_optimizer_weight=0.0,
        max_group_sandbox_optimizer_weight=0.40,
        max_turnover_sandbox=0.25,
        max_risk_budget_usage=0.30,
        score_objective_weight=0.25,
        concentration_objective_weight=0.20,
        risk_budget_objective_weight=0.20,
        robustness_objective_weight=0.20,
        turnover_objective_weight=0.15,
        deterministic=True,
        policy_valid=True,
        research_data_only=True,
        optimizer_sandbox_only=True
    )

def build_conservative_optimizer_policy() -> OptimizerPolicy:
    p = build_default_optimizer_policy()
    p.policy_kind = OptimizerPolicyKind.CONSERVATIVE_OPTIMIZER_SANDBOX_POLICY
    p.max_sandbox_optimizer_weight = 0.05
    p.max_group_sandbox_optimizer_weight = 0.20
    return p

def build_risk_budget_first_optimizer_policy() -> OptimizerPolicy:
    p = build_default_optimizer_policy()
    p.policy_kind = OptimizerPolicyKind.RISK_BUDGET_FIRST_OPTIMIZER_SANDBOX_POLICY
    p.risk_budget_objective_weight = 0.50
    return p

def build_robustness_first_optimizer_policy() -> OptimizerPolicy:
    p = build_default_optimizer_policy()
    p.policy_kind = OptimizerPolicyKind.ROBUSTNESS_FIRST_OPTIMIZER_SANDBOX_POLICY
    p.robustness_objective_weight = 0.50
    return p

def build_low_concentration_optimizer_policy() -> OptimizerPolicy:
    p = build_default_optimizer_policy()
    p.policy_kind = OptimizerPolicyKind.LOW_CONCENTRATION_OPTIMIZER_SANDBOX_POLICY
    p.concentration_objective_weight = 0.50
    return p

def validate_optimizer_policy(policy: OptimizerPolicy) -> List[str]:
    errs = []
    if policy.actual_target_weights_allowed: errs.append("actual_target_weights_allowed is True")
    if policy.actual_allocation_allowed: errs.append("actual_allocation_allowed is True")
    if policy.capital_deployment_allowed: errs.append("capital_deployment_allowed is True")
    if policy.actual_portfolio_optimization_allowed: errs.append("actual_portfolio_optimization_allowed is True")
    if not policy.optimizer_sandbox_only: errs.append("optimizer_sandbox_only is False")
    return errs

def optimizer_policy_summary(policy: OptimizerPolicy) -> Dict[str, Any]:
    return {"kind": policy.policy_kind.value, "valid": policy.policy_valid}

def optimizer_policy_to_text(policy: OptimizerPolicy, limit: int = 300) -> str:
    return str(policy.to_dict())[:limit]
