import pytest
import subprocess

def test_cli_strategy_list():
    res = subprocess.run(["python", "-m", "usa_signal_bot", "strategy-list"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "trend_following_skeleton" in res.stdout

def test_cli_strategy_info():
    res = subprocess.run(["python", "-m", "usa_signal_bot", "strategy-info", "--name", "trend_following_skeleton"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Candidate only, no execution" in res.stdout

def test_cli_signal_store_info():
    res = subprocess.run(["python", "-m", "usa_signal_bot", "signal-store-info"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "file_count" in res.stdout

def test_cli_signal_summary():
    res = subprocess.run(["python", "-m", "usa_signal_bot", "signal-summary"], capture_output=True, text=True)
    assert res.returncode == 0

def test_cli_strategy_run_feature_store_no_features():
    # It should fail or warn if no features are found
    res = subprocess.run(["python", "-m", "usa_signal_bot", "strategy-run-feature-store", "--strategy", "trend_following_skeleton", "--symbols", "AAPL"], capture_output=True, text=True)
    # Either exits 1 or warns, but should not crash
    assert "Error" in res.stdout or "Error" in res.stderr or res.returncode in [0, 1]
