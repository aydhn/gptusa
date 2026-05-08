from pathlib import Path
from usa_signal_bot.release.runbook_generator import generate_operator_runbook, runbook_to_markdown

def test_generate_operator_runbook():
    runbook = generate_operator_runbook()
    assert "OVERVIEW" in runbook.sections
    assert len(runbook.command_reference) > 0

    md = runbook_to_markdown(runbook)
    assert "CRITICAL SAFETY WARNINGS" in md
    assert "NOT a live trading bot" in md
