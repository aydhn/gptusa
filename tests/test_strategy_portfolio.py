import pytest
from datetime import datetime, timezone
import json

from usa_signal_bot.strategies.strategy_portfolio import (
    StrategyPortfolioConfig, default_strategy_portfolio_config, validate_strategy_portfolio_config,
    aggregate_strategy_portfolio_results, strategy_portfolio_result_to_text,
    write_strategy_portfolio_run_json, write_strategy_portfolio_result_json
)
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.strategy_models import StrategyRunResult
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket, SignalLifecycleStatus, SignalQualityStatus, StrategyRunStatus
from usa_signal_bot.core.exceptions import StrategyPortfolioError
from usa_signal_bot.strategies.signal_confluence import ConfluenceReport, ConfluenceGroupResult, ConfluenceDirection, ConfluenceStrength

def _make_signal(sid, sym, tf, act, strat="test"):
    return StrategySignal(
        signal_id=sid, strategy_name=strat, symbol=sym, timeframe=tf,
        timestamp_utc=datetime.now(timezone.utc).isoformat(), action=act,
        confidence=0.9, confidence_bucket=SignalConfidenceBucket.HIGH, score=90.0,
        reasons=[], feature_snapshot={}, risk_flags=[], lifecycle_status=SignalLifecycleStatus.CREATED,
        quality_status=SignalQualityStatus.ACCEPTED
    )

def test_default_config_valid():
    config = default_strategy_portfolio_config()
    validate_strategy_portfolio_config(config)

def test_invalid_config():
    config = StrategyPortfolioConfig(max_candidates=0)
    with pytest.raises(StrategyPortfolioError):
        validate_strategy_portfolio_config(config)

def test_aggregate_strategy_portfolio_results():
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG, "strat1")
    sig2 = _make_signal("s2", "MSFT", "1d", SignalAction.LONG, "strat2")

    res1 = StrategyRunResult(
        run_id="run1", strategy_name="strat1", status=StrategyRunStatus.COMPLETED,
        signals=[sig1], symbols_processed=["AAPL"], timeframes_processed=["1d"],
        warnings=[], errors=[], created_at_utc=""
    )
    res2 = StrategyRunResult(
        run_id="run2", strategy_name="strat2", status=StrategyRunStatus.COMPLETED,
        signals=[sig2], symbols_processed=["MSFT"], timeframes_processed=["1d"],
        warnings=[], errors=[], created_at_utc=""
    )

    cr = ConfluenceGroupResult(
        symbol="AAPL", timeframe="1d",
        direction=ConfluenceDirection.LONG_BIAS,
        strength=ConfluenceStrength.STRONG,
        confluence_score=85.0,
        signal_count=1,
        strategies=["strat1"],
        actions={},
        average_confidence=0.9,
        average_score=90.0,
        conflicting=False,
        reasons=[],
        signal_ids=[]
    )
    from usa_signal_bot.core.enums import SignalAggregationMode
    crep = ConfluenceReport(report_id="c1", created_at_utc="", aggregation_mode=SignalAggregationMode.BY_SYMBOL_TIMEFRAME, group_results=[cr], total_groups=1, conflicted_groups=0, strong_groups=1)

    agg = aggregate_strategy_portfolio_results([res1, res2], confluence_report=crep)

    assert agg.portfolio_run.signal_count == 2
    assert len(agg.selected_signals) > 0

    aapl_sig = next(s for s in agg.selected_signals if s.symbol == "AAPL")
    assert aapl_sig.confluence_score == 85.0

def test_strategy_portfolio_result_to_text():
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG, "strat1")
    res1 = StrategyRunResult(
        run_id="run1", strategy_name="strat1", status=StrategyRunStatus.COMPLETED,
        signals=[sig1], symbols_processed=["AAPL"], timeframes_processed=["1d"],
        warnings=[], errors=[], created_at_utc=""
    )
    agg = aggregate_strategy_portfolio_results([res1])
    text = strategy_portfolio_result_to_text(agg)
    assert "Strategy Portfolio Aggregation" in text

def test_write_strategy_portfolio_run_json(tmp_path):
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG, "strat1")
    res1 = StrategyRunResult(
        run_id="run1", strategy_name="strat1", status=StrategyRunStatus.COMPLETED,
        signals=[sig1], symbols_processed=["AAPL"], timeframes_processed=["1d"],
        warnings=[], errors=[], created_at_utc=""
    )
    agg = aggregate_strategy_portfolio_results([res1])

    path = tmp_path / "run.json"
    write_strategy_portfolio_run_json(path, agg.portfolio_run)
    assert path.exists()
    with open(path) as f:
        data = json.load(f)
        assert data["signal_count"] == 1

def test_write_strategy_portfolio_result_json(tmp_path):
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG, "strat1")
    res1 = StrategyRunResult(
        run_id="run1", strategy_name="strat1", status=StrategyRunStatus.COMPLETED,
        signals=[sig1], symbols_processed=["AAPL"], timeframes_processed=["1d"],
        warnings=[], errors=[], created_at_utc=""
    )
    agg = aggregate_strategy_portfolio_results([res1])

    path = tmp_path / "res.json"
    write_strategy_portfolio_result_json(path, agg)
    assert path.exists()
    with open(path) as f:
        data = json.load(f)
        assert "selected_candidates" in data
