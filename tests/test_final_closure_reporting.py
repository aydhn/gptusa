import pytest
from usa_signal_bot.feature_engine.final_closure.final_closure_report import build_final_closure_context
from usa_signal_bot.feature_engine.final_closure.final_closure_reporting import (
    final_closure_context_to_text, final_closure_limitations_text
)

def test_final_closure_reporting():
    ctx = build_final_closure_context()
    text = final_closure_context_to_text(ctx)
    assert "Context" in text

    limitations = final_closure_limitations_text()
    assert "LIMITATIONS" in limitations
    assert "Phase 125 is NOT an activation" in limitations
