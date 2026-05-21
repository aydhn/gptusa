from usa_signal_bot.paper_observer.runtime_safety_validator import validate_observer_runtime_safety
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment
from usa_signal_bot.paper_observer.observer_runtime_context import build_observer_runtime_context
from usa_signal_bot.core.enums import ObserverSafetyFlag

def test_validate_observer_runtime_safety():
    enrollment = build_observer_enrollment("cand_1", "t_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    context = build_observer_runtime_context(enrollment)

    errors = validate_observer_runtime_safety(enrollment, context)
    assert len(errors) == 0

def test_validate_observer_runtime_safety_errors():
    enrollment = build_observer_enrollment("cand_1", "t_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    context = build_observer_runtime_context(enrollment)
    context.allow_broker_orders = True

    errors = validate_observer_runtime_safety(enrollment, context)
    assert len(errors) == 1
    assert "BROKER_ORDER_RISK" in errors[0]
