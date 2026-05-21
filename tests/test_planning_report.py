from usa_signal_bot.paper_controlled_planning.planning_report import build_controlled_planning_review
from usa_signal_bot.paper_controlled_planning.planning_ticket import build_controlled_planning_ticket
from usa_signal_bot.core.enums import ControlledPlanningReportType

def test_report():
    t = build_controlled_planning_ticket("c1", 80.0, "ELIGIBLE")
    rev = build_controlled_planning_review(t)
    assert rev.report_type == ControlledPlanningReportType.FULL_CONTROLLED_PLANNING_REVIEW
    assert len(rev.planning_tickets) == 1
