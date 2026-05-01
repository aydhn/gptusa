import pytest
from usa_signal_bot.features.volatility_sets import (
    basic_volatility_indicator_set, band_volatility_indicator_set,
    channel_volatility_indicator_set, compression_volatility_indicator_set,
    full_volatility_indicator_set, get_volatility_indicator_set,
    list_volatility_indicator_sets, volatility_indicator_set_to_dict
)
from usa_signal_bot.core.exceptions import VolatilityIndicatorSetError

def test_basic_volatility_set():
    s = basic_volatility_indicator_set()
    assert s.name == "basic_volatility"
    assert "atr" in s.indicators

def test_band_volatility_set():
    s = band_volatility_indicator_set()
    assert s.name == "band_volatility"
    assert "bollinger_bands" in s.indicators

def test_channel_volatility_set():
    s = channel_volatility_indicator_set()
    assert s.name == "channel_volatility"
    assert "keltner_channel" in s.indicators

def test_compression_volatility_set():
    s = compression_volatility_indicator_set()
    assert s.name == "compression_volatility"
    assert "volatility_compression" in s.indicators

def test_full_volatility_set():
    s = full_volatility_indicator_set()
    assert s.name == "full_volatility"
    assert len(s.indicators) >= 12

def test_get_volatility_indicator_set():
    s = get_volatility_indicator_set("basic_volatility")
    assert s.name == "basic_volatility"

    with pytest.raises(VolatilityIndicatorSetError):
        get_volatility_indicator_set("unknown_set")

def test_list_volatility_indicator_sets():
    sets = list_volatility_indicator_sets()
    assert len(sets) == 5

def test_volatility_indicator_set_to_dict():
    s = basic_volatility_indicator_set()
    d = volatility_indicator_set_to_dict(s)
    assert d["name"] == "basic_volatility"
    assert "atr" in d["indicators"]
