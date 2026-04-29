import pytest
import subprocess
import sys

def test_universe_info_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-info"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "USA Signal Bot Universe Info" in result.stdout

def test_universe_validate_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-validate"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Passed        : YES" in result.stdout

def test_universe_list_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-list", "--limit", "2"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Universe Symbols" in result.stdout

def test_universe_build_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-build"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Snapshot written" in result.stdout

def test_universe_summary_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-summary"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Universe Summary" in result.stdout

def test_provider_info_command():
    # Since we use sys.exit, we'll just check if it runs without exception
    # directly using a subprocess or mock
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-info"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "USA Signal Bot Provider Info" in result.stdout
    assert "mock" in result.stdout

def test_provider_list_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-list"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Registered Providers" in result.stdout

def test_provider_check_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-check"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "All guard checks passed" in result.stdout

def test_provider_plan_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-plan", "--symbols", "AAPL,MSFT", "--timeframe", "1d"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Provider Fetch Plan" in result.stdout
    assert "Symbols: 2" in result.stdout

def test_provider_mock_fetch_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-mock-fetch", "--symbols", "AAPL", "--timeframe", "1d"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Mock Data Fetch Result" in result.stdout
    assert "fake data" in result.stdout
