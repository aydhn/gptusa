import pytest
from usa_signal_bot.feature_engine.factor_explainability.drift_interpretation import interpret_factor_drift_report

def test_interpret_factor_drift_report():
    res = interpret_factor_drift_report({})
    assert "metadata" in res.lower()
