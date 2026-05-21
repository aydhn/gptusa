from usa_signal_bot.paper_controlled_planning.paper_quarantine_adapter import quarantine_supports_controlled_planning, attach_controlled_planning_metadata_to_quarantine_payload
from usa_signal_bot.paper_controlled_planning.planning_report import build_controlled_planning_review
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket

def test_quarantine_adapter():
    payload = {"candidate_id": "c1", "status": "EXIT_ELIGIBLE"}
    supports, _ = quarantine_supports_controlled_planning(payload)
    assert supports

    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    rev = build_controlled_planning_review(t)
    out = attach_controlled_planning_metadata_to_quarantine_payload(payload, rev)
    assert "planning_ticket_id" in out
