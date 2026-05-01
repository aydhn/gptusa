import pytest
import pandas as pd
import numpy as np

from usa_signal_bot.features.price_action_utils import (
    calculate_candle_body, calculate_candle_body_pct, calculate_upper_wick, calculate_lower_wick,
    calculate_full_range, calculate_close_location_value, calculate_gap_pct,
    calculate_breakout_distance_pct, calculate_breakdown_distance_pct,
    detect_inside_bar, detect_outside_bar, detect_swing_high, detect_swing_low,
    calculate_higher_high, calculate_lower_low, calculate_range_expansion, validate_price_action_window
)
from usa_signal_bot.core.exceptions import IndicatorParameterError

def test_calculate_candle_body():
    o = pd.Series([10.0, 10.0, 10.0])
    c = pd.Series([12.0, 8.0, 10.0])
    body = calculate_candle_body(o, c)
    assert body.tolist() == [2.0, 2.0, 0.0]

def test_calculate_candle_body_pct():
    o = pd.Series([10.0, 10.0, 10.0])
    c = pd.Series([12.0, 8.0, 10.0])
    body_pct = calculate_candle_body_pct(o, c)
    assert body_pct.tolist() == [0.2, 0.2, 0.0]

def test_calculate_upper_wick():
    o = pd.Series([10.0, 10.0, 10.0])
    h = pd.Series([13.0, 10.0, 11.0])
    c = pd.Series([12.0, 8.0, 10.0])
    wick = calculate_upper_wick(o, h, c)
    assert wick.tolist() == [1.0, 0.0, 1.0]

def test_calculate_lower_wick():
    o = pd.Series([10.0, 10.0, 10.0])
    l = pd.Series([9.0, 7.0, 10.0])
    c = pd.Series([12.0, 8.0, 10.0])
    wick = calculate_lower_wick(o, l, c)
    assert wick.tolist() == [1.0, 1.0, 0.0]

def test_calculate_full_range():
    h = pd.Series([13.0, 10.0, 11.0])
    l = pd.Series([9.0, 7.0, 10.0])
    r = calculate_full_range(h, l)
    assert r.tolist() == [4.0, 3.0, 1.0]

def test_calculate_close_location_value():
    h = pd.Series([13.0, 10.0, 10.0])
    l = pd.Series([9.0, 7.0, 10.0])
    c = pd.Series([12.0, 7.0, 10.0])
    clv = calculate_close_location_value(h, l, c)
    assert np.isclose(clv.iloc[0], 0.75)
    assert np.isclose(clv.iloc[1], 0.0)
    assert np.isnan(clv.iloc[2])

def test_calculate_gap_pct():
    o = pd.Series([10.0, 12.0, 8.0])
    prev_c = pd.Series([np.nan, 10.0, 10.0])
    gap = calculate_gap_pct(o, prev_c)
    assert np.isnan(gap.iloc[0])
    assert np.isclose(gap.iloc[1], 0.2)
    assert np.isclose(gap.iloc[2], -0.2)

def test_calculate_breakout_distance_pct():
    c = pd.Series([10.0, 11.0, 12.0, 13.0])
    h = pd.Series([11.0, 12.0, 12.5, 14.0])
    dist = calculate_breakout_distance_pct(c, h, window=2)
    assert np.isnan(dist.iloc[0])
    assert np.isnan(dist.iloc[1])
    assert np.isclose(dist.iloc[2], 0.0)
    assert np.isclose(dist.iloc[3], 0.04)

def test_calculate_breakdown_distance_pct():
    c = pd.Series([10.0, 9.0, 8.0, 7.0])
    l = pd.Series([9.0, 8.0, 7.5, 6.0])
    dist = calculate_breakdown_distance_pct(c, l, window=2)
    assert np.isnan(dist.iloc[0])
    assert np.isnan(dist.iloc[1])
    assert np.isclose(dist.iloc[2], 0.0)
    assert np.isclose(dist.iloc[3], 7.0/7.5 - 1)

def test_detect_inside_bar():
    h = pd.Series([12.0, 11.0, 13.0])
    l = pd.Series([8.0, 9.0, 7.0])
    ib = detect_inside_bar(h, l)
    assert ib.tolist() == [0, 1, 0]

def test_detect_outside_bar():
    h = pd.Series([12.0, 11.0, 13.0])
    l = pd.Series([8.0, 9.0, 7.0])
    ob = detect_outside_bar(h, l)
    assert ob.tolist() == [0, 0, 1]

def test_detect_swing_high():
    h = pd.Series([10.0, 11.0, 12.0, 11.0, 10.0])
    sh = detect_swing_high(h, left_window=1, right_window=1)
    assert sh.tolist() == [0, 0, 0, 1, 0]

def test_detect_swing_low():
    l = pd.Series([10.0, 9.0, 8.0, 9.0, 10.0])
    sl = detect_swing_low(l, left_window=1, right_window=1)
    assert sl.tolist() == [0, 0, 0, 1, 0]

def test_calculate_higher_high():
    h = pd.Series([10.0, 11.0, 12.0, 11.0, 10.0, 11.0, 13.0, 12.0, 11.0])
    sh = detect_swing_high(h, 1, 1)
    hh = calculate_higher_high(h, sh)
    assert hh.iloc[7] == 1

def test_calculate_lower_low():
    l = pd.Series([10.0, 9.0, 8.0, 9.0, 10.0, 9.0, 7.0, 8.0, 9.0])
    sl = detect_swing_low(l, 1, 1)
    ll = calculate_lower_low(l, sl)
    assert ll.iloc[7] == 1

def test_calculate_range_expansion():
    h = pd.Series([11.0, 11.0, 15.0])
    l = pd.Series([10.0, 10.0, 10.0])
    rex = calculate_range_expansion(h, l, window=2)
    assert np.isnan(rex.iloc[0])
    assert np.isnan(rex.iloc[1])
    assert rex.iloc[2] == 5.0

def test_validate_price_action_window():
    with pytest.raises(IndicatorParameterError):
        validate_price_action_window(-1, "test")
    with pytest.raises(IndicatorParameterError):
        validate_price_action_window(1001, "test")
    validate_price_action_window(10, "test")
