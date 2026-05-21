from usa_signal_bot.paper_observer.session_registry import (
    register_observer_session,
    find_observer_session_by_id,
    latest_observer_session_for_candidate
)
from usa_signal_bot.paper_observer.parallel_monitor import run_read_only_parallel_monitor
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context

def test_observer_session_registry():
    registry = []
    context = build_mock_observer_runtime_context()
    context.candidate_id = "cand_abc"
    session = run_read_only_parallel_monitor(context)

    registry = register_observer_session(session, registry)
    assert len(registry) == 1

    registry = register_observer_session(session, registry)
    assert len(registry) == 1

    found = find_observer_session_by_id(registry, session.session_id)
    assert found == session

    latest = latest_observer_session_for_candidate(registry, "cand_abc")
    assert latest == session
