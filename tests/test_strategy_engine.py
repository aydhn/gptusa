import pytest
from usa_signal_bot.strategies.strategy_engine import StrategyEngine
from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
from usa_signal_bot.strategies.strategy_input import StrategyInputBatch, StrategyFeatureFrame

def test_strategy_engine_run():
    r = create_default_strategy_registry()
    e = StrategyEngine(r, None)

    frame = StrategyFeatureFrame("AAPL", "1d", [{"close_ema_20": 105, "close_ema_50": 100}], ["close_ema_20", "close_ema_50"])
    batch = StrategyInputBatch([frame], "test", ["AAPL"], ["1d"], "test")

    res = e.run_strategy("trend_following_skeleton", batch)
    assert res.status.value == "COMPLETED"
    assert len(res.signals) == 1
    assert res.signals[0].symbol == "AAPL"

def test_strategy_engine_unknown_strategy():
    r = create_default_strategy_registry()
    e = StrategyEngine(r, None)

    batch = StrategyInputBatch([], "test", [], [], "test")
    res = e.run_strategy("unknown", batch)
    assert res.status.value == "FAILED"
    assert len(res.errors) > 0
