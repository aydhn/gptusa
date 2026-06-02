import pytest
from usa_signal_bot.backtesting.slippage_model import build_default_slippage_model

def test_slippage_model():
    m = build_default_slippage_model()
    assert m.slippage_model_valid is True
