import pytest
from usa_signal_bot.feature_engine.factor_explainability.explainability_reporting import explainability_limitations_text

def test_explainability_limitations_text():
    assert "research purposes only" in explainability_limitations_text()
