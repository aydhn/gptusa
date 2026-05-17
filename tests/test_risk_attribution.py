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
