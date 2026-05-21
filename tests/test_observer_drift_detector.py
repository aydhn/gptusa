from usa_signal_bot.paper_observer.drift_detector import detect_observer_drift
from usa_signal_bot.paper_observer.signal_mirror import build_mock_signal_mirror_outputs
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context
from usa_signal_bot.core.enums import ObserverDriftType

def test_detect_observer_drift():
    context = build_mock_observer_runtime_context()
    outputs = build_mock_signal_mirror_outputs(context)

    paper_snapshot = {}
    drifts = detect_observer_drift(paper_snapshot, outputs)

    assert len(drifts) == 1
    assert drifts[0].drift_type == ObserverDriftType.SIGNAL_COUNT_DRIFT
    assert drifts[0].delta == 1
