import os
import re

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def write_file(file_path, content):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# TESTS
# ---------------------------------------------------------
tests_content = """
import pytest
from usa_signal_bot.cost_robustness.robustness_models import (
    CostStressScenario, validate_cost_stress_scenario, create_cost_stress_scenario_id,
    CostFragilityAssessment, validate_cost_fragility_assessment
)
from usa_signal_bot.core.enums import CostStressType, CostStressSeverity, FillRealismMode, CostRobustnessStatus

def test_cost_stress_scenario_valid():
    scene = CostStressScenario(
        scenario_id="s1",
        name="test",
        stress_type=CostStressType.SLIPPAGE,
        severity=CostStressSeverity.BASELINE,
        slippage_multiplier=1.0,
        spread_multiplier=1.0,
        impact_multiplier=1.0,
        fee_multiplier=1.0,
        participation_multiplier=1.0,
        min_dollar_volume=None,
        fill_realism_mode=FillRealismMode.BASELINE,
        enabled=True
    )
    validate_cost_stress_scenario(scene)

def test_cost_stress_scenario_invalid():
    scene = CostStressScenario(
        scenario_id="s1",
        name="test",
        stress_type=CostStressType.SLIPPAGE,
        severity=CostStressSeverity.BASELINE,
        slippage_multiplier=-1.0,
        spread_multiplier=1.0,
        impact_multiplier=1.0,
        fee_multiplier=1.0,
        participation_multiplier=1.0,
        min_dollar_volume=None,
        fill_realism_mode=FillRealismMode.BASELINE,
        enabled=True
    )
    with pytest.raises(ValueError):
        validate_cost_stress_scenario(scene)

def test_fragility_assessment_valid():
    f = CostFragilityAssessment(
        assessment_id="f1",
        created_at_utc="now",
        status=CostRobustnessStatus.ROBUST,
        fragility_score=85.0,
        reasons=[],
        breakeven_cost_bps=None,
        breakeven_slippage_bps=None,
        breakeven_impact_bps=None,
        evidence={},
        warnings=[],
        errors=[]
    )
    validate_cost_fragility_assessment(f)
"""
write_file("tests/test_robustness_models.py", tests_content)

test_scenarios_content = """
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
"""
write_file("tests/test_stress_scenarios.py", test_scenarios_content)

test_adapters_content = """
from usa_signal_bot.cost_robustness.backtest_adapter import attach_cost_robustness_to_backtest_result, backtest_requires_cost_review
from usa_signal_bot.cost_robustness.signal_adapter import attach_cost_robustness_to_candidate, suppress_candidate_if_cost_fragile
from usa_signal_bot.cost_robustness.robustness_models import CostFragilityAssessment
from usa_signal_bot.core.enums import CostRobustnessStatus

def test_backtest_adapter():
    res = {"metrics": {}}
    res2 = attach_cost_robustness_to_backtest_result(res)
    assert res2['metadata']['cost_robustness_status'] == "ROBUST"
    assert not backtest_requires_cost_review(res2)

def test_signal_adapter():
    cand = {"symbol": "AAPL"}
    ass = CostFragilityAssessment("id", "now", CostRobustnessStatus.FRAGILE, 30.0, [], None, None, None, {}, [], [])
    cand2 = attach_cost_robustness_to_candidate(cand, ass)
    assert cand2['metadata']['cost_robustness_attached']

    cand3 = suppress_candidate_if_cost_fragile(cand2, ass)
    assert cand3['metadata']['suppressed_due_to_fragility']
"""
write_file("tests/test_cost_robustness_backtest_adapter.py", test_adapters_content)
