import pytest
import pandas as pd
import numpy as np
from usa_signal_bot.features.volatility_utils import (
    calculate_true_range, calculate_atr, calculate_normalized_atr,
    calculate_bollinger_bands, calculate_bollinger_bandwidth, calculate_bollinger_percent_b,
    calculate_keltner_channels, calculate_donchian_channels, calculate_rolling_volatility,
    calculate_price_range_pct, calculate_body_range_pct, calculate_volatility_compression,
    calculate_volatility_expansion, validate_band_multiplier, validate_volatility_window
)
from usa_signal_bot.core.exceptions import IndicatorParameterError

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "open": [10.0, 10.5, 11.0, 10.8, 11.2, 11.5, 12.0, 11.8, 12.5, 13.0],
        "high": [10.5, 11.0, 11.5, 11.2, 11.8, 12.0, 12.5, 12.2, 13.0, 13.5],
        "low": [9.5, 10.0, 10.5, 10.2, 10.8, 11.0, 11.5, 11.2, 12.0, 12.5],
        "close": [10.2, 10.8, 11.2, 10.5, 11.5, 11.8, 11.6, 12.3, 12.8, 13.2]
    })

def test_calculate_true_range(sample_data):
    tr = calculate_true_range(sample_data["high"], sample_data["low"], sample_data["close"])
    assert len(tr) == 10
    assert not pd.isna(tr.iloc[0])

def test_calculate_atr(sample_data):
    atr = calculate_atr(sample_data["high"], sample_data["low"], sample_data["close"], window=5, method="sma")
    assert len(atr) == 10
    assert pd.isna(atr.iloc[0])
    assert not pd.isna(atr.iloc[5])

    with pytest.raises(IndicatorParameterError):
        calculate_atr(sample_data["high"], sample_data["low"], sample_data["close"], method="invalid")

def test_calculate_normalized_atr(sample_data):
    natr = calculate_normalized_atr(sample_data["high"], sample_data["low"], sample_data["close"], window=5, method="sma")
    assert len(natr) == 10
    assert not pd.isna(natr.iloc[-1])
    assert natr.iloc[-1] >= 0

def test_calculate_bollinger_bands(sample_data):
    bb = calculate_bollinger_bands(sample_data["close"], window=5, num_std=2.0)
    assert len(bb) == 10
    assert "upper" in bb.columns
    assert "middle" in bb.columns
    assert "lower" in bb.columns
    assert (bb["upper"].dropna() > bb["lower"].dropna()).all()

def test_calculate_bollinger_bandwidth_and_percent_b(sample_data):
    bb = calculate_bollinger_bands(sample_data["close"], window=5, num_std=2.0)
    bw = calculate_bollinger_bandwidth(bb["upper"], bb["middle"], bb["lower"])
    pb = calculate_bollinger_percent_b(sample_data["close"], bb["upper"], bb["lower"])
    assert len(bw) == 10
    assert len(pb) == 10
    assert not pd.isna(bw.iloc[-1])
    assert not pd.isna(pb.iloc[-1])

def test_calculate_keltner_channels(sample_data):
    kc = calculate_keltner_channels(sample_data["high"], sample_data["low"], sample_data["close"], ema_window=5, atr_window=5)
    assert len(kc) == 10
    assert "upper" in kc.columns
    assert "middle" in kc.columns
    assert "lower" in kc.columns

def test_calculate_donchian_channels(sample_data):
    dc = calculate_donchian_channels(sample_data["high"], sample_data["low"], window=5)
    assert len(dc) == 10
    assert "upper" in dc.columns
    assert "middle" in dc.columns
    assert "lower" in dc.columns

def test_calculate_rolling_volatility(sample_data):
    vol = calculate_rolling_volatility(sample_data["close"], window=5)
    assert len(vol) == 10
    assert pd.isna(vol.iloc[0])
    assert not pd.isna(vol.iloc[5])

def test_calculate_price_range_pct(sample_data):
    pr = calculate_price_range_pct(sample_data["high"], sample_data["low"], sample_data["close"])
    assert len(pr) == 10
    assert not pd.isna(pr.iloc[0])

def test_calculate_body_range_pct(sample_data):
    br = calculate_body_range_pct(sample_data["open"], sample_data["close"], sample_data["high"], sample_data["low"])
    assert len(br) == 10
    assert not pd.isna(br.iloc[0])

def test_calculate_volatility_compression_expansion(sample_data):
    bb = calculate_bollinger_bands(sample_data["close"], window=3, num_std=2.0)
    bw = calculate_bollinger_bandwidth(bb["upper"], bb["middle"], bb["lower"])
    comp = calculate_volatility_compression(bw, reference_window=5)

    atr = calculate_atr(sample_data["high"], sample_data["low"], sample_data["close"], window=3, method="sma")
    exp = calculate_volatility_expansion(atr, reference_window=5)

    assert len(comp) == 10
    assert len(exp) == 10

def test_validate_band_multiplier():
    validate_band_multiplier(2.0, "mult")
    with pytest.raises(IndicatorParameterError):
        validate_band_multiplier(-1.0, "mult")
    with pytest.raises(IndicatorParameterError):
        validate_band_multiplier("2.0", "mult")
