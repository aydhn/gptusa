import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.symbol_attribution import (
    top_symbol_contributors, worst_symbol_contributors, symbol_cost_drag_summary
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e3", symbol="GOOG", net_pnl_usd=200.0, gross_pnl_usd=210.0, total_cost_usd=10.0),
    ]

def test_top_symbol_contributors():
    events = _get_mock_events()
    top = top_symbol_contributors(events, top_n=2)
    assert len(top) == 2
    assert top[0].name == "GOOG"
    assert top[1].name == "AAPL"

def test_worst_symbol_contributors():
    events = _get_mock_events()
    worst = worst_symbol_contributors(events, top_n=2)
    assert len(worst) == 2
    assert worst[0].name == "MSFT"
    assert worst[1].name == "AAPL"

def test_symbol_cost_drag_summary():
    events = _get_mock_events()
    summary = symbol_cost_drag_summary(events)
    assert "AAPL" in summary
    assert "MSFT" in summary
    assert "GOOG" in summary
