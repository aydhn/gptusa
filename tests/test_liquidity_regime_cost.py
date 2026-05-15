import pytest
from usa_signal_bot.core.enums import CostLiquidityRegime
from usa_signal_bot.regime_costs.liquidity_regime_cost import (
    classify_cost_liquidity_regime, liquidity_cost_multiplier,
    liquidity_cost_warnings, liquidity_regime_to_text
)

def test_liquidity_regime_classification():
    assert classify_cost_liquidity_regime(avg_dollar_volume=150_000_000) == CostLiquidityRegime.DEEP
    assert classify_cost_liquidity_regime(avg_dollar_volume=20_000_000) == CostLiquidityRegime.NORMAL
    assert classify_cost_liquidity_regime(avg_dollar_volume=5_000_000) == CostLiquidityRegime.THIN
    assert classify_cost_liquidity_regime(avg_dollar_volume=500_000) == CostLiquidityRegime.ILLIQUID
    assert classify_cost_liquidity_regime(None, None, "FROZEN") == CostLiquidityRegime.FROZEN
    assert classify_cost_liquidity_regime(None, None, None) == CostLiquidityRegime.INSUFFICIENT_DATA

def test_liquidity_multiplier():
    assert liquidity_cost_multiplier(CostLiquidityRegime.DEEP) < 1.0
    assert liquidity_cost_multiplier(CostLiquidityRegime.NORMAL) == 1.0
    assert liquidity_cost_multiplier(CostLiquidityRegime.ILLIQUID) > 1.0

def test_liquidity_warnings():
    w = liquidity_cost_warnings(CostLiquidityRegime.FROZEN)
    assert len(w) == 1
    assert "Frozen" in w[0]

def test_liquidity_text():
    t = liquidity_regime_to_text(CostLiquidityRegime.THIN, 1.75)
    assert "THIN" in t
    assert "1.75" in t
