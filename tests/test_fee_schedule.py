import pytest
from usa_signal_bot.transaction_costs.fee_schedule import (
    default_zero_commission_equity_fee_schedule,
    conservative_fee_schedule_proxy,
    fee_schedule_to_text
)

def test_default_zero_commission_schedule():
    sched = default_zero_commission_equity_fee_schedule()
    assert sched.commission_per_share == 0.0
    assert sched.min_commission_usd == 0.0
    assert sched.enabled is True

def test_conservative_fee_schedule():
    sched = conservative_fee_schedule_proxy()
    assert sched.commission_per_share > 0.0
    assert sched.min_commission_usd > 0.0

def test_fee_schedule_text():
    sched = conservative_fee_schedule_proxy()
    text = fee_schedule_to_text(sched)
    assert "Conservative Commission Proxy" in text
