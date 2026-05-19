import pytest
from usa_signal_bot.paper_shadow.simulation_context import (
    build_shadow_simulation_context_from_sandbox_payload,
    build_mock_shadow_simulation_context,
    validate_shadow_context_safety,
    shadow_context_summary,
    shadow_context_to_text
)

def test_simulation_context():
    payload = {
        "sandbox_id": "test_sandbox",
        "bundle_id": "test_bundle",
        "config": {"setting": "value"}
    }

    ctx = build_shadow_simulation_context_from_sandbox_payload(payload)
    assert ctx.source_sandbox_id == "test_sandbox"
    assert ctx.starting_equity_usd == 100000.0
    assert not ctx.allow_real_orders

    mock_ctx = build_mock_shadow_simulation_context()
    assert mock_ctx.starting_equity_usd == 100000.0

    errors = validate_shadow_context_safety(ctx)
    assert not errors

    ctx.allow_real_orders = True
    errors = validate_shadow_context_safety(ctx)
    assert "Context allows real orders" in errors

    summary = shadow_context_summary(mock_ctx)
    assert summary["starting_equity_usd"] == 100000.0

    text = shadow_context_to_text(mock_ctx)
    assert "Shadow Simulation Context" in text
