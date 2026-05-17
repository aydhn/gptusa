import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.regime_attribution import (
    regime_performance_attribution, regime_cost_attribution, regime_drawdown_proxy
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", regime_label="BULL", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", regime_label="BEAR", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e3", symbol="GOOG", net_pnl_usd=20.0, gross_pnl_usd=25.0, total_cost_usd=5.0), # No regime
    ]

def test_regime_performance_attribution():
    events = _get_mock_events()
    contribs = regime_performance_attribution(events)
    assert len(contribs) == 3
    names = [c.name for c in contribs]
    assert "BULL" in names
    assert "BEAR" in names
    assert "UNKNOWN" in names

def test_regime_cost_attribution():
    events = _get_mock_events()
    contribs = regime_cost_attribution(events)
    assert len(contribs) == 3

def test_regime_drawdown_proxy():
    events = _get_mock_events()
    proxies = regime_drawdown_proxy(events)
    assert len(proxies) == 3
    # BEAR regime has net PnL -50 -> 50 DD
    bear = [p for p in proxies if p.name == "BEAR"][0]
    assert bear.drawdown_contribution_usd == 50.0
