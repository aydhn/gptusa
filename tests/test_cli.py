import pytest
import subprocess
import sys

def run_cmd(cmd: list) -> int:
    try:
        res = subprocess.run([sys.executable, "-m", "usa_signal_bot"] + cmd, capture_output=True, text=True)
        return res.returncode
    except Exception:
        return 1

def test_cli_quality_commands():
    assert run_cmd(["quality-info"]) == 0
    assert run_cmd(["quality-artifacts"]) == 0
    # No writing so we don't pollute data directory in tests too much, but it shouldn't crash
    assert run_cmd(["quality-scorecard"]) == 0
    assert run_cmd(["readiness-gate", "--scope", "full_local_stack"]) == 0
    assert run_cmd(["acceptance-evaluate", "--scope", "full_local_stack"]) == 0
    assert run_cmd(["acceptance-summary"]) == 0
    assert run_cmd(["acceptance-latest"]) == 0
    assert run_cmd(["acceptance-validate"]) == 0
    assert run_cmd(["quality-notification-preview"]) == 0
    assert run_cmd(["quality-notification-dispatch-dry-run"]) == 0

def test_cli_existing_commands():
    # Make sure smoke is not broken
    assert run_cmd(["smoke"]) == 0
    assert run_cmd(["health"]) == 0
