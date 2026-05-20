from usa_signal_bot.paper_shadow.simulation_context import (
    build_shadow_simulation_context_from_sandbox_payload,
    build_mock_shadow_simulation_context,
    validate_shadow_context_safety,
    shadow_context_summary,
    shadow_context_to_text
)
from usa_signal_bot.core.enums import ShadowRuntimeMode

def test_build_shadow_simulation_context_from_sandbox_payload():
    ctx = build_shadow_simulation_context_from_sandbox_payload({"sandbox_id": "s1"})
    assert ctx.source_sandbox_id == "s1"
    assert not ctx.allow_real_orders

def test_build_mock_shadow_simulation_context():
    ctx = build_mock_shadow_simulation_context()
    assert ctx.runtime_mode == ShadowRuntimeMode.MOCK_SHADOW
    assert not ctx.allow_real_orders

def test_validate_shadow_context_safety():
    ctx = build_mock_shadow_simulation_context()
    assert len(validate_shadow_context_safety(ctx)) == 0
    ctx.allow_real_orders = True
    assert len(validate_shadow_context_safety(ctx)) == 1

def test_shadow_context_summary():
    ctx = build_mock_shadow_simulation_context()
    s = shadow_context_summary(ctx)
    assert s["is_safe"]

def test_shadow_context_to_text():
    ctx = build_mock_shadow_simulation_context()
    assert "mode=MOCK_SHADOW" in shadow_context_to_text(ctx)
