from usa_signal_bot.paper_observer.parallel_monitor import (
    run_read_only_parallel_monitor,
    validate_parallel_monitor_safety
)
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context
from usa_signal_bot.core.enums import ObserverRuntimeStatus

def test_run_read_only_parallel_monitor():
    context = build_mock_observer_runtime_context()
    session = run_read_only_parallel_monitor(context)

    assert session.status == ObserverRuntimeStatus.COMPLETED
    assert len(session.outputs) > 0

    errors = validate_parallel_monitor_safety(session)
    assert len(errors) == 0
