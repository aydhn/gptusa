import sys
import runpy
from unittest.mock import patch, MagicMock


def test_main_execution():
    """Test that __main__.py calls cli_main when run as main."""
    # To bypass missing dependencies like 'click' during tests collection or execution,
    # we mock it in sys.modules, but explicitly save and restore it to avoid polluting global state
    # (Memory constraint: "To bypass ImportError ... always restore original state")
    original_click = sys.modules.get("click")
    sys.modules["click"] = MagicMock()

    try:
        # We patch cli_main where it is defined so that when runpy imports it, it's mocked
        with patch("usa_signal_bot.app.cli.main") as mock_cli_main:
            with patch.object(sys, "argv", ["usa_signal_bot"]):
                runpy.run_module("usa_signal_bot.__main__", run_name="__main__")
            mock_cli_main.assert_called_once()
    finally:
        if original_click is None:
            del sys.modules["click"]
        else:
            sys.modules["click"] = original_click
