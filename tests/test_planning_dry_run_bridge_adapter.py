from usa_signal_bot.paper_controlled_planning.dry_run_bridge_adapter import adjacent_rehearsal_context_from_dry_run_review, attach_planning_hint_to_dry_run_payload
from usa_signal_bot.paper_controlled_planning.planning_report import build_controlled_planning_review
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket

def test_bridge_adapter():
    payload = {"candidate_id": "c1"}
    ctx = adjacent_rehearsal_context_from_dry_run_review(payload)
    assert ctx.candidate_id == "c1"

    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    rev = build_controlled_planning_review(t)
    out = attach_planning_hint_to_dry_run_payload(payload, rev)
    assert "controlled_planning_hint" in out
