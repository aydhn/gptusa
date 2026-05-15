import pytest
from usa_signal_bot.regime_map.regime_map_models import (
    TimeframeRegimeSnapshot,
    validate_timeframe_regime_snapshot,
    create_timeframe_regime_snapshot_id
)
from usa_signal_bot.core.enums import RegimeTimeframe, TrendRegime, VolatilityMapRegime, MomentumRegime, LiquidityMapRegime
from usa_signal_bot.core.exceptions import RegimeMapValidationError

def test_timeframe_snapshot_valid():
    snap = TimeframeRegimeSnapshot(
        snapshot_id="test",
        symbol="SPY",
        timeframe=RegimeTimeframe.DAILY,
        created_at_utc="2024-01-01T00:00:00Z",
        trend_regime=TrendRegime.UPTREND,
        volatility_regime=VolatilityMapRegime.NORMAL,
        momentum_regime=MomentumRegime.POSITIVE,
        liquidity_regime=LiquidityMapRegime.NORMAL,
        confidence=80.0,
        evidence={},
        warnings=[],
        errors=[]
    )
    validate_timeframe_regime_snapshot(snap) # Should pass

def test_timeframe_snapshot_invalid_confidence():
    snap = TimeframeRegimeSnapshot(
        snapshot_id="test",
        symbol="SPY",
        timeframe=RegimeTimeframe.DAILY,
        created_at_utc="2024-01-01T00:00:00Z",
        trend_regime=TrendRegime.UPTREND,
        volatility_regime=VolatilityMapRegime.NORMAL,
        momentum_regime=MomentumRegime.POSITIVE,
        liquidity_regime=LiquidityMapRegime.NORMAL,
        confidence=101.0,
        evidence={},
        warnings=[],
        errors=[]
    )
    with pytest.raises(RegimeMapValidationError):
        validate_timeframe_regime_snapshot(snap)

def test_id_factory():
    id1 = create_timeframe_regime_snapshot_id("SPY", RegimeTimeframe.DAILY)
    assert id1.startswith("tfs_SPY_DAILY_")
