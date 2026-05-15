import subprocess
import sys

def test_cli_help():
    res = subprocess.run([sys.executable, "-m", "usa_signal_bot", "help"], capture_output=True, text=True)
    assert res.returncode == 0

def test_cli_health():
    res = subprocess.run([sys.executable, "-m", "usa_signal_bot", "health"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "PASS" in res.stdout

def test_cli_regime_info():
    res = subprocess.run([sys.executable, "-m", "usa_signal_bot", "regime-map-info"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "NOT investment advice" in res.stdout

def test_cli_trend_confirmation():
    res = subprocess.run([sys.executable, "-m", "usa_signal_bot", "trend-confirmation", "--symbol", "SPY"], capture_output=True, text=True)
    assert res.returncode == 0
