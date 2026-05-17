import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.core.enums import AttributionDimension, ContributionDirection, AttributionQuality
from usa_signal_bot.attribution.pnl_attribution import (
    aggregate_pnl_by_dimension, calculate_win_rate, classify_contribution_direction, pnl_attribution_to_text
)

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", strategy_name="S1", sector="Tech", net_pnl_usd=100.0, gross_pnl_usd=110.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e2", symbol="AAPL", strategy_name="S2", sector="Tech", net_pnl_usd=-50.0, gross_pnl_usd=-40.0, total_cost_usd=10.0),
        AttributionTradeEvent(event_id="e3", symbol="MSFT", strategy_name="S1", sector="Tech", net_pnl_usd=200.0, gross_pnl_usd=220.0, total_cost_usd=20.0),
    ]

def test_aggregate_by_symbol():
    events = _get_mock_events()
    contribs = aggregate_pnl_by_dimension(events, AttributionDimension.SYMBOL)

    assert len(contribs) == 2
    assert contribs[0].name == "MSFT"  # Sorted by net_pnl desc (200 > 50)
    assert contribs[0].net_pnl_usd == 200.0
    assert contribs[1].name == "AAPL"
    assert contribs[1].net_pnl_usd == 50.0
    assert contribs[1].trade_count == 2

def test_aggregate_by_strategy():
    events = _get_mock_events()
    contribs = aggregate_pnl_by_dimension(events, AttributionDimension.STRATEGY)

    assert len(contribs) == 2
    assert contribs[0].name == "S1"
    assert contribs[0].net_pnl_usd == 300.0
    assert contribs[1].name == "S2"
    assert contribs[1].net_pnl_usd == -50.0

def test_aggregate_by_sector():
    events = _get_mock_events()
    contribs = aggregate_pnl_by_dimension(events, AttributionDimension.SECTOR)

    assert len(contribs) == 1
    assert contribs[0].name == "Tech"
    assert contribs[0].net_pnl_usd == 250.0

def test_win_rate():
    events = _get_mock_events()
    wr = calculate_win_rate(events)
    assert round(wr, 1) == 66.7

def test_classify_direction():
    assert classify_contribution_direction(100) == ContributionDirection.POSITIVE
    assert classify_contribution_direction(-100) == ContributionDirection.NEGATIVE
    assert classify_contribution_direction(0) == ContributionDirection.NEUTRAL
    assert classify_contribution_direction(None) == ContributionDirection.INSUFFICIENT_DATA

def test_pnl_attribution_to_text():
    events = _get_mock_events()
    contribs = aggregate_pnl_by_dimension(events, AttributionDimension.SYMBOL)
    text = pnl_attribution_to_text(contribs)
    assert "MSFT" in text
    assert "AAPL" in text
