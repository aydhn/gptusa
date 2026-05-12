import pytest
import subprocess
import sys

def run_cli_command(cmd_args):
    return subprocess.run(
        [sys.executable, "-m", "usa_signal_bot"] + cmd_args,
        capture_output=True,
        text=True
    )

def check_cli_command_registered(cmd_name):
    res = run_cli_command([cmd_name, "--help"])
    # If the command is registered, argparse returns 0 for --help
    assert res.returncode == 0
    assert cmd_name in res.stdout

def test_cli_commands_registered():
    commands = [
        "profiling-info",
        "profile-noop",
        "profile-artifacts",
        "profile-lightweight",
        "profiling-summary",
        "profiling-latest",
        "profiling-validate",
        "budget-calibrate",
        "calibration-latest",
        "throttling-policies",
        "throttling-plan",
        "throttling-latest",
        "profiling-review",
        "profiling-audit-summary",
        "profiling-notification-preview",
        "profiling-notification-dispatch-dry-run"
    ]
    for cmd in commands:
        check_cli_command_registered(cmd)

def test_performance_info(monkeypatch, tmp_path):
    monkeypatch.setattr("sys.argv", ["usa_signal_bot", "performance-info"])
    from usa_signal_bot.app.cli import main
    assert main() == 0

def test_performance_baselines(monkeypatch, tmp_path):
    monkeypatch.setattr("sys.argv", ["usa_signal_bot", "performance-baselines"])
    from usa_signal_bot.app.cli import main
    assert main() == 0

def test_sla_thresholds(monkeypatch, tmp_path):
    monkeypatch.setattr("sys.argv", ["usa_signal_bot", "sla-thresholds"])
    from usa_signal_bot.app.cli import main
    assert main() == 0
