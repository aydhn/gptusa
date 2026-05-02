import pytest
from usa_signal_bot.strategies.example_strategies import (
    TrendFollowingSkeletonStrategy,
    MeanReversionSkeletonStrategy,
    MomentumSkeletonStrategy,
    VolatilityBreakoutSkeletonStrategy
)
from usa_signal_bot.strategies.strategy_input import StrategyInputBatch, StrategyFeatureFrame

def make_batch(rows, feature_names):
    frame = StrategyFeatureFrame("AAPL", "1d", rows, feature_names)
    return StrategyInputBatch([frame], "test", ["AAPL"], ["1d"], "test")

def test_trend_following():
    s = TrendFollowingSkeletonStrategy()

    # Missing feature
    b1 = make_batch([{"close_ema_20": 10}], ["close_ema_20"])
    sigs1 = s.generate_signals(b1)
    assert len(sigs1) == 0

    # Valid candidate
    b2 = make_batch([{"close_ema_20": 105, "close_ema_50": 100}], ["close_ema_20", "close_ema_50"])
    sigs2 = s.generate_signals(b2)
    assert len(sigs2) == 1
    assert "105" in sigs2[0].reasons[0]

def test_mean_reversion():
    s = MeanReversionSkeletonStrategy()

    # Inside bounds
    b1 = make_batch([{"close_bb_percent_b_20_2.0": 0.5}], ["close_bb_percent_b_20_2.0"])
    sigs1 = s.generate_signals(b1)
    assert len(sigs1) == 0

    # Outside bounds
    b2 = make_batch([{"close_bb_percent_b_20_2.0": 0.01}], ["close_bb_percent_b_20_2.0"])
    sigs2 = s.generate_signals(b2)
    assert len(sigs2) == 1

def test_momentum():
    s = MomentumSkeletonStrategy()

    # Normal
    b1 = make_batch([{"close_rsi_14": 50, "close_roc_12": 1}], ["close_rsi_14", "close_roc_12"])
    sigs1 = s.generate_signals(b1)
    assert len(sigs1) == 0

    # Extreme
    b2 = make_batch([{"close_rsi_14": 80, "close_roc_12": 6}], ["close_rsi_14", "close_roc_12"])
    sigs2 = s.generate_signals(b2)
    assert len(sigs2) == 1

def test_volatility():
    s = VolatilityBreakoutSkeletonStrategy()

    # No breakout
    b1 = make_batch([{"volatility_compression_20_100": 1, "breakout_distance_pct_20": 0.01}], ["volatility_compression_20_100", "breakout_distance_pct_20"])
    sigs1 = s.generate_signals(b1)
    assert len(sigs1) == 0

    # Breakout
    b2 = make_batch([{"volatility_compression_20_100": 1, "breakout_distance_pct_20": 0.05}], ["volatility_compression_20_100", "breakout_distance_pct_20"])
    sigs2 = s.generate_signals(b2)
    assert len(sigs2) == 1
