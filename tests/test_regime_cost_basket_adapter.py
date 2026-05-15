import pytest
from usa_signal_bot.regime_costs.basket_adapter import (
    attach_regime_costs_to_basket_result, basket_regime_concentration_warnings
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot
from usa_signal_bot.core.enums import CombinedCostRegime

def test_basket_adapter():
    s = build_cost_regime_snapshot("SPY")
    s.combined_regime = CombinedCostRegime.BLOCKED
    res = attach_regime_costs_to_basket_result({}, [s])
    assert res["metadata"]["basket_regime_concentration"]["BLOCKED"] == 1
    w = basket_regime_concentration_warnings(res)
    assert len(w) == 1
