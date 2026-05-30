from usa_signal_bot.regime_classification.freeze_preparation.monitoring_validation_specs import (
    build_default_monitoring_validation_rules,
    validate_monitoring_validation_rules
)

def test_build_default_rules():
    rules = build_default_monitoring_validation_rules()
    assert len(rules) > 10

def test_validate_rules():
    rules = build_default_monitoring_validation_rules()
    errors = validate_monitoring_validation_rules(rules)
    assert len(errors) == 0
