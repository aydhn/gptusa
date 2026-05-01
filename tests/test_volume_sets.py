import pytest

from usa_signal_bot.features.volume_sets import (
    basic_volume_indicator_set, flow_volume_indicator_set,
    liquidity_volume_indicator_set, full_volume_indicator_set,
    list_volume_indicator_sets, get_volume_indicator_set,
    volume_indicator_set_to_dict
)

def test_basic_volume_set():
    s = basic_volume_indicator_set()
    assert s.name == "basic_volume"
    assert "relative_volume" in s.indicators

def test_list_volume_indicator_sets():
    sets = list_volume_indicator_sets()
    assert len(sets) == 4

def test_get_volume_indicator_set():
    s = get_volume_indicator_set("flow_volume")
    assert s.name == "flow_volume"
