import pytest
from usa_signal_bot.core.enums import CostLifecycleRegime
from usa_signal_bot.regime_costs.lifecycle_regime_cost import (
    classify_cost_lifecycle_regime, lifecycle_cost_multiplier,
    lifecycle_cost_warnings, lifecycle_regime_to_text
)

def test_lifecycle_regime_classification():
    assert classify_cost_lifecycle_regime(None, None, None) == CostLifecycleRegime.NORMAL
    assert classify_cost_lifecycle_regime("pending_split", None, None) == CostLifecycleRegime.CORPORATE_ACTION_WATCH
    assert classify_cost_lifecycle_regime("post_split", None, None) == CostLifecycleRegime.POST_SPLIT_WINDOW
    assert classify_cost_lifecycle_regime(None, "delist", None) == CostLifecycleRegime.DELISTING_RISK
    assert classify_cost_lifecycle_regime(None, None, "inconsistent_data") == CostLifecycleRegime.ADJUSTED_DATA_RISK

def test_lifecycle_multiplier():
    assert lifecycle_cost_multiplier(CostLifecycleRegime.NORMAL) == 1.0
    assert lifecycle_cost_multiplier(CostLifecycleRegime.DELISTING_RISK) > 1.0

def test_lifecycle_warnings():
    w = lifecycle_cost_warnings(CostLifecycleRegime.DELISTING_RISK)
    assert len(w) == 1
    assert "Delisting" in w[0]

def test_lifecycle_text():
    t = lifecycle_regime_to_text(CostLifecycleRegime.DELISTING_RISK, 4.0)
    assert "DELISTING" in t
    assert "4.0" in t
