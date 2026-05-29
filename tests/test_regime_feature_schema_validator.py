import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.regime_feature_schema_validator import (
    validate_regime_feature_dataframe_schema
)

def test_validate_regime_feature_dataframe_schema_valid():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "regime_volatility_state_feature": [0.5]})
    errors = validate_regime_feature_dataframe_schema(df)
    assert len(errors) == 0

def test_validate_regime_feature_dataframe_schema_invalid():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "buy_signal": [1]})
    errors = validate_regime_feature_dataframe_schema(df)
    assert len(errors) > 0
