import pytest
from usa_signal_bot.regime_classification.feature_engineering.regime_feature_output_safety_validator import (
    validate_regime_feature_engineering_context_safety
)
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureEngineeringContext

def test_validate_regime_feature_engineering_context_safety_safe():
    ctx = RegimeFeatureEngineeringContext()
    errors = validate_regime_feature_engineering_context_safety(ctx)
    assert len(errors) == 0

def test_validate_regime_feature_engineering_context_safety_unsafe():
    ctx = RegimeFeatureEngineeringContext()
    ctx.produces_trade_signal = True
    errors = validate_regime_feature_engineering_context_safety(ctx)
    assert len(errors) > 0
