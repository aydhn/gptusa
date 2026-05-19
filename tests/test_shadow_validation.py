import pytest
from usa_signal_bot.paper_shadow.shadow_validation import (
    validate_shadow_context_report,
    shadow_validation_report_to_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def test_shadow_validation():
    ctx = build_mock_shadow_simulation_context()
    rep = validate_shadow_context_report(ctx)
    assert rep.valid

    ctx.allow_real_orders = True
    rep2 = validate_shadow_context_report(ctx)
    assert not rep2.valid

    text = shadow_validation_report_to_text(rep)
    assert "Shadow Validation Report" in text
