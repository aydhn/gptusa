from usa_signal_bot.paper_shadow.shadow_validation import (
    validate_no_live_execution_language_in_shadow, validate_no_broker_execution_fields_in_shadow,
    validate_no_paper_state_mutation_fields_in_shadow, validate_shadow_context_report
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context

def test_validate_no_live_execution_language_in_shadow():
    rep = validate_no_live_execution_language_in_shadow("this is a test")
    assert rep.valid
    rep = validate_no_live_execution_language_in_shadow("sent to broker")
    assert not rep.valid

def test_validate_no_broker_execution_fields_in_shadow():
    rep = validate_no_broker_execution_fields_in_shadow({"broker_order_id": "123"})
    assert not rep.valid
    rep = validate_no_broker_execution_fields_in_shadow({"shadow_order_id": "123"})
    assert rep.valid

def test_validate_shadow_context_report():
    ctx = build_mock_shadow_simulation_context()
    rep = validate_shadow_context_report(ctx)
    assert rep.valid

    ctx.allow_real_orders = True
    rep = validate_shadow_context_report(ctx)
    assert not rep.valid
