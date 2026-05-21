from usa_signal_bot.paper_observer.observer_runtime_context import (
    build_observer_runtime_context,
    validate_observer_context_safety
)
from usa_signal_bot.paper_observer.observer_enrollment import build_observer_enrollment

def test_build_observer_runtime_context():
    enrollment = build_observer_enrollment("cand_1", "t_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    context = build_observer_runtime_context(enrollment)

    assert context.locked is True
    assert context.allow_broker_orders is False
    assert context.allow_telegram_real_send is False

    errors = validate_observer_context_safety(context)
    assert len(errors) == 0

def test_validate_observer_context_safety_errors():
    enrollment = build_observer_enrollment("cand_1", "t_1", "APPROVED_FOR_NEXT_NON_EXECUTING_STAGE")
    context = build_observer_runtime_context(enrollment)

    context.allow_telegram_real_send = True
    context.allow_paper_orders = True

    errors = validate_observer_context_safety(context)
    assert len(errors) == 2
