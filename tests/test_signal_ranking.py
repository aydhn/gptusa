import pytest
from datetime import datetime, timezone
from usa_signal_bot.strategies.signal_ranking import (
    SignalRankingConfig, default_signal_ranking_config, validate_signal_ranking_config,
    action_priority_score, quality_status_score, recency_score, risk_penalty_score,
    rank_signal, rank_signals, filter_ranked_signals, ranking_report_to_text
)
from usa_signal_bot.core.exceptions import SignalRankingError
from usa_signal_bot.core.enums import SignalAction, SignalQualityStatus, SignalRiskFlag, SignalConfidenceBucket, SignalLifecycleStatus, SignalRankingStatus
from usa_signal_bot.strategies.signal_contract import StrategySignal

def test_default_config_valid():
    config = default_signal_ranking_config()
    validate_signal_ranking_config(config)

def test_invalid_config():
    config = SignalRankingConfig(min_rank_score=101.0)
    with pytest.raises(SignalRankingError):
        validate_signal_ranking_config(config)

def test_action_priority_score():
    assert action_priority_score(SignalAction.LONG) == 1.0
    assert action_priority_score(SignalAction.SHORT) == 0.8
    assert action_priority_score(SignalAction.WATCH) == 0.5
    assert action_priority_score(SignalAction.FLAT) == 0.0

def test_quality_status_score():
    assert quality_status_score(SignalQualityStatus.ACCEPTED) == 1.0
    assert quality_status_score(SignalQualityStatus.WARNING) == 0.6
    assert quality_status_score(SignalQualityStatus.REJECTED) == 0.0

def test_recency_score():
    now_utc = datetime.now(timezone.utc).isoformat()
    assert recency_score(now_utc, now_utc) == 100.0

def test_risk_penalty_score():
    assert risk_penalty_score([]) == 0.0
    assert risk_penalty_score([SignalRiskFlag.HIGH_VOLATILITY]) == 0.4

def test_rank_signal():
    now_utc = datetime.now(timezone.utc).isoformat()
    sig = StrategySignal(
        signal_id="test1", strategy_name="test", symbol="AAPL", timeframe="1d",
        timestamp_utc=now_utc, action=SignalAction.LONG,
        confidence=0.9, confidence_bucket=SignalConfidenceBucket.HIGH, score=90.0,
        reasons=[], feature_snapshot={}, risk_flags=[], lifecycle_status=SignalLifecycleStatus.CREATED,
        quality_status=SignalQualityStatus.ACCEPTED, confluence_score=80.0
    )
    ranked = rank_signal(sig)
    assert ranked.rank_score > 0
    assert ranked.ranking_status == SignalRankingStatus.RANKED
    assert ranked.rank_score <= default_signal_ranking_config().max_rank_score_without_backtest

def test_rank_signals():
    now_utc = datetime.now(timezone.utc).isoformat()
    sig1 = StrategySignal(
        signal_id="test1", strategy_name="test", symbol="AAPL", timeframe="1d",
        timestamp_utc=now_utc, action=SignalAction.LONG,
        confidence=0.9, confidence_bucket=SignalConfidenceBucket.HIGH, score=90.0,
        reasons=[], feature_snapshot={}, risk_flags=[], lifecycle_status=SignalLifecycleStatus.CREATED,
        quality_status=SignalQualityStatus.ACCEPTED, confluence_score=80.0
    )
    report = rank_signals([sig1])
    assert report.total_signals == 1
    assert report.ranked_count == 1
    assert report.ranked_signals[0].rank == 1

def test_filter_ranked_signals():
    now_utc = datetime.now(timezone.utc).isoformat()
    sig1 = StrategySignal(
        signal_id="test1", strategy_name="test", symbol="AAPL", timeframe="1d",
        timestamp_utc=now_utc, action=SignalAction.LONG,
        confidence=0.1, confidence_bucket=SignalConfidenceBucket.LOW, score=10.0,
        reasons=[], feature_snapshot={}, risk_flags=[], lifecycle_status=SignalLifecycleStatus.CREATED,
        quality_status=SignalQualityStatus.REJECTED, confluence_score=10.0
    )
    report = rank_signals([sig1])
    filtered_report = filter_ranked_signals(report, min_rank_score=90.0)
    assert filtered_report.filtered_count == 1
    assert filtered_report.ranked_count == 0

def test_ranking_report_to_text():
    now_utc = datetime.now(timezone.utc).isoformat()
    sig1 = StrategySignal(
        signal_id="test1", strategy_name="test", symbol="AAPL", timeframe="1d",
        timestamp_utc=now_utc, action=SignalAction.LONG,
        confidence=0.9, confidence_bucket=SignalConfidenceBucket.HIGH, score=90.0,
        reasons=[], feature_snapshot={}, risk_flags=[], lifecycle_status=SignalLifecycleStatus.CREATED,
        quality_status=SignalQualityStatus.ACCEPTED, confluence_score=80.0
    )
    report = rank_signals([sig1])
    text = ranking_report_to_text(report)
    assert "Signal Ranking Report" in text
    assert "Total Signals: 1" in text
