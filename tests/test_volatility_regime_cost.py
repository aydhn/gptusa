import pytest
from usa_signal_bot.core.enums import CostVolatilityRegime
from usa_signal_bot.regime_costs.volatility_regime_cost import (
    classify_cost_volatility_regime, volatility_cost_multiplier,
    volatility_cost_warnings, volatility_regime_to_text
)

def test_volatility_regime_classification():
    assert classify_cost_volatility_regime(atr_pct=0.2) == CostVolatilityRegime.VERY_LOW
    assert classify_cost_volatility_regime(atr_pct=0.8) == CostVolatilityRegime.LOW
    assert classify_cost_volatility_regime(atr_pct=2.0) == CostVolatilityRegime.NORMAL
    assert classify_cost_volatility_regime(atr_pct=4.0) == CostVolatilityRegime.HIGH
    assert classify_cost_volatility_regime(atr_pct=7.0) == CostVolatilityRegime.EXTREME
    assert classify_cost_volatility_regime(atr_pct=1.0, gap_pct=12.0) == CostVolatilityRegime.EXTREME
    assert classify_cost_volatility_regime(None, None, None) == CostVolatilityRegime.INSUFFICIENT_DATA

def test_volatility_multiplier():
    assert volatility_cost_multiplier(CostVolatilityRegime.VERY_LOW) < 1.0
    assert volatility_cost_multiplier(CostVolatilityRegime.NORMAL) == 1.0
    assert volatility_cost_multiplier(CostVolatilityRegime.EXTREME) > 1.0

def test_volatility_warnings():
    w = volatility_cost_warnings(CostVolatilityRegime.EXTREME)
    assert len(w) == 1
    assert "Extreme volatility" in w[0]

def test_volatility_text():
    t = volatility_regime_to_text(CostVolatilityRegime.NORMAL, 1.0)
    assert "NORMAL" in t
    assert "1.00" in t
