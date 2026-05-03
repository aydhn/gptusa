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

def test_score_and_validate_signals():
    from usa_signal_bot.strategies.signal_contract import StrategySignal
    from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket
    from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        engine = StrategyEngine(StrategyRegistry(), Path(tmp))

        sig = StrategySignal(
            signal_id="TEST-1", strategy_name="TEST_STRAT", symbol="AAPL", timeframe="1d",
            timestamp_utc="2024-01-01T00:00:00Z", action=SignalAction.LONG,
            confidence=0.8, confidence_bucket=SignalConfidenceBucket.HIGH,
            score=0.0, reasons=["Reason"], feature_snapshot={"k": 1}, risk_flags=[]
        )

        scored, scoring_results, quality_report = engine.score_and_validate_signals([sig])
        assert len(scored) == 1
        assert len(scoring_results) == 0 # Disabled by default unless config is passed
        assert len(quality_report.accepted_signal_ids) == 1

def test_run_strategies_with_confluence():
    from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
    from usa_signal_bot.strategies.strategy_input import StrategyInputBatch
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        engine = StrategyEngine(StrategyRegistry(), Path(tmp))

        # This will return empty since we don't have valid strategies registered here
        # But it should not crash
        import datetime
        batch = StrategyInputBatch("1d", ["1d"], datetime.datetime.now(datetime.timezone.utc).isoformat(), [], {})
        results, confluence = engine.run_strategies_with_confluence([], batch)
        assert len(results) == 0
        assert confluence.total_groups == 0

def test_run_strategies_ranked():
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_input import StrategyInputBatch
    from pathlib import Path

    registry = create_default_strategy_registry()
    engine = StrategyEngine(registry, Path("/tmp"))

    batch = StrategyInputBatch(provider_name="test", symbols=[], timeframes=[], created_at_utc="", frames=[]) # empty, but method should handle it gracefully
    res = engine.run_strategies_ranked(["trend_following_rule"], batch)

    assert res is not None
    assert hasattr(res, "portfolio_run")
    assert res.portfolio_run.signal_count == 0

def test_run_rule_strategy_set_ranked():
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_input import StrategyInputBatch
    from pathlib import Path

    registry = create_default_strategy_registry()
    engine = StrategyEngine(registry, Path("/tmp"))

    batch = StrategyInputBatch(provider_name="test", symbols=[], timeframes=[], created_at_utc="", frames=[]) # empty
    res = engine.run_rule_strategy_set_ranked("basic_rules", batch)

    assert res is not None
    assert hasattr(res, "portfolio_run")
    assert res.portfolio_run.signal_count == 0
