import pytest
from usa_signal_bot.features.price_action_sets import (
    get_price_action_indicator_set, list_price_action_indicator_sets,
    price_action_indicator_set_to_dict
)
from usa_signal_bot.core.exceptions import IndicatorSetError

def test_get_basic_price_action_set():
    s = get_price_action_indicator_set("basic_price_action")
    assert s.name == "basic_price_action"
    assert "candle_features" in s.indicators

def test_get_breakout_price_action_set():
    s = get_price_action_indicator_set("breakout_price_action")
    assert s.name == "breakout_price_action"
    assert "breakout_distance" in s.indicators

def test_get_structure_price_action_set():
    s = get_price_action_indicator_set("structure_price_action")
    assert s.name == "structure_price_action"
    assert "swing_points" in s.indicators

def test_get_candle_price_action_set():
    s = get_price_action_indicator_set("candle_price_action")
    assert s.name == "candle_price_action"
    assert "inside_outside_bar" in s.indicators

def test_get_full_price_action_set():
    s = get_price_action_indicator_set("full_price_action")
    assert s.name == "full_price_action"
    assert len(s.indicators) > 5

def test_get_unknown_set():
    with pytest.raises(IndicatorSetError):
        get_price_action_indicator_set("unknown_set")

def test_list_price_action_sets():
    sets = list_price_action_indicator_sets()
    assert len(sets) >= 5
    names = [s.name for s in sets]
    assert "basic_price_action" in names
    assert "full_price_action" in names

def test_set_to_dict():
    s = get_price_action_indicator_set("basic_price_action")
    d = price_action_indicator_set_to_dict(s)
    assert d["name"] == "basic_price_action"
    assert "candle_features" in d["indicators"]
