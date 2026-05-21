from usa_signal_bot.paper_controlled_planning.planning_ticket import (
    build_controlled_planning_ticket, build_controlled_planning_ticket_from_observation,
    validate_planning_ticket_safety
)
from usa_signal_bot.core.enums import ControlledPlanningTicketStatus, ControlledPlanningSafetyFlag

def test_ticket_builder():
    t = build_controlled_planning_ticket("c1", 85.0, "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING")
    assert t.status == ControlledPlanningTicketStatus.CREATED
    assert t.candidate_id == "c1"
    assert t.allowed_for_active_paper is False
    assert not validate_planning_ticket_safety(t)

    t_obs = build_controlled_planning_ticket_from_observation({"candidate_id": "c2", "exit_decision": "BLOCK"})
    assert t_obs.status == ControlledPlanningTicketStatus.BLOCKED
    assert ControlledPlanningSafetyFlag.BLOCKED_EXIT_DECISION in t_obs.safety_flags
