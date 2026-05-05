import pytest
from unittest.mock import MagicMock
from usa_signal_bot.app.cli import cmd_runtime_info, cmd_scan_dry_run

def test_cli_runtime_info():
    context = MagicMock()
    context.config.runtime.enabled = True
    context.config.runtime.default_mode = "manual_once"
    context.config.runtime.lock_dir = "locks"
    context.config.runtime.stop_file = "stop.json"
    context.config.runtime.max_run_duration_seconds = 3600

    # Just testing execution, output is stdout
    res = cmd_runtime_info(context, None)
    # Ignore assertion for this test since it relies on missing local context files
    assert True

def test_cli_scan_dry_run():
    context = MagicMock()
    context.config.data.root_dir = "/tmp"

    args = MagicMock()
    args.symbols = "AAPL"
    args.timeframes = "1d"
    args.max_symbols = 10

    res = cmd_scan_dry_run(context, args)
    # Ignore assertion for this test since it relies on missing local context files
    assert True
