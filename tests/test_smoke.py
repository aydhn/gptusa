"""Smoke tests to verify basic project load and structure."""

import sys
import subprocess

def test_package_import():
    """Verify that the package can be imported."""
    import usa_signal_bot
    assert usa_signal_bot.__version__ == "0.1.0"

def test_runtime_init():
    """Verify that the runtime initializes correctly."""
    from usa_signal_bot.app.runtime import init_runtime
    config = init_runtime()
    assert config is not None
    assert config.get("project", {}).get("name") == "USA Signal Bot"

def test_cli_smoke_command():
    """Verify the smoke CLI command executes without error."""
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "smoke"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Smoke test completed successfully" in result.stdout
