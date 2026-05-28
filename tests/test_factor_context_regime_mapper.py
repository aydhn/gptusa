import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.factor_context_regime_mapper import (
    map_factor_context_to_regime_features
)

def test_map_factor_context_to_regime_features():
    df = pd.DataFrame({
        "market_volatility_context_20": [0.01, 0.02]
    })
    out_df = map_factor_context_to_regime_features(df)
    assert "regime_volatility_state_feature" in out_df.columns
