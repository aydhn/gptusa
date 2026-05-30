import pytest
from usa_signal_bot.regime_classification.validation.compatibility_validation_specs import build_default_compatibility_validation_rules

def test_build_default_compatibility_validation_rules():
    rules = build_default_compatibility_validation_rules()
    assert len(rules) == 16
    assert all(r.passed is False for r in rules)
