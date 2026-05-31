import pytest
from usa_signal_bot.ml_research.foundation.forbidden_ml_output_validator import validate_no_forbidden_ml_output_fields

def test_forbidden_output_validator_clean():
    res = validate_no_forbidden_ml_output_fields(["feature1", "feature2"])
    assert len(res) == 0

def test_forbidden_output_validator_dirty():
    res = validate_no_forbidden_ml_output_fields(["buy_signal", "feature1"])
    assert len(res) == 1
