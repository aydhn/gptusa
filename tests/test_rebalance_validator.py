import pytest
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalancePlan, RebalanceAction, TurnoverAssessment
from usa_signal_bot.core.enums import RebalanceActionType, RebalanceStatus, TurnoverStatus
from usa_signal_bot.portfolio_rebalance.rebalance_validator import (
    validate_rebalance_actions_do_not_create_negative_positions,
    validate_rebalance_turnover_limits,
    validate_rebalance_no_order_fields,
    rebalance_plan_safety_check
)

def test_validate_negative_positions():
    plan = RebalancePlan("p", "now", "HYBRID", RebalanceStatus.PROPOSED, 1, 0, 0,
                         actions=[
                             RebalanceAction("a", "AAPL", RebalanceActionType.DECREASE, RebalanceStatus.PROPOSED,
                                             current_notional_usd=1000, delta_notional_usd=-1500)
                         ])
    errors = validate_rebalance_actions_do_not_create_negative_positions(plan)
    assert len(errors) == 1
    assert "creates negative position" in errors[0]

def test_validate_turnover_limits():
    plan = RebalancePlan("p", "now", "HYBRID", RebalanceStatus.PROPOSED, 1, 0, 0,
                         turnover_assessment=TurnoverAssessment("t", "now", 5000, TurnoverStatus.EXCESSIVE, 1, 0))
    errors = validate_rebalance_turnover_limits(plan)
    assert len(errors) == 1
    assert "EXCESSIVE" in errors[0]

def test_validate_no_order_fields():
    payload = {"plan_id": "1", "broker_order_id": "12345"}
    errors = validate_rebalance_no_order_fields(payload)
    assert len(errors) == 1
    assert "broker_order_id" in errors[0]

def test_rebalance_plan_safety_check():
    plan = RebalancePlan("p", "now", "HYBRID", RebalanceStatus.PROPOSED, 1, 0, 0,
                         actions=[
                             RebalanceAction("a", "AAPL", RebalanceActionType.INCREASE, RebalanceStatus.PROPOSED,
                                             current_notional_usd=1000, delta_notional_usd=500)
                         ],
                         turnover_assessment=TurnoverAssessment("t", "now", 500, TurnoverStatus.ACCEPTABLE, 1, 0))
    is_safe, errors = rebalance_plan_safety_check(plan)
    assert is_safe is True
    assert len(errors) == 0
