import pytest
import pandas as pd

from usa_signal_bot.features.volume_indicators import (
    OBVIndicator, VWAPIndicator, RollingVWAPIndicator,
    MFIIndicator, CMFIndicator, AccumulationDistributionIndicator,
    VolumeAverageIndicator, RelativeVolumeIndicator, VolumeChangeIndicator,
    VolumeROCIndicator, DollarVolumeIndicator, VolumeTrendStrengthIndicator
)
from usa_signal_bot.core.exceptions import FeatureComputationError, IndicatorParameterError

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "timestamp": pd.date_range("2023-01-01", periods=10),
        "symbol": ["AAPL"] * 10,
        "timeframe": ["1d"] * 10,
        "open": [10.0] * 10,
        "high": [12.0] * 10,
        "low": [9.0] * 10,
        "close": [11.0] * 10,
        "volume": [1000] * 10
    })

def test_obv_indicator(sample_df):
    ind = OBVIndicator()
    res = ind.compute(sample_df)
    assert "obv" in res.columns

def test_vwap_indicator(sample_df):
    ind = VWAPIndicator()
    res = ind.compute(sample_df)
    assert "vwap" in res.columns

def test_rolling_vwap_indicator(sample_df):
    ind = RollingVWAPIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "rolling_vwap_5" in res.columns

def test_mfi_indicator(sample_df):
    ind = MFIIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "mfi_5" in res.columns

def test_cmf_indicator(sample_df):
    ind = CMFIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "cmf_5" in res.columns

def test_adl_indicator(sample_df):
    ind = AccumulationDistributionIndicator()
    res = ind.compute(sample_df)
    assert "adl" in res.columns

def test_volume_average_indicator(sample_df):
    ind = VolumeAverageIndicator()
    res = ind.compute(sample_df, {"window": 5, "method": "ema"})
    assert "volume_ema_5" in res.columns

def test_relative_volume_indicator(sample_df):
    ind = RelativeVolumeIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "relative_volume_5" in res.columns

def test_volume_change_indicator(sample_df):
    ind = VolumeChangeIndicator()
    res = ind.compute(sample_df, {"periods": 2})
    assert "volume_change_2" in res.columns

def test_volume_roc_indicator(sample_df):
    ind = VolumeROCIndicator()
    res = ind.compute(sample_df, {"window": 3})
    assert "volume_roc_3" in res.columns

def test_dollar_volume_indicator(sample_df):
    ind = DollarVolumeIndicator()
    res = ind.compute(sample_df, {"average_window": 5})
    assert "dollar_volume" in res.columns

def test_volume_trend_strength_indicator(sample_df):
    ind = VolumeTrendStrengthIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "volume_trend_strength_5" in res.columns

def test_missing_required_column():
    df = pd.DataFrame({"close": [10, 20]})
    ind = OBVIndicator()
    with pytest.raises(FeatureComputationError):
        ind.compute(df)
