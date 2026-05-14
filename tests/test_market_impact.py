import pytest
from usa_signal_bot.core.enums import TransactionSide, MarketImpactStatus
from usa_signal_bot.transaction_costs.market_impact import estimate_market_impact

def test_market_impact_low():
    res = estimate_market_impact("SPY", TransactionSide.BUY, 1000, 10000000)
    assert res.status in [MarketImpactStatus.NEGLIGIBLE, MarketImpactStatus.LOW]

def test_market_impact_extreme():
    res = estimate_market_impact("SPY", TransactionSide.BUY, 1000000, 10000)
    assert res.status == MarketImpactStatus.EXTREME

def test_market_impact_insufficient():
    res = estimate_market_impact("SPY", TransactionSide.BUY, 1000, None)
    assert res.status == MarketImpactStatus.INSUFFICIENT_DATA
