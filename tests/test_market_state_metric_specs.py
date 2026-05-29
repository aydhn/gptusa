import pytest
from usa_signal_bot.regime_classification.feature_engineering.market_state_metric_specs import (
    build_default_market_state_metric_specs,
    validate_market_state_metric_specs
)

def test_build_default_market_state_metric_specs():
    specs = build_default_market_state_metric_specs()
    assert len(specs) > 0
    errors = validate_market_state_metric_specs(specs)
    assert len(errors) == 0
