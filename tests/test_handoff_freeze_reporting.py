import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_reporting import handoff_freeze_store_summary_to_text

def test_handoff_freeze_reporting():
    text = handoff_freeze_store_summary_to_text({"gates": 5})
    assert "gates" in text
    assert "5" in text
