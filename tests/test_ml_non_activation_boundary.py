import pytest
from usa_signal_bot.ml_research.foundation.ml_non_activation_boundary import (
    build_ml_non_activation_boundary_rules, build_ml_non_activation_boundary_result
)

def test_non_activation_boundary_safe():
    rules = build_ml_non_activation_boundary_rules()
    res = build_ml_non_activation_boundary_result(rules)
    assert res.boundary_passed is True

def test_non_activation_boundary_unsafe():
    rules = build_ml_non_activation_boundary_rules({"unsafe": True})
    res = build_ml_non_activation_boundary_result(rules)
    assert res.boundary_passed is False
