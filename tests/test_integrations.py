from usa_signal_bot.quality.data_quality_evaluator import enrich_quality_scorecard_with_observer_dims
from usa_signal_bot.observability.metrics_collector import observer_metrics_collector
from usa_signal_bot.notifications.notification_adapters import notifications_from_paper_observer_review
from usa_signal_bot.paper_observer.observer_report import build_paper_observer_review
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context
from usa_signal_bot.paper_observer.parallel_monitor import run_read_only_parallel_monitor

def test_quality_evaluator():
    scorecard = {}
    enrich_quality_scorecard_with_observer_dims(scorecard, {"allow_active_paper": True})
    assert scorecard["locked_observer_runtime_safety_score"] == 0

def test_metrics_collector():
    enrollment = build_observer_enrollment("cand_1", "t1", "OK")
    context = build_mock_observer_runtime_context()
    session = run_read_only_parallel_monitor(context)
    review = build_paper_observer_review(enrollment, session)

    observer_metrics_collector.collect_from_observer_review(review)
    metrics = observer_metrics_collector.get_metrics()
    assert metrics["latest_observer_session_count"] > 0
    assert metrics["latest_observer_output_count"] > 0

def test_notification_adapters():
    enrollment = build_observer_enrollment("cand_1", "t1", "OK")
    context = build_mock_observer_runtime_context()
    session = run_read_only_parallel_monitor(context)
    review = build_paper_observer_review(enrollment, session)

    msgs = notifications_from_paper_observer_review(review)
    assert len(msgs) > 0

    msg_types = [m.type for m in msgs]
    assert "paper_observer_report" in msg_types
