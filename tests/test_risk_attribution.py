import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.core.enums import AttributionDimension
from usa_signal_bot.attribution.risk_attribution import volatility_contribution_proxy

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=100.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", net_pnl_usd=-50.0),
        AttributionTradeEvent(event_id="e3", symbol="GOOG", net_pnl_usd=-50.0),
    ]

def test_volatility_contribution_proxy():
    events = _get_mock_events()
    contribs = volatility_contribution_proxy(events, AttributionDimension.SYMBOL)
    assert len(contribs) == 3
    # Total abs pnl = 200
    aapl = [c for c in contribs if c.name == "AAPL"][0]
    assert aapl.volatility_contribution_proxy == 50.0 # 100/200

def test_volatility_contribution_proxy_zero_pnl():
    events = [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=0.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", net_pnl_usd=None),
    ]
    contribs = volatility_contribution_proxy(events, AttributionDimension.SYMBOL)
    assert len(contribs) == 0

def test_volatility_contribution_proxy_strategy_dimension():
    events = [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", strategy_name="S1", net_pnl_usd=50.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", strategy_name="S1", net_pnl_usd=50.0),
        AttributionTradeEvent(event_id="e3", symbol="GOOG", strategy_name=None, net_pnl_usd=100.0),
    ]
    contribs = volatility_contribution_proxy(events, AttributionDimension.COST_COMPONENT)

    assert len(contribs) == 2
    s1 = [c for c in contribs if c.name == "S1"][0]
    unknown = [c for c in contribs if c.name == "UNKNOWN"][0]

    assert s1.volatility_contribution_proxy == 50.0  # 100/200
    assert unknown.volatility_contribution_proxy == 50.0  # 100/200
