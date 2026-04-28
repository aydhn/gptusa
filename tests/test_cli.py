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
