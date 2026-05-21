from usa_signal_bot.paper_controlled_planning.eligibility_checker import (
    evaluate_controlled_planning_eligibility, planning_ticket_status_from_decision,
    controlled_planning_safety_flags_from_observation
)
from usa_signal_bot.core.enums import ControlledPlanningDecision, ControlledPlanningTicketStatus

def test_eligibility():
    p = {"candidate_id": "1", "exit_decision": "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING", "observation_score": 80.0}
    assert evaluate_controlled_planning_eligibility(p, 75.0) == ControlledPlanningDecision.CREATE_PLANNING_TICKET
    assert planning_ticket_status_from_decision(ControlledPlanningDecision.CREATE_PLANNING_TICKET) == ControlledPlanningTicketStatus.CREATED

    p_low = {"candidate_id": "1", "exit_decision": "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING", "observation_score": 60.0}
    assert evaluate_controlled_planning_eligibility(p_low, 75.0) == ControlledPlanningDecision.REQUEST_MORE_OBSERVATION

    p_block = {"exit_decision": "BLOCK"}
    assert evaluate_controlled_planning_eligibility(p_block, 75.0) == ControlledPlanningDecision.BLOCK
