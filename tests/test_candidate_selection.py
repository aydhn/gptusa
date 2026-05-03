import pytest
from datetime import datetime, timezone

from usa_signal_bot.strategies.candidate_selection import (
    CandidateSelectionConfig, default_candidate_selection_config, validate_candidate_selection_config,
    evaluate_candidate, select_candidates, enforce_candidate_limits, get_selected_signals,
    candidate_selection_report_to_text, CandidateSelectionStatus, CandidateRejectionReason
)
from usa_signal_bot.strategies.signal_ranking import RankedSignal, SignalRankingStatus, SignalRankingReport
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket, SignalLifecycleStatus, SignalRiskFlag
from usa_signal_bot.core.exceptions import CandidateSelectionError

def _make_signal(sid, sym, tf, act, conf=0.9, risk_flags=None):
    if risk_flags is None:
        risk_flags = []
    return StrategySignal(
        signal_id=sid, strategy_name="test_strat", symbol=sym, timeframe=tf,
        timestamp_utc=datetime.now(timezone.utc).isoformat(), action=act,
        confidence=conf, confidence_bucket=SignalConfidenceBucket.HIGH, score=90.0,
        reasons=[], feature_snapshot={}, risk_flags=risk_flags, lifecycle_status=SignalLifecycleStatus.CREATED
    )

def _make_ranked(sig, score):
    return RankedSignal(
        signal=sig, rank_score=score, rank=1,
        ranking_status=SignalRankingStatus.RANKED,
        components={}, penalties={}, bonuses={}, ranking_notes=[],
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

def test_default_config_valid():
    config = default_candidate_selection_config()
    validate_candidate_selection_config(config)

def test_invalid_config():
    config = CandidateSelectionConfig(max_candidates=0)
    with pytest.raises(CandidateSelectionError):
        validate_candidate_selection_config(config)

def test_evaluate_candidate_low_rank():
    config = default_candidate_selection_config()
    sig = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    rs = _make_ranked(sig, 20.0)
    cand = evaluate_candidate(rs, config)
    assert cand.selection_status == CandidateSelectionStatus.REJECTED
    assert cand.rejection_reason == CandidateRejectionReason.LOW_RANK_SCORE

def test_evaluate_candidate_short_action_rejected():
    config = default_candidate_selection_config()
    sig = _make_signal("s1", "AAPL", "1d", SignalAction.SHORT)
    rs = _make_ranked(sig, 80.0)
    cand = evaluate_candidate(rs, config)
    assert cand.selection_status == CandidateSelectionStatus.REJECTED
    assert "SHORT action not allowed" in cand.notes[0]

def test_evaluate_candidate_high_risk():
    config = default_candidate_selection_config()
    sig = _make_signal("s1", "AAPL", "1d", SignalAction.LONG, risk_flags=[SignalRiskFlag.HIGH_VOLATILITY])
    rs = _make_ranked(sig, 80.0)
    cand = evaluate_candidate(rs, config)
    assert cand.selection_status == CandidateSelectionStatus.REJECTED
    assert cand.rejection_reason == CandidateRejectionReason.HIGH_RISK_FLAGS

def test_enforce_candidate_limits_symbol():
    config = default_candidate_selection_config()
    config.max_candidates_per_symbol = 1
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    sig2 = _make_signal("s2", "AAPL", "1d", SignalAction.LONG)
    rs1 = _make_ranked(sig1, 80.0)
    rs2 = _make_ranked(sig2, 90.0)

    cand1 = evaluate_candidate(rs1, config)
    cand2 = evaluate_candidate(rs2, config)

    accepted, rejected = enforce_candidate_limits([cand1, cand2], config)
    assert len(accepted) == 1
    assert len(rejected) == 1
    assert accepted[0].candidate_id == f"cand_{sig2.signal_id}"

def test_select_candidates():
    config = default_candidate_selection_config()
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    rs1 = _make_ranked(sig1, 80.0)
    report_in = SignalRankingReport(
        report_id="123", created_at_utc=datetime.now(timezone.utc).isoformat(),
        total_signals=1, ranked_count=1, filtered_count=0, top_rank_score=80.0,
        average_rank_score=80.0, ranked_signals=[rs1]
    )
    report_out = select_candidates(report_in, config)
    assert report_out.selected_count == 1
    assert report_out.rejected_count == 0

def test_get_selected_signals():
    config = default_candidate_selection_config()
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    rs1 = _make_ranked(sig1, 80.0)
    report_in = SignalRankingReport(
        report_id="123", created_at_utc=datetime.now(timezone.utc).isoformat(),
        total_signals=1, ranked_count=1, filtered_count=0, top_rank_score=80.0,
        average_rank_score=80.0, ranked_signals=[rs1]
    )
    report_out = select_candidates(report_in, config)
    sigs = get_selected_signals(report_out)
    assert len(sigs) == 1
    assert sigs[0].symbol == "AAPL"

def test_candidate_selection_report_to_text():
    config = default_candidate_selection_config()
    sig1 = _make_signal("s1", "AAPL", "1d", SignalAction.LONG)
    rs1 = _make_ranked(sig1, 80.0)
    report_in = SignalRankingReport(
        report_id="123", created_at_utc=datetime.now(timezone.utc).isoformat(),
        total_signals=1, ranked_count=1, filtered_count=0, top_rank_score=80.0,
        average_rank_score=80.0, ranked_signals=[rs1]
    )
    report_out = select_candidates(report_in, config)
    text = candidate_selection_report_to_text(report_out)
    assert "Candidate Selection Report" in text
