import pytest
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_validation import validate_no_unsafe_advanced_feature_fields

def test_validation():
    r = validate_no_unsafe_advanced_feature_fields({"activation_allowed": False})
    assert r.valid
    r2 = validate_no_unsafe_advanced_feature_fields({"activation_allowed": True})
    assert not r2.valid
