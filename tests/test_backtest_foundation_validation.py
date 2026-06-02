import pytest
from usa_signal_bot.backtesting.backtest_foundation_validation import validate_no_sensitive_data_in_backtest_payload

def test_sensitive_data():
    res = validate_no_sensitive_data_in_backtest_payload({"api_key": "123"})
    assert res.valid is False

    res2 = validate_no_sensitive_data_in_backtest_payload({"model": "abc"})
    assert res2.valid is True
