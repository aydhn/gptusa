import pytest
from usa_signal_bot.feature_engine.advanced_features.cross_sectional_universe import build_cross_sectional_universe, validate_cross_sectional_universe

def test_universe():
    u = build_cross_sectional_universe()
    assert len(u.symbols) >= 2
    assert "SPY" in u.symbols
    assert len(validate_cross_sectional_universe(u)) == 0
