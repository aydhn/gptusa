import pytest
from usa_signal_bot.features.divergence_sets import (
    basic_divergence_indicator_set, oscillator_divergence_indicator_set,
    volume_divergence_indicator_set, full_divergence_indicator_set,
    get_divergence_indicator_set, list_divergence_indicator_sets
)
from usa_signal_bot.core.exceptions import DivergenceIndicatorSetError

def test_basic_divergence_set():
    s = basic_divergence_indicator_set()
    assert s.name == "basic_divergence"
    assert "rsi_divergence" in s.indicators

def test_get_divergence_set():
    s = get_divergence_indicator_set("volume_divergence")
    assert s.name == "volume_divergence"

def test_get_unknown_set():
    with pytest.raises(DivergenceIndicatorSetError):
        get_divergence_indicator_set("unknown_set")

def test_list_divergence_sets():
    sets = list_divergence_indicator_sets()
    assert len(sets) == 4
