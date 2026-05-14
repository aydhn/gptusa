import pytest
from usa_signal_bot.core.enums import TransactionSide
from usa_signal_bot.transaction_costs.fee_schedule import default_zero_commission_equity_fee_schedule, conservative_fee_schedule_proxy
from usa_signal_bot.transaction_costs.commission_estimator import estimate_total_fee_proxy_usd, fee_proxy_to_bps

def test_zero_commission():
    sched = default_zero_commission_equity_fee_schedule()
    res = estimate_total_fee_proxy_usd(TransactionSide.BUY, 10, 1000, sched)
    assert res["commission_usd"] == 0.0
    # No regulatory fee on buy
    assert res["regulatory_fee_usd"] == 0.0
    assert res["total_fee_usd"] == 0.0

def test_regulatory_fee_sell():
    sched = default_zero_commission_equity_fee_schedule()
    res = estimate_total_fee_proxy_usd(TransactionSide.SELL, 10, 1000, sched)
    assert res["commission_usd"] == 0.0
    assert res["regulatory_fee_usd"] > 0.0
    assert res["total_fee_usd"] > 0.0

def test_conservative_commission():
    sched = conservative_fee_schedule_proxy()
    res = estimate_total_fee_proxy_usd(TransactionSide.BUY, 10, 1000, sched)
    assert res["commission_usd"] >= sched.min_commission_usd

def test_fee_to_bps():
    bps = fee_proxy_to_bps(1.0, 1000)
    assert bps == 10.0
