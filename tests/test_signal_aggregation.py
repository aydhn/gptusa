import pytest
from datetime import datetime, timezone
import json
from pathlib import Path

from usa_signal_bot.strategies.signal_aggregation import (
    SignalCollapseMode, build_signal_group_key, detect_group_conflict,
    select_best_ranked_signal, aggregate_signals, collapse_ranked_signals,
    aggregation_report_to_text, write_signal_aggregation_report_json
)
from usa_signal_bot.strategies.signal_ranking import RankedSignal, SignalRankingStatus
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket, SignalLifecycleStatus

def _make_signal(sid, sym, tf, act):
    return StrategySignal(
        signal_id=sid, strategy_name="test", symbol=sym, timeframe=tf,
        timestamp_utc=datetime.now(timezone.utc).isoformat(), action=act,
        confidence=0.9, confidence_bucket=SignalConfidenceBucket.HIGH, score=90.0,
        reasons=[], feature_snapshot={}, risk_flags=[], lifecycle_status=SignalLifecycleStatus.CREATED
    )

def _make_ranked(sig, score):
    return RankedSignal(
        signal=sig, rank_score=score, rank=1,
        ranking_status=SignalRankingStatus.RANKED,
        components={}, penalties={}, bonuses={}, ranking_notes=[],
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

def test_build_signal_group_key():
    sig = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    assert build_signal_group_key(sig, SignalCollapseMode.BEST_PER_SYMBOL_TIMEFRAME) == "AAPL_1d"
    assert build_signal_group_key(sig, SignalCollapseMode.BEST_PER_SYMBOL) == "AAPL"

def test_detect_group_conflict():
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    sig2 = _make_signal("s2", "AAPL", "1d", SignalAction.SHORT)
    assert detect_group_conflict([sig1, sig2]) == True
    assert detect_group_conflict([sig1, sig1]) == False

def test_select_best_ranked_signal():
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    rs1 = _make_ranked(sig1, 50.0)
    rs2 = _make_ranked(sig1, 60.0)
    best = select_best_ranked_signal([rs1, rs2])
    assert best.rank_score == 60.0

def test_aggregate_signals():
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    sig2 = _make_signal("s2", "AAPL", "1d", SignalAction.LONG)
    rs1 = _make_ranked(sig1, 50.0)
    rs2 = _make_ranked(sig2, 60.0)

    report = aggregate_signals([sig1, sig2], [rs1, rs2], SignalCollapseMode.BEST_PER_SYMBOL_TIMEFRAME)
    assert report.total_groups == 1
    assert report.groups[0].group_key == "AAPL_1d"
    assert report.groups[0].max_rank_score == 60.0

def test_aggregate_best_per_symbol():
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    sig2 = _make_signal("s2", "AAPL", "1wk", SignalAction.LONG)
    rs1 = _make_ranked(sig1, 50.0)
    rs2 = _make_ranked(sig2, 60.0)

    report = aggregate_signals([sig1, sig2], [rs1, rs2], SignalCollapseMode.BEST_PER_SYMBOL)
    assert report.total_groups == 1
    assert report.groups[0].group_key == "AAPL"

def test_collapse_ranked_signals():
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    sig2 = _make_signal("s2", "AAPL", "1d", SignalAction.LONG)
    rs1 = _make_ranked(sig1, 50.0)
    rs2 = _make_ranked(sig2, 60.0)

    report = aggregate_signals([sig1, sig2], [rs1, rs2], SignalCollapseMode.BEST_PER_SYMBOL_TIMEFRAME)
    collapsed = collapse_ranked_signals(report)
    assert len(collapsed) == 1
    assert collapsed[0].rank_score == 60.0

def test_aggregation_report_to_text():
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    report = aggregate_signals([sig1], [_make_ranked(sig1, 50.0)])
    text = aggregation_report_to_text(report)
    assert "Signal Aggregation Report" in text

def test_write_signal_aggregation_report_json(tmp_path):
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    report = aggregate_signals([sig1], [_make_ranked(sig1, 50.0)])
    path = tmp_path / "agg.json"
    write_signal_aggregation_report_json(path, report)
    assert path.exists()
    with open(path) as f:
        data = json.load(f)
        assert data["total_input_signals"] == 1
