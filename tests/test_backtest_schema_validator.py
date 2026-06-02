import pytest
from usa_signal_bot.backtesting.backtest_schema_validator import validate_backtest_column_names

def test_schema_validator():
    res = validate_backtest_column_names(["symbol", "open", "buy_signal"])
    assert len(res) == 1
    assert "Forbidden active trading columns detected" in res[0]
