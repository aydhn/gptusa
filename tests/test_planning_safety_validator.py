from usa_signal_bot.paper_controlled_planning.planning_safety_validator import validate_controlled_planning_safety, collect_controlled_planning_safety_flags
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket
from usa_signal_bot.paper_controlled_planning.approval_queue import build_final_approval_queue_item
from usa_signal_bot.core.enums import ControlledPlanningSafetyFlag

def test_safety_validator():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    q = build_final_approval_queue_item(t)
    errs = validate_controlled_planning_safety(t, None, q)
    assert not errs

    flags = collect_controlled_planning_safety_flags(t, None, q)
    assert ControlledPlanningSafetyFlag.MISSING_HUMAN_APPROVAL_NOTES in flags
