import pytest
from usa_signal_bot.strategies.strategy_interface import Strategy
from usa_signal_bot.strategies.example_strategies import TrendFollowingSkeletonStrategy
from usa_signal_bot.strategies.strategy_input import StrategyInputBatch, StrategyFeatureFrame

def test_strategy_abstract():
    with pytest.raises(TypeError):
        s = Strategy()

def test_strategy_concrete():
    s = TrendFollowingSkeletonStrategy()
    assert s.metadata.name == "trend_following_skeleton"
    assert s.parameter_schema.strategy_name == "trend_following_skeleton"
    assert "close_ema_20" in s.required_features()
    s.assert_no_execution() # should not raise

    frame = StrategyFeatureFrame("AAPL", "1d", [{"close_ema_20": 10, "close_ema_50": 5}], ["close_ema_20", "close_ema_50"])
    batch = StrategyInputBatch([frame], "test", ["AAPL"], ["1d"], "test")

    val = s.validate_input(batch)
    assert val[0].valid

    p = s.validate_params()
    assert "fast_ema_col" in p
