import pytest
import pandas as pd
import numpy as np

from usa_signal_bot.features.volume_utils import (
    calculate_obv, calculate_vwap, calculate_rolling_vwap,
    calculate_money_flow_index, calculate_chaikin_money_flow,
    calculate_accumulation_distribution_line, calculate_volume_sma,
    calculate_volume_ema, calculate_relative_volume,
    calculate_volume_change, calculate_volume_roc,
    calculate_dollar_volume, calculate_average_dollar_volume,
    calculate_volume_trend_strength, validate_volume_window
)
from usa_signal_bot.core.exceptions import IndicatorParameterError

def test_calculate_obv():
    close = pd.Series([10.0, 11.0, 10.5, 12.0])
    volume = pd.Series([100, 200, 150, 300])
    obv = calculate_obv(close, volume)

    # Diff: [NaN, 1.0, -0.5, 1.5]
    # Direction: [0, 1, -1, 1]
    # Vol Adj: [0, 200, -150, 300]
    # Cumsum: [0, 200, 50, 350]
    assert obv.iloc[0] == 0
    assert obv.iloc[1] == 200
    assert obv.iloc[2] == 50
    assert obv.iloc[3] == 350

def test_calculate_vwap():
    high = pd.Series([10, 20])
    low = pd.Series([10, 20])
    close = pd.Series([10, 20])
    volume = pd.Series([100, 100])

    vwap = calculate_vwap(high, low, close, volume)
    assert vwap.iloc[0] == 10.0
    assert vwap.iloc[1] == 15.0

def test_calculate_rolling_vwap():
    high = pd.Series([10, 20, 30])
    low = pd.Series([10, 20, 30])
    close = pd.Series([10, 20, 30])
    volume = pd.Series([100, 100, 100])
    vwap = calculate_rolling_vwap(high, low, close, volume, window=2)
    assert vwap.iloc[0] == 10.0
    assert vwap.iloc[1] == 15.0
    assert vwap.iloc[2] == 25.0

def test_calculate_money_flow_index():
    high = pd.Series([10, 12, 14, 16])
    low = pd.Series([10, 12, 14, 16])
    close = pd.Series([10, 12, 14, 16])
    volume = pd.Series([100, 100, 100, 100])
    mfi = calculate_money_flow_index(high, low, close, volume, window=2)
    assert np.isclose(mfi.iloc[1], 100.0)

def test_calculate_chaikin_money_flow():
    high = pd.Series([10, 10])
    low = pd.Series([5, 5])
    close = pd.Series([7.5, 10])
    volume = pd.Series([100, 100])
    cmf = calculate_chaikin_money_flow(high, low, close, volume, window=2)
    assert cmf.iloc[0] == 0.0
    assert cmf.iloc[1] == 0.5

def test_calculate_accumulation_distribution_line():
    high = pd.Series([10])
    low = pd.Series([5])
    close = pd.Series([10])
    volume = pd.Series([100])
    adl = calculate_accumulation_distribution_line(high, low, close, volume)
    assert adl.iloc[0] == 100.0

def test_calculate_volume_sma_ema():
    vol = pd.Series([100, 200, 300])
    sma = calculate_volume_sma(vol, window=2)
    assert sma.iloc[0] == 100.0
    assert sma.iloc[1] == 150.0
    ema = calculate_volume_ema(vol, span=2)
    assert not np.isnan(ema.iloc[2])

def test_calculate_relative_volume():
    vol = pd.Series([100, 100, 200])
    rel = calculate_relative_volume(vol, window=2)
    assert np.isclose(rel.iloc[2], 1.33333333)

def test_calculate_volume_change_roc():
    vol = pd.Series([100, 150])
    chg = calculate_volume_change(vol, periods=1)
    assert chg.iloc[1] == 50.0
    roc = calculate_volume_roc(vol, window=1)
    assert roc.iloc[1] == 50.0

def test_calculate_dollar_volume():
    close = pd.Series([10, 20])
    vol = pd.Series([100, 50])
    dv = calculate_dollar_volume(close, vol)
    assert dv.iloc[0] == 1000
    adv = calculate_average_dollar_volume(close, vol, window=2)
    assert adv.iloc[1] == 1000

def test_calculate_volume_trend_strength():
    close = pd.Series([10, 11, 12.1])
    vol = pd.Series([100, 100, 100])
    vts = calculate_volume_trend_strength(vol, close, window=2)
    assert not np.isnan(vts.iloc[2])

def test_validate_volume_window():
    with pytest.raises(IndicatorParameterError):
        validate_volume_window(-1, "win")
    validate_volume_window(10, "win")
