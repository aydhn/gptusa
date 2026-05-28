import pytest
from usa_signal_bot.regime_classification.feature_engineering.regime_feature_engineering_validation import (
    validate_regime_feature_engineering_context_report,
    RegimeFeatureEngineeringContext
)

def test_validate_regime_feature_engineering_context_report_valid():
    ctx = RegimeFeatureEngineeringContext()
    rep = validate_regime_feature_engineering_context_report(ctx)
    assert rep.valid is True

def test_validate_regime_feature_engineering_context_report_invalid():
    ctx = RegimeFeatureEngineeringContext(activation_allowed=True)
    rep = validate_regime_feature_engineering_context_report(ctx)
    assert rep.valid is False
