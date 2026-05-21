from usa_signal_bot.paper_controlled_planning.planning_validation import validate_no_live_execution_language_in_controlled_planning, validate_no_active_paper_language_in_controlled_planning
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket
from usa_signal_bot.paper_controlled_planning.planning_validation import validate_controlled_planning_ticket_report

def test_validation():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    rep = validate_controlled_planning_ticket_report(t)
    assert rep.valid

    bad_lang = validate_no_live_execution_language_in_controlled_planning("live approved")
    assert not bad_lang.valid

    bad_paper = validate_no_active_paper_language_in_controlled_planning("aktif et")
    assert not bad_paper.valid
