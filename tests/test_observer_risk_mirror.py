from usa_signal_bot.paper_observer.risk_mirror import (
    build_observer_risk_outputs,
    validate_risk_mirror_outputs_safe
)
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context
from usa_signal_bot.paper_observer.proposal_generator import build_mock_observer_proposals

def test_build_observer_risk_outputs():
    context = build_mock_observer_runtime_context()
    proposals = build_mock_observer_proposals(context)

    risk_outputs = build_observer_risk_outputs(context, proposals)
    assert len(risk_outputs) == 1

    out = risk_outputs[0]
    assert out.is_real_order is False

    errors = validate_risk_mirror_outputs_safe(risk_outputs)
    assert len(errors) == 0
