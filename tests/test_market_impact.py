import pytest
from usa_signal_bot.core.enums import TransactionSide, MarketImpactStatus
from usa_signal_bot.transaction_costs.market_impact import estimate_market_impact
from usa_signal_bot.transaction_costs.cost_models import TransactionCostInput

def test_market_impact_low():
    tc_in = TransactionCostInput(input_id="1", symbol="SPY", side=TransactionSide.BUY, quantity=None, notional_usd=1000, price=None, avg_dollar_volume=10000000, atr_pct=None, spread_proxy_bps=None, participation_rate_pct=None, liquidity_status=None)
    res = estimate_market_impact(tc_in)
    assert res.status in [MarketImpactStatus.NEGLIGIBLE, MarketImpactStatus.LOW]

def test_market_impact_extreme():
    tc_in = TransactionCostInput(input_id="2", symbol="SPY", side=TransactionSide.BUY, quantity=None, notional_usd=1000000, price=None, avg_dollar_volume=10000, atr_pct=None, spread_proxy_bps=None, participation_rate_pct=None, liquidity_status=None)
    res = estimate_market_impact(tc_in)
    assert res.status == MarketImpactStatus.EXTREME

def test_market_impact_insufficient():
    tc_in = TransactionCostInput(input_id="3", symbol="SPY", side=TransactionSide.BUY, quantity=None, notional_usd=1000, price=None, avg_dollar_volume=None, atr_pct=None, spread_proxy_bps=None, participation_rate_pct=None, liquidity_status=None)
    res = estimate_market_impact(tc_in)
    assert res.status == MarketImpactStatus.INSUFFICIENT_DATA
