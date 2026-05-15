import datetime
from usa_signal_bot.regime_map.trend_confirmation import classify_trend_regime
from usa_signal_bot.core.enums import TrendRegime

def test_uptrend_classification():
    # close > ma20 > ma50
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": i, "high": i, "low": i, "close": i, "volume": 100} for i in range(1, 60)]
    reg, ev = classify_trend_regime(rows)
    assert reg in [TrendRegime.UPTREND, TrendRegime.STRONG_UPTREND]

def test_downtrend_classification():
    # close < ma20 < ma50
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 60-i, "high": 60-i, "low": 60-i, "close": 60-i, "volume": 100} for i in range(1, 60)]
    reg, ev = classify_trend_regime(rows)
    assert reg in [TrendRegime.DOWNTREND, TrendRegime.STRONG_DOWNTREND]
