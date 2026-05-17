import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.core.enums import SignalContributionStatus
from usa_signal_bot.attribution.signal_attribution import (
    signal_contribution_by_family, signal_contribution_by_strategy, signal_contribution_by_id, identify_detrimental_signals
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", signal_family="RSI", signal_id="RSI_1", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", signal_family="MACD", signal_id="MACD_1", net_pnl_usd=-10.0, gross_pnl_usd=10.0, total_cost_usd=20.0), # cost degraded
        AttributionTradeEvent(event_id="e3", symbol="GOOG", signal_family="MACD", signal_id="MACD_2", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=10.0), # detrimental
    ]

def test_signal_contribution_by_family():
    events = _get_mock_events()
    contribs = signal_contribution_by_family(events)
    assert len(contribs) == 2
    macd = [c for c in contribs if c.signal_family == "MACD"][0]
    assert macd.net_pnl_usd == -60.0

def test_signal_contribution_by_id():
    events = _get_mock_events()
    contribs = signal_contribution_by_id(events)
    assert len(contribs) == 3
    macd_1 = [c for c in contribs if c.signal_id == "MACD_1"][0]
    assert macd_1.status == SignalContributionStatus.COST_DEGRADED

def test_identify_detrimental_signals():
    events = _get_mock_events()
    contribs = signal_contribution_by_id(events)
    detrimental = identify_detrimental_signals(contribs)
    assert len(detrimental) == 2 # MACD_1 and MACD_2
