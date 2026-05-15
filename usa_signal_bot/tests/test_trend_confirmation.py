import pytest
from usa_signal_bot.regime_map.trend_confirmation import classify_trend_regime, trend_regime_to_text
from usa_signal_bot.core.enums import TrendRegime

def test_trend_confirmation_insufficient_data():
    rows = [{"date": "2023-01-01", "close": 10}]
    regime, ev = classify_trend_regime(rows, long_window=50)
    assert regime == TrendRegime.INSUFFICIENT_DATA

def test_trend_confirmation_uptrend():
    # Construct a perfect uptrend
    rows = [{"date": f"2023-01-{i:02d}", "close": 10 + i} for i in range(1, 60)]
    regime, ev = classify_trend_regime(rows, short_window=20, long_window=50)
    assert regime in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]

def test_trend_confirmation_downtrend():
    # Construct a perfect downtrend
    rows = [{"date": f"2023-01-{i:02d}", "close": 100 - i} for i in range(1, 60)]
    regime, ev = classify_trend_regime(rows, short_window=20, long_window=50)
    assert regime in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]

def test_trend_regime_to_text():
    text = trend_regime_to_text(TrendRegime.UPTREND, {"slope": 1.5})
    assert "UPTREND" in text
    assert "1.5" in text
