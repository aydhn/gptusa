import pytest
import pandas as pd
from usa_signal_bot.regime_classification.feature_engineering.market_state_metrics_engine import (
    add_market_state_metrics
)

def test_add_market_state_metrics():
    df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "close": [150.0, 152.0, 151.0],
        "volume": [1000, 1100, 1050]
    })

    out_df, results = add_market_state_metrics(df)
    assert "market_return_context_20" in out_df.columns
    assert len(results) > 0
