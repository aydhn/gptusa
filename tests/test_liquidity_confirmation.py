import datetime
from usa_signal_bot.regime_map.liquidity_confirmation import classify_liquidity_map_regime
from usa_signal_bot.core.enums import LiquidityMapRegime

def test_liquidity_deep():
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100, "high": 100, "low": 100, "close": 100, "volume": 10000000} for i in range(1, 90)]
    reg, ev = classify_liquidity_map_regime(rows)
    assert reg == LiquidityMapRegime.DEEP

def test_liquidity_illiquid():
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100, "high": 100, "low": 100, "close": 100, "volume": 1000} for i in range(1, 90)]
    reg, ev = classify_liquidity_map_regime(rows)
    assert reg in [LiquidityMapRegime.ILLIQUID, LiquidityMapRegime.THIN]
