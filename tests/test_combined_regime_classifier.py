import pytest
from usa_signal_bot.core.enums import (
    CostVolatilityRegime, CostLiquidityRegime, CostSpreadRegime,
    CostSessionRegime, CostLifecycleRegime, CombinedCostRegime
)
from usa_signal_bot.regime_costs.combined_regime_classifier import (
    classify_combined_cost_regime, build_cost_regime_snapshot, build_regime_cost_multiplier,
    combined_regime_to_text, combined_regime_warnings
)

def test_combined_classification():
    assert classify_combined_cost_regime(CostVolatilityRegime.NORMAL, CostLiquidityRegime.NORMAL, CostSpreadRegime.NORMAL, CostSessionRegime.REGULAR, CostLifecycleRegime.NORMAL) == CombinedCostRegime.NORMAL

    assert classify_combined_cost_regime(CostVolatilityRegime.NORMAL, CostLiquidityRegime.NORMAL, CostSpreadRegime.NORMAL, CostSessionRegime.CLOSED, CostLifecycleRegime.NORMAL) == CombinedCostRegime.BLOCKED

    assert classify_combined_cost_regime(CostVolatilityRegime.EXTREME, CostLiquidityRegime.ILLIQUID, CostSpreadRegime.NORMAL, CostSessionRegime.REGULAR, CostLifecycleRegime.NORMAL) == CombinedCostRegime.HIGH_RISK

    assert classify_combined_cost_regime(CostVolatilityRegime.HIGH, CostLiquidityRegime.THIN, CostSpreadRegime.NORMAL, CostSessionRegime.REGULAR, CostLifecycleRegime.NORMAL) == CombinedCostRegime.STRESSED

    assert classify_combined_cost_regime(CostVolatilityRegime.INSUFFICIENT_DATA, CostLiquidityRegime.NORMAL, CostSpreadRegime.NORMAL, CostSessionRegime.REGULAR, CostLifecycleRegime.NORMAL) == CombinedCostRegime.INSUFFICIENT_DATA

def test_build_cost_regime_snapshot():
    s = build_cost_regime_snapshot("SPY", {"atr_pct": 2.0}, {"avg_dollar_volume": 100_000_000}, 50.0, "REGULAR")
    assert s.combined_regime == CombinedCostRegime.NORMAL

def test_build_regime_cost_multiplier():
    s = build_cost_regime_snapshot("SPY", {"atr_pct": 2.0}, {"avg_dollar_volume": 10_000_000}, 50.0, "REGULAR")
    m = build_regime_cost_multiplier("SPY", s)
    assert m.combined_multiplier == 1.0

def test_combined_text_and_warnings():
    s = build_cost_regime_snapshot("SPY", {"atr_pct": 10.0}, {"avg_dollar_volume": 100_000_000}, 50.0, "CLOSED")
    assert s.combined_regime == CombinedCostRegime.BLOCKED
    w = combined_regime_warnings(s)
    assert any("BLOCKED" in msg for msg in w)
    t = combined_regime_to_text(s)
    assert "BLOCKED" in t
