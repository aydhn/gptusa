import pytest
from usa_signal_bot.backtesting.commission_model import build_default_commission_model

def test_commission_model():
    m = build_default_commission_model()
    assert m.commission_model_valid is True
