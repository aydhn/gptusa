import pytest
import pandas as pd
from usa_signal_bot.features.volatility_indicators import (
    TrueRangeIndicator, ATRIndicator, NormalizedATRIndicator,
    BollingerBandsIndicator, BollingerBandwidthIndicator, BollingerPercentBIndicator,
    KeltnerChannelIndicator, DonchianChannelIndicator, RollingVolatilityIndicator,
    PriceRangeIndicator, VolatilityCompressionIndicator, VolatilityExpansionIndicator
)
from usa_signal_bot.core.exceptions import IndicatorParameterError, FeatureComputationError

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "open": [10.0, 10.5, 11.0, 10.8, 11.2, 11.5, 12.0, 11.8, 12.5, 13.0, 13.5, 13.8, 14.2, 14.5, 15.0],
        "high": [10.5, 11.0, 11.5, 11.2, 11.8, 12.0, 12.5, 12.2, 13.0, 13.5, 14.0, 14.2, 14.8, 15.0, 15.5],
        "low": [9.5, 10.0, 10.5, 10.2, 10.8, 11.0, 11.5, 11.2, 12.0, 12.5, 13.0, 13.2, 13.8, 14.0, 14.5],
        "close": [10.2, 10.8, 11.2, 10.5, 11.5, 11.8, 11.6, 12.3, 12.8, 13.2, 13.8, 13.5, 14.5, 14.8, 15.2],
        "symbol": ["AAPL"] * 15,
        "timeframe": ["1d"] * 15,
        "timestamp_utc": [d.isoformat() for d in pd.date_range("2023-01-01", periods=15)]
    })

def test_true_range_indicator(sample_df):
    ind = TrueRangeIndicator()
    res = ind.compute(sample_df)
    assert "true_range" in res.columns
    assert "symbol" in res.columns
    assert len(res) == len(sample_df)

def test_atr_indicator(sample_df):
    ind = ATRIndicator()
    res = ind.compute(sample_df, {"window": 5, "method": "sma"})
    assert "atr_5_sma" in res.columns

    with pytest.raises(IndicatorParameterError):
        ind.compute(sample_df, {"window": 0})

def test_normalized_atr_indicator(sample_df):
    ind = NormalizedATRIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "normalized_atr_5_wilder" in res.columns

def test_bollinger_bands_indicator(sample_df):
    ind = BollingerBandsIndicator()
    res = ind.compute(sample_df, {"window": 5, "num_std": 2.0})
    assert "close_bb_middle_5_2p0" in res.columns
    assert "close_bb_upper_5_2p0" in res.columns
    assert "close_bb_lower_5_2p0" in res.columns

def test_bollinger_bandwidth_indicator(sample_df):
    ind = BollingerBandwidthIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "close_bb_bandwidth_5_2p0" in res.columns

def test_bollinger_percent_b_indicator(sample_df):
    ind = BollingerPercentBIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "close_bb_percent_b_5_2p0" in res.columns

def test_keltner_channel_indicator(sample_df):
    ind = KeltnerChannelIndicator()
    res = ind.compute(sample_df, {"ema_window": 5, "atr_window": 5, "multiplier": 1.5})
    assert "keltner_middle_5_5_1p5" in res.columns
    assert "keltner_upper_5_5_1p5" in res.columns
    assert "keltner_lower_5_5_1p5" in res.columns

def test_donchian_channel_indicator(sample_df):
    ind = DonchianChannelIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "donchian_middle_5" in res.columns
    assert "donchian_upper_5" in res.columns
    assert "donchian_lower_5" in res.columns

def test_rolling_volatility_indicator(sample_df):
    ind = RollingVolatilityIndicator()
    res = ind.compute(sample_df, {"window": 5})
    assert "close_rolling_volatility_5" in res.columns

def test_price_range_indicator(sample_df):
    ind = PriceRangeIndicator()
    res = ind.compute(sample_df)
    assert "high_low_range_pct" in res.columns
    assert "body_range_pct" in res.columns

def test_volatility_compression_indicator(sample_df):
    ind = VolatilityCompressionIndicator()
    res = ind.compute(sample_df, {"window": 3, "reference_window": 10})
    assert "volatility_compression_3_10" in res.columns

def test_volatility_expansion_indicator(sample_df):
    ind = VolatilityExpansionIndicator()
    res = ind.compute(sample_df, {"atr_window": 3, "reference_window": 10})
    assert "volatility_expansion_3_10" in res.columns

def test_missing_required_column(sample_df):
    ind = ATRIndicator()
    bad_df = sample_df.drop(columns=["high"])
    with pytest.raises(FeatureComputationError):
        ind.compute(bad_df)
