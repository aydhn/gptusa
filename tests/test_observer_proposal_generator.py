from usa_signal_bot.paper_observer.proposal_generator import (
    build_mock_observer_proposals,
    validate_observer_proposals_safe
)
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context

def test_build_mock_observer_proposals():
    context = build_mock_observer_runtime_context()
    outputs = build_mock_observer_proposals(context)

    assert len(outputs) == 1
    out = outputs[0]
    assert out.is_real_order is False
    assert out.sends_to_broker is False

    errors = validate_observer_proposals_safe(outputs)
    assert len(errors) == 0
