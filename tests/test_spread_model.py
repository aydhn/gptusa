import pytest
from usa_signal_bot.backtesting.spread_model import build_default_spread_model

def test_spread_model():
    m = build_default_spread_model()
    assert m.spread_model_valid is True
