import pytest
from usa_signal_bot.feature_engine.factor_explainability.explainability_validation import validate_no_execution_language_in_explainability_text

def test_validate_no_execution_language_in_explainability_text():
    rep = validate_no_execution_language_in_explainability_text("buy")
    assert rep.valid is False
    rep2 = validate_no_execution_language_in_explainability_text("research")
    assert rep2.valid is True
