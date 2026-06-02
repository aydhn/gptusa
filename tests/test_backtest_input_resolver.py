import pytest
from usa_signal_bot.backtesting.backtest_input_resolver import build_backtest_input_references

class DummyDF:
    def __init__(self, cols):
        self.columns = cols
    def __len__(self):
        return 1

def test_build_backtest_input_references():
    df = DummyDF(["symbol", "timestamp", "open", "high", "low", "close", "volume"])
    refs = build_backtest_input_references({"price_bars": {"kind": "PRICE_BAR_DATA"}}, {"price_bars": df})
    assert len(refs) == 1
    assert not refs[0].errors

def test_forbidden_columns():
    df = DummyDF(["symbol", "timestamp", "buy_signal"])
    refs = build_backtest_input_references({"price_bars": {"kind": "PRICE_BAR_DATA"}}, {"price_bars": df})
    assert len(refs) == 1
    assert "Forbidden columns detected" in str(refs[0].errors)
