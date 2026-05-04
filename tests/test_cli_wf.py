import subprocess
import sys
import json
from pathlib import Path

def run_cli(*args):
    cmd = [sys.executable, "-m", "usa_signal_bot"] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True)

def test_walk_forward_info():
    res = run_cli("walk-forward-info")
    assert res.returncode == 0
    assert "Walk-Forward Analysis Configuration" in res.stdout
    assert "OUT-OF-SAMPLE EVALUATION" in res.stdout

def test_walk_forward_plan():
    res = run_cli("walk-forward-plan", "--start", "2020-01-01", "--end", "2024-01-01", "--mode", "rolling", "--train-days", "100", "--test-days", "30", "--step-days", "30")
    assert res.returncode == 0
    assert "Walk-Forward Plan" in res.stdout
    assert "[win_001]" in res.stdout

def test_walk_forward_summary():
    res = run_cli("walk-forward-summary")
    assert res.returncode == 0
    assert "Walk-Forward Runs Summary" in res.stdout

def test_walk_forward_latest():
    res = run_cli("walk-forward-latest")
    assert res.returncode == 0

def test_walk_forward_validate():
    res = run_cli("walk-forward-validate", "--latest")
    assert res.returncode in (0, 1)

def test_walk_forward_run_signals(tmp_path):
    sig_file = tmp_path / "sigs.jsonl"
    with open(sig_file, "w") as f:
        f.write('{"signal_id":"sig_01","symbol":"AAPL","timeframe":"1d","timestamp_utc":"2020-01-02T00:00:00Z","action":"BUY","confidence":0.8,"feature_summary":{}}\n')

    res = run_cli("walk-forward-run-signals", "--signal-file", str(sig_file), "--symbols", "AAPL", "--start", "2020-01-01", "--end", "2020-03-01", "--max-windows", "1")
    assert res.returncode == 0
    assert "WALK-FORWARD RUN SUMMARY" in res.stdout
