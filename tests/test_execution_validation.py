from usa_signal_bot.execution.execution_validation import (
    validate_no_live_execution_language_in_execution,
    validate_no_broker_execution_fields
)

def test_validation():
    # Should flag
    rep1 = validate_no_broker_execution_fields({"broker_order_id": "123"})
    assert rep1.valid == False

    rep2 = validate_no_live_execution_language_in_execution("live approved for trading")
    assert rep2.valid == False

    rep3 = validate_no_live_execution_language_in_execution("test passed")
    assert rep3.valid == True
