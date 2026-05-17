import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.attribution_reporting import (
    attribution_trade_event_to_text, attribution_limitations_text
)

def test_attribution_trade_event_to_text():
    event = AttributionTradeEvent(event_id="e1", symbol="AAPL", side="BUY", net_pnl_usd=100.0, strategy_name="Trend")
    text = attribution_trade_event_to_text(event)
    assert "AAPL" in text
    assert "BUY" in text
    assert "$100.00" in text
    assert "Trend" in text

def test_attribution_limitations_text():
    text = attribution_limitations_text()
    assert "ATTRIBUTION LIMITATIONS" in text
    assert "NOT represent real broker performance" in text
    assert "NOT investment advice" in text
