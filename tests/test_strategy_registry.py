import pytest
from usa_signal_bot.strategies.strategy_registry import StrategyRegistry, create_default_strategy_registry
from usa_signal_bot.strategies.example_strategies import TrendFollowingSkeletonStrategy
from usa_signal_bot.core.exceptions import StrategyRegistrationError
from usa_signal_bot.core.enums import StrategyCategory

def test_strategy_registry_default():
    r = create_default_strategy_registry()
    assert r.has("trend_following_skeleton")
    assert r.has("mean_reversion_skeleton")
    assert r.has("momentum_skeleton")
    assert r.has("volatility_breakout_skeleton")

    names = r.list_names()
    assert len(names) == 4

    tf = r.list_by_category(StrategyCategory.TREND_FOLLOWING)
    assert len(tf) == 1

    r.validate_all() # should not raise

def test_strategy_registry_duplicate():
    r = StrategyRegistry()
    r.register(TrendFollowingSkeletonStrategy())
    with pytest.raises(StrategyRegistrationError):
        r.register(TrendFollowingSkeletonStrategy())

def test_strategy_registry_unknown():
    r = StrategyRegistry()
    with pytest.raises(StrategyRegistrationError):
        r.get("unknown")

def test_strategy_registry_unregister():
    r = StrategyRegistry()
    r.register(TrendFollowingSkeletonStrategy())
    assert r.has("trend_following_skeleton")
    r.unregister("trend_following_skeleton")
    assert not r.has("trend_following_skeleton")
