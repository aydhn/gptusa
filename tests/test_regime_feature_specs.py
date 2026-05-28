import pytest
from usa_signal_bot.regime_classification.feature_engineering.regime_feature_specs import (
    build_default_regime_feature_specs,
    validate_regime_feature_specs
)

def test_build_default_regime_feature_specs():
    specs = build_default_regime_feature_specs()
    assert len(specs) > 0
    errors = validate_regime_feature_specs(specs)
    assert len(errors) == 0
