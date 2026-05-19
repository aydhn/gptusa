import pytest
from usa_signal_bot.paper_shadow.shadow_safety_guard import (
    collect_shadow_safety_flags_from_context,
    assert_shadow_session_safe,
    ShadowSafetyError,
    shadow_safety_guard_to_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def test_shadow_safety_guard():
    ctx = build_mock_shadow_simulation_context()
    flags = collect_shadow_safety_flags_from_context(ctx)
    assert not flags

    ctx.allow_real_orders = True
    flags = collect_shadow_safety_flags_from_context(ctx)
    assert len(flags) == 1

    with pytest.raises(ShadowSafetyError):
        assert_shadow_session_safe(ctx)

    text = shadow_safety_guard_to_text({"flag_count": 1})
    assert "Shadow Safety Guard Summary" in text
