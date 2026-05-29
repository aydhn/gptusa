import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.regime_feature_table_builder import (
    build_regime_feature_table_for_symbol
)

def test_build_regime_feature_table_for_symbol():
    df = pd.DataFrame({
        "symbol": ["AAPL"],
        "timestamp": ["2023-01-01"],
        "close": [150.0],
        "volume": [1000]
    })
    out_df, result = build_regime_feature_table_for_symbol("AAPL", df)

    assert "market_return_context_20" in out_df.columns
    assert "regime_volatility_state_feature" in out_df.columns
    assert result.schema_valid is True
