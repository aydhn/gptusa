import pytest
import subprocess
import sys

def run_cli_command(command: list[str]) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "usa_signal_bot"] + command
    return subprocess.run(cmd, capture_output=True, text=True)

def test_cli_active_universe_info():
    res = run_cli_command(["active-universe-info"])
    assert res.returncode == 0
    assert "Active Universe Resolution" in res.stdout

def test_cli_active_universe_symbols():
    res = run_cli_command(["active-universe-symbols", "--limit", "1"])
    assert res.returncode == 0
    assert "Active Universe Symbols" in res.stdout

def test_cli_active_universe_runs():
    res = run_cli_command(["active-universe-runs"])
    assert res.returncode == 0
    assert "Universe Data Runs" in res.stdout
