import pytest
from usa_signal_bot.app.cli import phase132_regime_context_validation_info

def test_phase132_cli_info(capsys):
    phase132_regime_context_validation_info(None)
    captured = capsys.readouterr()
    assert "Phase 132 is active" in captured.out
    assert "NOT strategy activation" in captured.out
