import pytest
from usa_signal_bot.core.enums import SignalDriftStatus
from usa_signal_bot.comparison.signal_drift import (
    signal_snapshot_from_signal_record, signal_snapshot_from_candidate_record,
    compare_signal_snapshots, calculate_feature_gap_score,
    calculate_signal_drift_metrics, match_signal_snapshots,
    signal_drift_metrics_to_text
)

def test_snapshot_from_records():
    sig = {"symbol": "AAPL", "score": 0.8, "action": "buy"}
    snap1 = signal_snapshot_from_signal_record(sig)
    assert snap1.symbol == "AAPL"
    assert snap1.score == 0.8
    assert snap1.action == "buy"

    cand = {"symbol": "MSFT", "rank": 95.0, "direction": "sell"}
    snap2 = signal_snapshot_from_candidate_record(cand)
    assert snap2.symbol == "MSFT"
    assert snap2.rank_score == 95.0
    assert snap2.action == "sell"

def test_compare_snapshots():
    s1 = signal_snapshot_from_signal_record({"score": 0.8, "confidence": 0.9, "action": "buy", "features": {"f1": 10}})
    s2 = signal_snapshot_from_signal_record({"score": 0.7, "confidence": 0.9, "action": "buy", "features": {"f1": 9}})

    pair = compare_signal_snapshots(s1, s2)
    assert pair.score_gap == pytest.approx(0.1)
    assert pair.confidence_gap == 0.0
    assert pair.feature_gap_score == pytest.approx(0.1)
    assert not pair.changed_action

def test_changed_action_drift():
    s1 = signal_snapshot_from_signal_record({"action": "buy"})
    s2 = signal_snapshot_from_signal_record({"action": "sell"})
    pair = compare_signal_snapshots(s1, s2)
    assert pair.changed_action
    assert pair.drift_status == SignalDriftStatus.SEVERE_DRIFT

def test_drift_metrics():
    s1 = signal_snapshot_from_signal_record({"symbol": "AAPL", "action": "buy"})
    s2 = signal_snapshot_from_signal_record({"symbol": "AAPL", "action": "sell"})
    pairs = match_signal_snapshots([s1], [s2])
    metrics = calculate_signal_drift_metrics(pairs)

    assert metrics.compared_signal_count == 1
    assert metrics.changed_signal_count == 1
    assert metrics.drift_status == SignalDriftStatus.SEVERE_DRIFT

def test_text_output():
    metrics = calculate_signal_drift_metrics([])
    txt = signal_drift_metrics_to_text(metrics)
    assert "Compared: 0" in txt
