import pytest
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_registry import build_advanced_feature_specs, validate_advanced_feature_registry

def test_registry():
    specs = build_advanced_feature_specs()
    assert len(specs) >= 20
    errors = validate_advanced_feature_registry(specs)
    assert len(errors) == 0
