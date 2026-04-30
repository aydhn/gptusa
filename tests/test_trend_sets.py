import pytest
from usa_signal_bot.features.trend_sets import (
    basic_trend_indicator_set, moving_average_trend_indicator_set,
    macd_trend_indicator_set, full_trend_indicator_set,
    get_trend_indicator_set, list_trend_indicator_sets, indicator_set_to_dict
)
from usa_signal_bot.core.exceptions import IndicatorSetError

def test_basic_trend_set():
    s = basic_trend_indicator_set()
    assert s.name == "basic_trend"
    assert "sma" in s.indicators
    assert "window" in s.params_by_indicator["sma"]

def test_moving_average_trend_set():
    s = moving_average_trend_indicator_set()
    assert s.name == "moving_average_trend"
    assert "tema" in s.indicators

def test_macd_trend_set():
    s = macd_trend_indicator_set()
    assert s.name == "macd_trend"
    assert s.indicators == ["macd"]

def test_full_trend_set():
    s = full_trend_indicator_set()
    assert s.name == "full_trend"
    assert len(s.indicators) > 5

def test_get_trend_indicator_set():
    s = get_trend_indicator_set("basic_trend")
    assert s.name == "basic_trend"

    with pytest.raises(IndicatorSetError):
        get_trend_indicator_set("unknown_set")

def test_list_trend_indicator_sets():
    sets = list_trend_indicator_sets()
    names = [s.name for s in sets]
    assert "basic_trend" in names
    assert "macd_trend" in names

def test_indicator_set_to_dict():
    s = macd_trend_indicator_set()
    d = indicator_set_to_dict(s)
    assert d["name"] == "macd_trend"
    assert d["indicators"] == ["macd"]
