from pathlib import Path
from usa_signal_bot.regime_map.regime_map_store import regime_map_store_dir, write_timeframe_regime_snapshot_json
from usa_signal_bot.regime_map.regime_map_models import TimeframeRegimeSnapshot
from usa_signal_bot.core.enums import RegimeTimeframe, TrendRegime, VolatilityMapRegime, MomentumRegime, LiquidityMapRegime

def test_store_dir(tmp_path):
    d = regime_map_store_dir(tmp_path)
    assert d.exists()

def test_write_snapshot(tmp_path):
    d = regime_map_store_dir(tmp_path)
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
    p = write_timeframe_regime_snapshot_json(d / "test.json", snap)
    assert p.exists()
