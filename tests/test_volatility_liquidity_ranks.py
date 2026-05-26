import pytest
import pandas as pd
from usa_signal_bot.feature_engine.advanced_features.volatility_liquidity_ranks import add_volatility_liquidity_rank_features

def test_ranks():
    t1 = pd.DataFrame({"timestamp": ["1", "2"], "realized_vol_20": [0.1, 0.2], "volume": [100, 200]})
    t2 = pd.DataFrame({"timestamp": ["1", "2"], "realized_vol_20": [0.2, 0.1], "volume": [200, 100]})
    res = add_volatility_liquidity_rank_features({"A": t1, "B": t2})
    assert "cs_realized_vol_20_rank" in res["A"].columns
