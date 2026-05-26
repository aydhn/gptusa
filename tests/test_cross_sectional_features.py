import pytest
import pandas as pd
from usa_signal_bot.feature_engine.advanced_features.cross_sectional_features import add_cross_sectional_rank_features

def test_cs_features():
    t1 = pd.DataFrame({"timestamp": ["1", "2"], "ret": [0.01, 0.05]})
    t2 = pd.DataFrame({"timestamp": ["1", "2"], "ret": [0.02, 0.01]})
    res = add_cross_sectional_rank_features({"A": t1, "B": t2}, ["ret"])
    assert "cs_ret_zscore" in res["A"].columns
    assert "cs_ret_percentile" in res["A"].columns
