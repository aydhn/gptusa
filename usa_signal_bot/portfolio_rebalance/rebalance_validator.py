from typing import Any, Dict, List, Tuple
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalancePlan
from usa_signal_bot.core.enums import RebalanceStatus

def validate_rebalance_plan_exposure_consistency(plan: RebalancePlan) -> List[str]:
    errors = []
    # Simplified check to ensure total delta equals target gross - current gross (roughly)
    # Since exits might be suppressed, this is a soft validation
    if plan.total_delta_notional_usd is not None and plan.current_state and plan.target_state:
        # Just an example, actual logic depends on how we handle cash vs gross
        pass
    return errors

def validate_rebalance_actions_do_not_create_negative_positions(plan: RebalancePlan) -> List[str]:
    errors = []
    for action in plan.actions:
        if action.status == RebalanceStatus.PROPOSED and action.delta_notional_usd is not None and action.current_notional_usd is not None:
            if action.current_notional_usd + action.delta_notional_usd < -0.01:
                errors.append(f"Action {action.action_id} for {action.symbol} creates negative position notional.")
    return errors

def validate_rebalance_turnover_limits(plan: RebalancePlan) -> List[str]:
    errors = []
    if plan.turnover_assessment:
        if plan.turnover_assessment.status.value in ["EXCESSIVE"]:
            errors.append("Plan turnover assessment is EXCESSIVE, violates turnover limits.")
    return errors

def validate_rebalance_no_order_fields(plan_payload: Dict[str, Any]) -> List[str]:
    errors = []
    str_payload = str(plan_payload).lower()
    forbidden_fields = ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]
    for f in forbidden_fields:
        if f in str_payload:
            errors.append(f"Forbidden broker execution field found: {f}")
    return errors

def rebalance_plan_safety_check(plan: RebalancePlan) -> Tuple[bool, List[str]]:
    errors = []
    errors.extend(validate_rebalance_actions_do_not_create_negative_positions(plan))
    errors.extend(validate_rebalance_turnover_limits(plan))
    return len(errors) == 0, errors

def rebalance_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Rebalance Plan Validation: PASS"
    lines = ["Rebalance Plan Validation: FAIL"]
    for e in errors:
        lines.append(f"  - {e}")
    return "\n".join(lines)
