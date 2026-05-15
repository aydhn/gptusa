import pytest
from usa_signal_bot.regime_map.regime_map_models import (
    TimeframeRegimeSnapshot,
    validate_timeframe_regime_snapshot,
    create_timeframe_regime_snapshot_id
)
from usa_signal_bot.core.enums import RegimeTimeframe, TrendRegime, VolatilityMapRegime, MomentumRegime, LiquidityMapRegime

def test_timeframe_regime_snapshot_valid():
    snap = TimeframeRegimeSnapshot(
        snapshot_id="test",
        symbol="SPY",
        timeframe=RegimeTimeframe.DAILY,
        created_at_utc="2023-01-01T00:00:00Z",
        trend_regime=TrendRegime.UPTREND,
        volatility_regime=VolatilityMapRegime.NORMAL,
        momentum_regime=MomentumRegime.POSITIVE,
        liquidity_regime=LiquidityMapRegime.DEEP,
        confidence=80.0,
        evidence={},
        warnings=[],
        errors=[]
    )
    validate_timeframe_regime_snapshot(snap)

def test_timeframe_regime_snapshot_invalid_symbol():
    snap = TimeframeRegimeSnapshot(
        snapshot_id="test",
        symbol="",
        timeframe=RegimeTimeframe.DAILY,
        created_at_utc="2023-01-01T00:00:00Z",
        trend_regime=TrendRegime.UPTREND,
        volatility_regime=VolatilityMapRegime.NORMAL,
        momentum_regime=MomentumRegime.POSITIVE,
        liquidity_regime=LiquidityMapRegime.DEEP,
        confidence=80.0,
        evidence={},
        warnings=[],
        errors=[]
    )
    with pytest.raises(ValueError):
        validate_timeframe_regime_snapshot(snap)

def test_timeframe_regime_snapshot_invalid_confidence():
    snap = TimeframeRegimeSnapshot(
        snapshot_id="test",
        symbol="SPY",
        timeframe=RegimeTimeframe.DAILY,
        created_at_utc="2023-01-01T00:00:00Z",
        trend_regime=TrendRegime.UPTREND,
        volatility_regime=VolatilityMapRegime.NORMAL,
        momentum_regime=MomentumRegime.POSITIVE,
        liquidity_regime=LiquidityMapRegime.DEEP,
        confidence=150.0,
        evidence={},
        warnings=[],
        errors=[]
    )
    with pytest.raises(ValueError):
        validate_timeframe_regime_snapshot(snap)
