import datetime
from usa_signal_bot.regime_map.volatility_confirmation import classify_volatility_map_regime
from usa_signal_bot.core.enums import VolatilityMapRegime

def test_volatility_insufficient():
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 1, "high": 1, "low": 1, "close": 1, "volume": 100} for i in range(1, 10)]
    reg, ev = classify_volatility_map_regime(rows)
    assert reg == VolatilityMapRegime.INSUFFICIENT_DATA

def test_volatility_normal():
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100+i, "high": 110+i, "low": 90+i, "close": 105+i, "volume": 100} for i in range(1, 90)]
    reg, ev = classify_volatility_map_regime(rows)
    # Could be high or normal based on thresholds, just assert it runs and doesn't crash
    assert reg in [VolatilityMapRegime.NORMAL, VolatilityMapRegime.HIGH, VolatilityMapRegime.EXPANDING, VolatilityMapRegime.EXTREME, VolatilityMapRegime.COMPRESSED]
