import pytest
from usa_signal_bot.core.enums import (
    CostVolatilityRegime, CostLiquidityRegime, CostSpreadRegime,
    CostSessionRegime, CostLifecycleRegime, CombinedCostRegime,
    RegimeCostCurveProfile, AdaptiveExecutionDecision, RegimeCostAdjustmentStatus, RegimeCostReportType
)
from usa_signal_bot.regime_costs.regime_cost_models import (
    CostRegimeSnapshot, RegimeCostMultiplier, RegimeCostCurveSelection,
    AdaptiveExecutionRealismDecision, RegimeAwareCostBreakdown, RegimeCostReview,
    validate_cost_regime_snapshot, validate_regime_cost_multiplier,
    create_cost_regime_snapshot_id, get_utc_now_str
)
from usa_signal_bot.core.exceptions import RegimeCostValidationError

def test_cost_regime_snapshot_valid():
    s = CostRegimeSnapshot(
        snapshot_id="test",
        symbol="AAPL",
        created_at_utc=get_utc_now_str(),
        volatility_regime=CostVolatilityRegime.NORMAL,
        liquidity_regime=CostLiquidityRegime.DEEP,
        spread_regime=CostSpreadRegime.TIGHT,
        session_regime=CostSessionRegime.REGULAR,
        lifecycle_regime=CostLifecycleRegime.NORMAL,
        combined_regime=CombinedCostRegime.NORMAL,
        evidence={},
        warnings=[],
        errors=[]
    )
    validate_cost_regime_snapshot(s)
    assert s.symbol == "AAPL"

def test_cost_regime_snapshot_invalid():
    s = CostRegimeSnapshot(
        snapshot_id="test",
        symbol="",
        created_at_utc=get_utc_now_str(),
        volatility_regime=CostVolatilityRegime.NORMAL,
        liquidity_regime=CostLiquidityRegime.DEEP,
        spread_regime=CostSpreadRegime.TIGHT,
        session_regime=CostSessionRegime.REGULAR,
        lifecycle_regime=CostLifecycleRegime.NORMAL,
        combined_regime=CombinedCostRegime.NORMAL,
        evidence={},
        warnings=[],
        errors=[]
    )
    with pytest.raises(RegimeCostValidationError):
        validate_cost_regime_snapshot(s)

def test_regime_cost_multiplier_invalid():
    m = RegimeCostMultiplier(
        multiplier_id="test",
        symbol="AAPL",
        created_at_utc=get_utc_now_str(),
        volatility_multiplier=-1.0,
        liquidity_multiplier=1.0,
        spread_multiplier=1.0,
        session_multiplier=1.0,
        lifecycle_multiplier=1.0,
        combined_multiplier=-1.0,
        min_cost_bps=None,
        max_cost_bps=None,
        warnings=[],
        errors=[]
    )
    with pytest.raises(RegimeCostValidationError):
        validate_regime_cost_multiplier(m)

    m2 = RegimeCostMultiplier(
        multiplier_id="test",
        symbol="AAPL",
        created_at_utc=get_utc_now_str(),
        volatility_multiplier=1.0,
        liquidity_multiplier=1.0,
        spread_multiplier=1.0,
        session_multiplier=1.0,
        lifecycle_multiplier=1.0,
        combined_multiplier=1.0,
        min_cost_bps=10.0,
        max_cost_bps=5.0,
        warnings=[],
        errors=[]
    )
    with pytest.raises(RegimeCostValidationError):
        validate_regime_cost_multiplier(m2)
