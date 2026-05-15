import datetime
from usa_signal_bot.regime_map.momentum_confirmation import classify_momentum_regime
from usa_signal_bot.core.enums import MomentumRegime

def test_momentum_positive():
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100+i, "high": 100+i, "low": 100+i, "close": 100+i, "volume": 100} for i in range(1, 60)]
    reg, ev = classify_momentum_regime(rows)
    assert reg in [MomentumRegime.POSITIVE, MomentumRegime.STRONG_POSITIVE]

def test_momentum_negative():
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100-i, "high": 100-i, "low": 100-i, "close": 100-i, "volume": 100} for i in range(1, 60)]
    reg, ev = classify_momentum_regime(rows)
    assert reg in [MomentumRegime.NEGATIVE, MomentumRegime.STRONG_NEGATIVE]
