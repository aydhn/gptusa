import pytest
from usa_signal_bot.core.enums import CostSpreadRegime
from usa_signal_bot.regime_costs.spread_regime_cost import (
    classify_cost_spread_regime, spread_cost_multiplier,
    spread_cost_warnings, spread_regime_to_text
)

def test_spread_regime_classification():
    assert classify_cost_spread_regime(10.0) == CostSpreadRegime.TIGHT
    assert classify_cost_spread_regime(50.0) == CostSpreadRegime.NORMAL
    assert classify_cost_spread_regime(150.0) == CostSpreadRegime.WIDE
    assert classify_cost_spread_regime(250.0) == CostSpreadRegime.VERY_WIDE
    assert classify_cost_spread_regime(None) == CostSpreadRegime.INSUFFICIENT_DATA

def test_spread_multiplier():
    assert spread_cost_multiplier(CostSpreadRegime.TIGHT) < 1.0
    assert spread_cost_multiplier(CostSpreadRegime.NORMAL) == 1.0
    assert spread_cost_multiplier(CostSpreadRegime.VERY_WIDE) > 1.0

def test_spread_warnings():
    w = spread_cost_warnings(CostSpreadRegime.VERY_WIDE)
    assert len(w) == 1
    assert "Very wide" in w[0]

def test_spread_text():
    t = spread_regime_to_text(CostSpreadRegime.WIDE, 1.75)
    assert "WIDE" in t
    assert "1.75" in t
