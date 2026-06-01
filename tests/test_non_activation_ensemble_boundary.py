import pytest
from usa_signal_bot.ml_research.ensemble_scaffolding.non_activation_ensemble_boundary import build_non_activation_ensemble_boundary_result, build_non_activation_ensemble_boundary_rules

def test_build_bound():
    rules = build_non_activation_ensemble_boundary_rules()
    bound = build_non_activation_ensemble_boundary_result(rules)
    assert bound.boundary_passed is True
    assert bound.no_live_inference is True
