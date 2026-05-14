
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
