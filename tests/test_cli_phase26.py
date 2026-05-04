import pytest
import subprocess
import sys

def test_backtest_cost_info_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "backtest-cost-info"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_backtest_trade_ledger_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "backtest-trade-ledger", "--latest"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_backtest_advanced_metrics_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "backtest-advanced-metrics", "--latest"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_backtest_cost_summary_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "backtest-cost-summary", "--latest"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
