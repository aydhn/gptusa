
import pytest
from usa_signal_bot.cost_robustness.stress_scenarios import default_cost_stress_scenarios, filter_enabled_scenarios

def test_default_scenarios():
    scenarios = default_cost_stress_scenarios()
    assert len(scenarios) == 5
    baseline = next(s for s in scenarios if s.name == "Baseline Scenario")
    assert baseline.slippage_multiplier == 1.0

def test_filter_enabled():
    scenarios = default_cost_stress_scenarios()
    scenarios[0].enabled = False
    filtered = filter_enabled_scenarios(scenarios)
    assert len(filtered) == 4
