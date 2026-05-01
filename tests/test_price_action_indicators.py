import pytest
import pandas as pd

from usa_signal_bot.features.price_action_indicators import (
    CandleFeaturesIndicator, WickFeaturesIndicator, CloseLocationValueIndicator,
    GapFeaturesIndicator, BreakoutDistanceIndicator, BreakdownDistanceIndicator,
    InsideOutsideBarIndicator, SwingPointIndicator, MarketStructureIndicator,
    RangeExpansionIndicator
)
from usa_signal_bot.core.exceptions import IndicatorParameterError, FeatureComputationError

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "open": [10.0, 11.0, 10.5, 12.0, 11.0],
        "high": [11.0, 12.0, 11.0, 13.0, 12.0],
        "low": [9.0, 10.0, 10.0, 11.0, 10.0],
        "close": [10.5, 11.5, 10.5, 12.5, 11.5]
    })

def test_candle_features_indicator(sample_data):
    ind = CandleFeaturesIndicator()
    out = ind.compute(sample_data)
    assert "candle_body" in out.columns
    assert "candle_direction_code" in out.columns
    assert out["candle_direction_code"].iloc[0] == 1 # 10.5 > 10.0 -> bullish
    assert out["candle_direction_code"].iloc[2] == 0 # 10.5 == 10.5 -> doji

def test_wick_features_indicator(sample_data):
    ind = WickFeaturesIndicator()
    out = ind.compute(sample_data)
    assert "upper_wick" in out.columns
    assert "wick_imbalance" in out.columns

def test_close_location_value_indicator(sample_data):
    ind = CloseLocationValueIndicator()
    out = ind.compute(sample_data)
    assert "close_location_value" in out.columns

def test_gap_features_indicator(sample_data):
    ind = GapFeaturesIndicator()
    out = ind.compute(sample_data)
    assert "gap_pct" in out.columns
    assert "gap_direction_code" in out.columns

def test_breakout_distance_indicator(sample_data):
    ind = BreakoutDistanceIndicator()
    out = ind.compute(sample_data, {"window": 2})
    assert "breakout_distance_pct_2" in out.columns
    assert "rolling_high_prev_2" in out.columns

def test_breakdown_distance_indicator(sample_data):
    ind = BreakdownDistanceIndicator()
    out = ind.compute(sample_data, {"window": 2})
    assert "breakdown_distance_pct_2" in out.columns
    assert "rolling_low_prev_2" in out.columns

def test_inside_outside_bar_indicator(sample_data):
    ind = InsideOutsideBarIndicator()
    out = ind.compute(sample_data)
    assert "inside_bar" in out.columns
    assert "bar_pattern_code" in out.columns

def test_swing_point_indicator(sample_data):
    ind = SwingPointIndicator()
    out = ind.compute(sample_data, {"left_window": 1, "right_window": 1})
    assert "confirmed_swing_high_1_1" in out.columns
    assert "swing_point_code_1_1" in out.columns

def test_market_structure_indicator(sample_data):
    ind = MarketStructureIndicator()
    out = ind.compute(sample_data, {"swing_left": 1, "swing_right": 1})
    assert "higher_high" in out.columns
    assert "structure_state_code" in out.columns

def test_range_expansion_indicator(sample_data):
    ind = RangeExpansionIndicator()
    out = ind.compute(sample_data, {"window": 2})
    assert "range_expansion_2" in out.columns
    assert "range_contraction_2" in out.columns

def test_invalid_params(sample_data):
    ind = BreakoutDistanceIndicator()
    with pytest.raises(IndicatorParameterError):
        ind.compute(sample_data, {"window": 1}) # Min is 2

def test_missing_required_columns():
    ind = CandleFeaturesIndicator()
    df = pd.DataFrame({"open": [10.0]})
    with pytest.raises(FeatureComputationError):
        ind.compute(df)
