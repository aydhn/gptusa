from usa_signal_bot.paper_observer.observer_report import (
    build_paper_observer_review,
    paper_observer_limitations_text
)
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context
from usa_signal_bot.paper_observer.parallel_monitor import run_read_only_parallel_monitor
from usa_signal_bot.core.enums import ObserverReportType

def test_build_paper_observer_review():
    enrollment = build_observer_enrollment("cand_1", "ticket_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    context = build_mock_observer_runtime_context()
    session = run_read_only_parallel_monitor(context)

    review = build_paper_observer_review(enrollment, session)
    assert review.report_type == ObserverReportType.FULL_OBSERVER_REVIEW
    assert len(review.enrollments) == 1
    assert len(review.sessions) == 1
    assert len(review.audit_entries) == 2

def test_paper_observer_limitations_text():
    text = paper_observer_limitations_text()
    assert "No broker" in text
    assert "NOT INVESTMENT ADVICE" in text
