import pandas as pd
import numpy as np
from usa_signal_bot.feature_engine.core_indicators.rolling_window_engine import (
    rolling_mean, rolling_std, rolling_sum, exponential_moving_average, weighted_moving_average, validate_rolling_window
)

def test_validate_rolling_window():
    assert validate_rolling_window(5) == []
    assert validate_rolling_window(0) != []

def test_rolling_mean():
    s = pd.Series([1, 2, 3, 4, 5])
    rm = rolling_mean(s, 3)
    assert np.isnan(rm[0])
    assert rm[2] == 2.0
