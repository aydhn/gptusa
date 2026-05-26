import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from usa_signal_bot.feature_engine.advanced_features.multi_symbol_feature_table import build_multi_symbol_advanced_feature_tables

def test_build_multi_symbol_advanced_feature_tables(tmp_path):
    # Setup dummies
    df_aapl = pd.DataFrame({
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-03"] * 30,
        "close": np.random.rand(90) * 100,
        "high": np.random.rand(90) * 100 + 100,
        "low": np.random.rand(90) * 100,
        "volume": np.random.rand(90) * 1000
    })
    df_spy = pd.DataFrame({
        "timestamp": ["2023-01-01", "2023-01-02", "2023-01-03"] * 30,
        "close": np.random.rand(90) * 100,
        "high": np.random.rand(90) * 100 + 100,
        "low": np.random.rand(90) * 100,
        "volume": np.random.rand(90) * 1000
    })

    path_aapl = tmp_path / "aapl.csv"
    path_spy = tmp_path / "spy.csv"

    df_aapl.to_csv(path_aapl, index=False)
    df_spy.to_csv(path_spy, index=False)

    paths = {"AAPL": path_aapl, "SPY": path_spy}

    aligned, result = build_multi_symbol_advanced_feature_tables(paths)

    assert "AAPL" in aligned
    assert "SPY" in aligned

    # Check that advanced features exist
    assert "realized_vol_10" in aligned["AAPL"].columns
    assert "cs_ret_1d_percentile" in aligned["AAPL"].columns

    # Check result
    assert result.passed
    assert not result.produced_trade_signal
    assert not result.network_used
