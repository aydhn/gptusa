import pytest
from usa_signal_bot.backtesting.backtest_engine import BacktestRunConfig, BacktestRunRequest, BacktestRunResult
from usa_signal_bot.backtesting.signal_adapter import default_signal_to_order_config
from usa_signal_bot.core.enums import BacktestExitMode
from usa_signal_bot.backtesting.backtest_validation import (
    validate_backtest_run_config, validate_backtest_run_request, assert_backtest_valid
)
from usa_signal_bot.core.exceptions import BacktestValidationError

def test_validate_config_valid():
    config = BacktestRunConfig(10000.0, 0.0, 0.0, default_signal_to_order_config(), BacktestExitMode.HOLD_N_BARS, 5, 10, 1000.0, True)
    report = validate_backtest_run_config(config)
    assert report.valid

def test_validate_config_invalid_cash():
    config = BacktestRunConfig(0.0, 0.0, 0.0, default_signal_to_order_config(), BacktestExitMode.HOLD_N_BARS, 5, 10, 1000.0, True)
    report = validate_backtest_run_config(config)
    assert not report.valid
    assert len(report.errors) == 1
    assert "starting_cash" in report.issues[0].field

def test_validate_request_empty_symbols():
    req = BacktestRunRequest("test", [], "1d", "yfinance", "file.jsonl")
    report = validate_backtest_run_request(req)
    assert not report.valid

def test_assert_valid_raises():
    req = BacktestRunRequest("test", [], "1d", "yfinance", "file.jsonl")
    report = validate_backtest_run_request(req)
    with pytest.raises(BacktestValidationError):
        assert_backtest_valid(report)
