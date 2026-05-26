import pytest
import pandas as pd
from usa_signal_bot.feature_engine.advanced_features.relative_strength_features import add_relative_strength_vs_benchmark

def test_rs():
    t1 = pd.DataFrame({"timestamp": ["1", "2"], "ret_1d": [0.01, 0.05]})
    t2 = pd.DataFrame({"timestamp": ["1", "2"], "ret_1d": [0.02, 0.01]})
    res = add_relative_strength_vs_benchmark({"A": t1, "SPY": t2}, benchmark_symbol="SPY", columns=["ret_1d"])
    assert "rs_ret_1d_vs_spy" in res["A"].columns
