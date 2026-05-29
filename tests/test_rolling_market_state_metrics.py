import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.rolling_market_state_metrics import (
    add_rolling_market_state_metrics
)

def test_add_rolling_market_state_metrics():
    df = pd.DataFrame({
        "market_return_context_20": [0.01, 0.02, 0.01, -0.01]
    })
    out_df = add_rolling_market_state_metrics(df, windows=[2])
    assert "market_return_context_20_rolling_mean_2" in out_df.columns
