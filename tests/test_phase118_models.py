import pytest
from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    AdvancedFeatureSpec,
    AdvancedFeatureFamily,
    NormalizationMethod,
    validate_advanced_feature_spec,
    create_advanced_feature_spec_id
)
from usa_signal_bot.core.exceptions import AdvancedFeatureValidationError

def test_advanced_feature_spec_validation():
    # Valid
    spec = AdvancedFeatureSpec(
        spec_id=create_advanced_feature_spec_id(),
        created_at_utc="2023-01-01T00:00:00Z",
        feature_name="test_feat",
        family=AdvancedFeatureFamily.ADVANCED_MOMENTUM,
        normalization_method=NormalizationMethod.NONE,
        input_columns=["close"],
        output_columns=["out"],
        parameters={},
        min_required_rows=10,
        min_required_symbols=1,
        local_pandas_only=True,
        cross_sectional=False,
        requires_network=False,
        requires_paid_api=False,
        requires_scraping=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_advanced_feature_spec(spec)

    # Invalid
    spec.requires_network = True
    with pytest.raises(AdvancedFeatureValidationError):
        validate_advanced_feature_spec(spec)
