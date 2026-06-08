from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import SizingPolicy, SizingPolicyKind

def build_default_sizing_policy() -> SizingPolicy:
    return SizingPolicy(
        policy_kind=SizingPolicyKind.CONTRACT_ONLY_RESEARCH_POLICY,
        policy_name="Default Phase 154 Research Policy",
        base_prototype_fraction=0.01,
        max_prototype_fraction=0.05,
        min_prototype_fraction=0.0,
        max_risk_budget_usage_fraction=0.25,
        deterministic=True,
        policy_valid=True,
        research_data_only=True,
        sizing_research_prototype_only=True,
        actual_position_sizing_allowed=False,
        target_weights_allowed=False,
        allocation_output_allowed=False,
        capital_deployment_allowed=False
    )

def build_conservative_sizing_policy() -> SizingPolicy:
    policy = build_default_sizing_policy()
    policy.policy_kind = SizingPolicyKind.CONSERVATIVE_RESEARCH_POLICY
    policy.policy_name = "Conservative Research Policy"
    policy.max_prototype_fraction = 0.02
    policy.max_risk_budget_usage_fraction = 0.10
    policy.volatility_penalty_enabled = True
    policy.drawdown_penalty_enabled = True
    return policy

def build_robustness_first_sizing_policy() -> SizingPolicy:
    policy = build_default_sizing_policy()
    policy.policy_kind = SizingPolicyKind.ROBUSTNESS_FIRST_RESEARCH_POLICY
    policy.policy_name = "Robustness First Research Policy"
    policy.robustness_penalty_enabled = True
    return policy

def validate_sizing_policy(policy: SizingPolicy) -> list[str]:
    errors = []
    if policy.actual_position_sizing_allowed:
        errors.append("actual_position_sizing_allowed must be False.")
    if policy.target_weights_allowed:
        errors.append("target_weights_allowed must be False.")
    if policy.allocation_output_allowed:
        errors.append("allocation_output_allowed must be False.")
    if policy.capital_deployment_allowed:
        errors.append("capital_deployment_allowed must be False.")

    if not (0.0 <= policy.min_prototype_fraction <= policy.base_prototype_fraction <= policy.max_prototype_fraction):
        errors.append("Invalid fraction bounds.")

    return errors

def sizing_policy_summary(policy: SizingPolicy) -> dict[str, Any]:
    return {"policy_kind": policy.policy_kind.value, "valid": len(validate_sizing_policy(policy)) == 0}

def sizing_policy_to_text(policy: SizingPolicy, limit: int = 300) -> str:
    return f"Policy: {policy.policy_name} ({policy.policy_kind.value})"[:limit]
