import pytest
from usa_signal_bot.regime_map.momentum_confirmation import classify_momentum_regime, momentum_regime_to_text
from usa_signal_bot.core.enums import MomentumRegime

def test_momentum_confirmation_insufficient_data():
    rows = [{"date": "2023-01-01", "close": 10}]
    regime, ev = classify_momentum_regime(rows)
    assert regime == MomentumRegime.INSUFFICIENT_DATA

def test_momentum_confirmation_positive():
    rows = [{"date": f"2023-01-{i:02d}", "close": 10 * (1.01 ** i)} for i in range(1, 50)]
    regime, ev = classify_momentum_regime(rows)
    assert regime in [MomentumRegime.POSITIVE, MomentumRegime.STRONG_POSITIVE]

def test_momentum_regime_to_text():
    text = momentum_regime_to_text(MomentumRegime.NEGATIVE, {"roc_pct": -5.0})
    assert "NEGATIVE" in text
    assert "-5.0" in text
