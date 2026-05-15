import pytest
from usa_signal_bot.regime_costs.backtest_adapter import (
    attach_regime_costs_to_backtest_trade, attach_regime_costs_to_backtest_result,
    backtest_regime_cost_summary, backtest_regime_cost_warnings
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot
from usa_signal_bot.core.enums import CombinedCostRegime

def test_attach_regime_costs_to_backtest_trade():
    s = build_cost_regime_snapshot("SPY")
    trade = {"symbol": "SPY"}
    res = attach_regime_costs_to_backtest_trade(trade, snapshot=s)
    assert res["metadata"]["cost_regime"] == s.combined_regime.value

def test_backtest_result_summary():
    s1 = build_cost_regime_snapshot("SPY")
    s1.combined_regime = CombinedCostRegime.NORMAL
    s2 = build_cost_regime_snapshot("SPY")
    s2.combined_regime = CombinedCostRegime.HIGH_RISK
    res = attach_regime_costs_to_backtest_result({}, [s1, s2])
    dist = res["metadata"]["regime_distribution"]
    assert dist["NORMAL"] == 1
    assert dist["HIGH_RISK"] == 1
    assert "HIGH_RISK" in backtest_regime_cost_warnings(res)[0]
