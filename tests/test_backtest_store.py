import pytest
from pathlib import Path
from usa_signal_bot.backtesting.backtest_store import (
    backtest_store_dir, build_backtest_run_dir, backtest_store_summary
)
from usa_signal_bot.core.exceptions import BacktestStorageError

def test_backtest_store_dir(tmp_path):
    d = backtest_store_dir(tmp_path)
    assert d.exists()
    assert d.name == "backtests"

def test_build_run_dir(tmp_path):
    d = build_backtest_run_dir(tmp_path, "run1")
    assert d.exists()
    assert d.name == "run1"

def test_build_run_dir_invalid(tmp_path):
    with pytest.raises(BacktestStorageError):
        build_backtest_run_dir(tmp_path, "../run1")

def test_summary_empty(tmp_path):
    summary = backtest_store_summary(tmp_path)
    assert summary["total_runs"] == 0
