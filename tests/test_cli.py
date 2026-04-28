import pytest
import subprocess
import sys

def run_cli_command(*args) -> subprocess.CompletedProcess:
    """Helper to run a CLI command and return the completed process."""
    return subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", *args],
        capture_output=True,
        text=True
    )

def test_cli_smoke_command():
    result = run_cli_command("smoke")
    assert result.returncode == 0
    assert "USA Signal Bot smoke check" in result.stdout
    assert "Status: OK" in result.stdout

def test_cli_validate_config_command():
    result = run_cli_command("validate-config")
    assert result.returncode == 0
    assert "Config validation: OK" in result.stdout

def test_cli_runtime_summary_command():
    result = run_cli_command("runtime-summary")
    assert result.returncode == 0
    assert "USA Signal Bot Runtime Summary" in result.stdout
    assert "local_paper_only" in result.stdout

def test_cli_check_env_command():
    result = run_cli_command("check-env")
    assert result.returncode == 0
    assert "Telegram Enabled: False" in result.stdout


def test_cli_storage_info():
    result = run_cli_command("storage-info")
    assert result.returncode == 0

def test_cli_storage_check():
    result = run_cli_command("storage-check")
    assert result.returncode == 0

def test_cli_storage_list():
    result = run_cli_command("storage-list")
    assert result.returncode == 0

def test_cli_storage_list_area():
    result = run_cli_command("storage-list", "--area", "cache")
    assert result.returncode == 0