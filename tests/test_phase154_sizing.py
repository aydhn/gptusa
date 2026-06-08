import pytest
import pandas as pd
from usa_signal_bot.portfolio.sizing.phase154_models import (
    SizingCandidate, SizingPolicy, SizingMethodContract,
    SizingPrototypeResult, SizingComparisonMatrix, SizingSafetyBoundaryResult
)
from usa_signal_bot.portfolio.sizing.sizing_input_resolver import detect_forbidden_sizing_columns
from usa_signal_bot.portfolio.sizing.fixed_fractional_sizing import calculate_fixed_fractional_prototype
from usa_signal_bot.portfolio.sizing.volatility_adjusted_sizing import calculate_volatility_adjusted_prototype
from usa_signal_bot.portfolio.sizing.sizing_safety_boundary import sizing_safety_boundary_passed, build_sizing_safety_boundary_rules
from usa_signal_bot.portfolio.sizing.sizing_policy import build_default_sizing_policy

def test_detect_forbidden_columns():
    cols = ["symbol", "broker_order", "volatility_proxy"]
    forbidden = detect_forbidden_sizing_columns(cols)
    assert "broker_order" in forbidden
    assert len(forbidden) == 1

def test_fixed_fractional_sizing():
    c = SizingCandidate(symbol="AAPL", eligible_for_research_prototype=True)
    p = build_default_sizing_policy()
    res = calculate_fixed_fractional_prototype(c, p)
    assert res == p.base_prototype_fraction

def test_volatility_adjusted_sizing():
    c = SizingCandidate(symbol="AAPL", eligible_for_research_prototype=True, volatility_proxy=0.01)
    p = build_default_sizing_policy()
    p.volatility_penalty_enabled = True
    res = calculate_volatility_adjusted_prototype(c, p)
    assert res < p.base_prototype_fraction  # Penalty applied
    assert res > 0.0

def test_safety_boundary_safe():
    rules = build_sizing_safety_boundary_rules()
    res = SizingSafetyBoundaryResult(rules=rules)
    res.boundary_passed = sizing_safety_boundary_passed(res)
    assert res.boundary_passed is True

def test_safety_boundary_unsafe():
    rules = build_sizing_safety_boundary_rules({"live_trading_enabled": True})
    res = SizingSafetyBoundaryResult(rules=rules)
    res.boundary_passed = sizing_safety_boundary_passed(res)
    assert res.boundary_passed is False
