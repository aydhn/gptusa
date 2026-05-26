from usa_signal_bot.feature_engine.core_indicators.feature_output_safety_validator import (
    feature_output_text_has_trade_or_execution_language, validate_feature_dataframe_output_safety
)
import pandas as pd

def test_language_check():
    assert feature_output_text_has_trade_or_execution_language("buy signal generated")
    assert feature_output_text_has_trade_or_execution_language("emir gönderildi")
    assert not feature_output_text_has_trade_or_execution_language("macd computed successfully")

def test_dataframe_safety():
    df_safe = pd.DataFrame({"macd_signal_9": [1], "close": [1]})
    assert not validate_feature_dataframe_output_safety(df_safe)

    df_unsafe = pd.DataFrame({"buy_signal": [1], "close": [1]})
    errors = validate_feature_dataframe_output_safety(df_unsafe)
    assert len(errors) > 0
