import pytest
from usa_signal_bot.regime_map.volatility_confirmation import classify_volatility_map_regime, volatility_map_regime_to_text
from usa_signal_bot.core.enums import VolatilityMapRegime
import numpy as np

def test_volatility_confirmation_insufficient_data():
    rows = [{"date": "2023-01-01", "close": 10}]
    regime, ev = classify_volatility_map_regime(rows)
    assert regime == VolatilityMapRegime.INSUFFICIENT_DATA

def test_volatility_confirmation_normal():
    # Construct stable price action

    # High volatility in the past
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 8, "close": 10, "volume": 100} for i in range(1, 40)]
    # Low volatility recently
    rows += [{"date": f"2023-02-{i:02d}", "open": 10, "high": 10.1, "low": 9.9, "close": 10, "volume": 100} for i in range(1, 41)]


    regime, ev = classify_volatility_map_regime(rows)
    assert regime in [VolatilityMapRegime.COMPRESSED, VolatilityMapRegime.NORMAL]

def test_volatility_map_regime_to_text():
    text = volatility_map_regime_to_text(VolatilityMapRegime.HIGH, {"realized_volatility_annualized": 25.5})
    assert "HIGH" in text
    assert "25.5" in text
