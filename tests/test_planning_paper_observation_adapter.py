from usa_signal_bot.paper_controlled_planning.paper_observation_adapter import planning_ticket_from_observation_review, attach_planning_metadata_to_observation_payload
from usa_signal_bot.paper_controlled_planning.planning_report import build_controlled_planning_review
from usa_signal_bot.core.enums import ControlledPlanningTicketStatus

def test_obs_adapter():
    payload = {"candidate_id": "c1", "exit_decision": "ELIGIBLE_FOR_CONTROLLED_PAPER_OBSERVATION_PLANNING", "observation_score": 85.0}
    t = planning_ticket_from_observation_review(payload)
    assert t.status == ControlledPlanningTicketStatus.CREATED

    rev = build_controlled_planning_review(t)
    out = attach_planning_metadata_to_observation_payload(payload, rev)
    assert out["planning_ticket_status"] == "CREATED"
