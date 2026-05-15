import pytest
from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine
from usa_signal_bot.core.enums import RegimeTimeframe, RegimeConfirmationStatus

def test_multi_timeframe_confirmation_insufficient():
    engine = MultiTimeframeRegimeConfirmationEngine([RegimeTimeframe.DAILY])
    conf = engine.confirm_symbol("SPY", [])
    assert conf.status == RegimeConfirmationStatus.INSUFFICIENT_DATA

def test_multi_timeframe_confirmation_confirmed():
    engine = MultiTimeframeRegimeConfirmationEngine([RegimeTimeframe.DAILY, RegimeTimeframe.WEEKLY])
    rows = [{"date": f"2023-01-{(i % 28) + 1:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 1000000} for i in range(1, 150)]
    conf = engine.confirm_symbol("SPY", rows)
    assert conf.status == RegimeConfirmationStatus.CONFIRMED
