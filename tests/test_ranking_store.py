import pytest
from pathlib import Path
from datetime import datetime, timezone

from usa_signal_bot.strategies.ranking_store import (
    ranking_store_dir, build_ranking_report_path, build_candidate_selection_report_path,
    build_portfolio_report_path, write_ranking_report_json, read_ranking_report_json,
    write_candidate_selection_report_json, read_candidate_selection_report_json,
    write_selected_candidates_jsonl, read_selected_candidates_jsonl, list_ranking_outputs, ranking_store_summary
)
from usa_signal_bot.strategies.signal_ranking import SignalRankingReport, RankedSignal, SignalRankingStatus
from usa_signal_bot.strategies.candidate_selection import CandidateSelectionReport, SelectedCandidate, CandidateSelectionStatus, CandidateRejectionReason
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket, SignalLifecycleStatus, SignalQualityStatus

def _make_signal(sid, sym):
    return StrategySignal(
        signal_id=sid, strategy_name="test", symbol=sym, timeframe="1d",
        timestamp_utc=datetime.now(timezone.utc).isoformat(), action=SignalAction.LONG,
        confidence=0.9, confidence_bucket=SignalConfidenceBucket.HIGH, score=90.0,
        reasons=[], feature_snapshot={}, risk_flags=[], lifecycle_status=SignalLifecycleStatus.CREATED,
        quality_status=SignalQualityStatus.ACCEPTED
    )

def _make_ranked(sig, score):
    return RankedSignal(
        signal=sig, rank_score=score, rank=1,
        ranking_status=SignalRankingStatus.RANKED,
        components={}, penalties={}, bonuses={}, ranking_notes=[],
        created_at_utc=datetime.now(timezone.utc).isoformat()
    )

def test_paths(tmp_path):
    d = ranking_store_dir(tmp_path)
    assert d.exists()
    assert "ranking" in str(d)

    p1 = build_ranking_report_path(tmp_path, "123")
    assert p1.name == "ranking_123.json"

    p2 = build_candidate_selection_report_path(tmp_path, "123")
    assert p2.name == "selection_123.json"

    p3 = build_portfolio_report_path(tmp_path, "123")
    assert p3.name == "portfolio_123.json"

def test_write_read_ranking_report(tmp_path):
    sig = _make_signal("s1", "AAPL")
    rs = _make_ranked(sig, 80.0)
    rep = SignalRankingReport(
        report_id="r1", created_at_utc="", total_signals=1, ranked_count=1, filtered_count=0,
        top_rank_score=80.0, average_rank_score=80.0, ranked_signals=[rs]
    )
    p = build_ranking_report_path(tmp_path, "r1")
    write_ranking_report_json(p, rep)
    assert p.exists()
    data = read_ranking_report_json(p)
    assert data["report_id"] == "r1"
    assert data["ranked_signals"][0]["symbol"] == "AAPL"

def test_write_read_candidate_selection(tmp_path):
    sig = _make_signal("s1", "AAPL")
    rs = _make_ranked(sig, 80.0)
    cand = SelectedCandidate(
        candidate_id="c1", ranked_signal=rs, selection_status=CandidateSelectionStatus.SELECTED,
        rejection_reason=None, selection_rank=1, notes=[], created_at_utc=""
    )
    rep = CandidateSelectionReport(
        report_id="c1", created_at_utc="", total_ranked_signals=1, selected_count=1,
        rejected_count=0, watchlisted_count=0, selected_candidates=[cand], rejected_candidates=[]
    )
    p = build_candidate_selection_report_path(tmp_path, "c1")
    write_candidate_selection_report_json(p, rep)
    assert p.exists()
    data = read_candidate_selection_report_json(p)
    assert data["report_id"] == "c1"
    assert data["selected_candidates"][0]["symbol"] == "AAPL"

def test_write_read_candidates_jsonl(tmp_path):
    sig = _make_signal("s1", "AAPL")
    rs = _make_ranked(sig, 80.0)
    cand = SelectedCandidate(
        candidate_id="c1", ranked_signal=rs, selection_status=CandidateSelectionStatus.SELECTED,
        rejection_reason=None, selection_rank=1, notes=[], created_at_utc=""
    )

    from usa_signal_bot.strategies.ranking_store import build_selected_candidates_path
    p = build_selected_candidates_path(tmp_path, "c1")
    write_selected_candidates_jsonl(p, [cand])
    assert p.exists()

    cands = read_selected_candidates_jsonl(p)
    assert len(cands) == 1
    assert cands[0]["candidate_id"] == "c1"
    assert cands[0]["signal"]["symbol"] == "AAPL"

def test_ranking_store_summary(tmp_path):
    sig = _make_signal("s1", "AAPL")
    rs = _make_ranked(sig, 80.0)
    rep = SignalRankingReport(
        report_id="r1", created_at_utc="", total_signals=1, ranked_count=1, filtered_count=0,
        top_rank_score=80.0, average_rank_score=80.0, ranked_signals=[rs]
    )
    p = build_ranking_report_path(tmp_path, "r1")
    write_ranking_report_json(p, rep)

    summary = ranking_store_summary(tmp_path)
    assert summary["total_files"] == 1
    assert summary["ranking_reports"] == 1
    assert summary["selection_reports"] == 0
