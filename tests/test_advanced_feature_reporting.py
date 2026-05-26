import pytest
from usa_signal_bot.feature_engine.advanced_features.phase118_models import AdvancedFeatureSpec, AdvancedFeatureFamily, NormalizationMethod
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_reporting import advanced_feature_spec_to_text

def test_reporting():
    s = AdvancedFeatureSpec(
        "1", "1", "name", AdvancedFeatureFamily.ADVANCED_MOMENTUM, NormalizationMethod.NONE,
        [], [], {}, 0, 0, True, False, False, False, False, False, False, [], [], [], {}
    )
    assert "name" in advanced_feature_spec_to_text(s)
