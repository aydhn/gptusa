from usa_signal_bot.paper_controlled_planning.rehearsal_safety_guard import (
    collect_rehearsal_safety_flags_from_context, assert_rehearsal_safe
)
from usa_signal_bot.paper_controlled_planning.adjacent_rehearsal_context import build_mock_paper_adjacent_rehearsal_context
from usa_signal_bot.core.exceptions import GuardedPaperAdjacentRehearsalError
from usa_signal_bot.core.enums import ControlledPlanningSafetyFlag
import pytest

def test_safety_guard():
    ctx = build_mock_paper_adjacent_rehearsal_context()
    assert_rehearsal_safe(ctx)

    ctx.allow_active_paper = True
    flags = collect_rehearsal_safety_flags_from_context(ctx)
    assert ControlledPlanningSafetyFlag.ACTIVE_PAPER_ENABLE_RISK in flags
    with pytest.raises(GuardedPaperAdjacentRehearsalError):
        assert_rehearsal_safe(ctx)
