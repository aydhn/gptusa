import pytest
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_output_safety_validator import advanced_feature_output_text_has_trade_or_execution_language

def test_safety_validator():
    assert not advanced_feature_output_text_has_trade_or_execution_language("this is a test")
    assert advanced_feature_output_text_has_trade_or_execution_language("emir gönderildi")
