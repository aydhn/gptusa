import pytest
from usa_signal_bot.attribution.attribution_models import AttributionTradeEvent
from usa_signal_bot.attribution.exposure_attribution import exposure_contribution_by_symbol

def _get_mock_events():
    return [
        AttributionTradeEvent(event_id="e1", symbol="AAPL", notional_usd=1000.0),
        AttributionTradeEvent(event_id="e2", symbol="MSFT", notional_usd=3000.0),
    ]

def test_exposure_contribution_by_symbol():
    events = _get_mock_events()
    contribs = exposure_contribution_by_symbol(events)
    assert len(contribs) == 2
    msft = [c for c in contribs if c.name == "MSFT"][0]
    assert msft.concentration_contribution_pct == 75.0
