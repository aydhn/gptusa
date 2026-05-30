import pytest
from usa_signal_bot.regime_classification.validation.regime_context_validation_reporting import regime_context_validation_limitations_text

def test_limitations_text():
    text = regime_context_validation_limitations_text()
    assert "not strategy activation" in text
