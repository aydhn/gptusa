from usa_signal_bot.paper_observer.monitoring_analyzer import analyze_observer_runtime_session
from usa_signal_bot.paper_observer.parallel_monitor import run_read_only_parallel_monitor
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context

def test_analyze_observer_runtime_session():
    context = build_mock_observer_runtime_context()
    session = run_read_only_parallel_monitor(context)

    analysis = analyze_observer_runtime_session(session)
    assert analysis["session_id"] == session.session_id
    assert analysis["metrics"]["output_count"] == len(session.outputs)
