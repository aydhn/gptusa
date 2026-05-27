import pytest
from usa_signal_bot.feature_engine.integration_freeze.freeze_preparation_safety_validator import validate_freeze_columns_safety

def test_validate_freeze_columns_safety():
    # MACD signal 9 is allowed
    errors = validate_freeze_columns_safety(["macd_signal_9", "volatility"])
    assert len(errors) == 0

    # buy is forbidden
    errors = validate_freeze_columns_safety(["buy_signal_strong"])
    assert len(errors) > 0
