from usa_signal_bot.paper_observer.signal_mirror import (
    build_mock_signal_mirror_outputs,
    validate_signal_mirror_outputs_safe
)
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context

def test_build_mock_signal_mirror_outputs():
    context = build_mock_observer_runtime_context()
    outputs = build_mock_signal_mirror_outputs(context)

    assert len(outputs) == 1
    out = outputs[0]
    assert out.is_real_order is False
    assert out.mutates_paper_state is False

    errors = validate_signal_mirror_outputs_safe(outputs)
    assert len(errors) == 0
