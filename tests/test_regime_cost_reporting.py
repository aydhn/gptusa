import pytest
from usa_signal_bot.regime_costs.regime_cost_reporting import (
    cost_regime_snapshot_to_text, regime_cost_limitations_text
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot

def test_reporting():
    s = build_cost_regime_snapshot("SPY")
    t = cost_regime_snapshot_to_text(s)
    assert "SPY" in t

    lim = regime_cost_limitations_text()
    assert "NOT INVESTMENT ADVICE" in lim
    assert "guarantee" in lim.lower()
