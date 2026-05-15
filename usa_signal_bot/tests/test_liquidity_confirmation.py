import pytest
from usa_signal_bot.regime_map.liquidity_confirmation import classify_liquidity_map_regime, liquidity_map_regime_to_text
from usa_signal_bot.core.enums import LiquidityMapRegime

def test_liquidity_confirmation_insufficient_data():
    rows = [{"date": "2023-01-01", "close": 10, "volume": 100}]
    regime, ev = classify_liquidity_map_regime(rows)
    assert regime == LiquidityMapRegime.INSUFFICIENT_DATA

def test_liquidity_confirmation_deep():
    rows = [{"date": f"2023-01-{i:02d}", "close": 100, "volume": 1000000} for i in range(1, 80)]
    regime, ev = classify_liquidity_map_regime(rows)
    assert regime == LiquidityMapRegime.DEEP

def test_liquidity_map_regime_to_text():
    text = liquidity_map_regime_to_text(LiquidityMapRegime.THIN, {"avg_dollar_volume": 1000000})
    assert "THIN" in text
    assert "1,000,000" in text
