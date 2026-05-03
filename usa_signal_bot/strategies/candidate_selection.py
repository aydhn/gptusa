"""Candidate selection system."""

import datetime
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

from usa_signal_bot.core.enums import (
    CandidateSelectionStatus, CandidateRejectionReason, SignalAction,
    SignalCollapseMode, SignalRiskFlag
)
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.signal_ranking import RankedSignal, SignalRankingReport
from usa_signal_bot.core.exceptions import CandidateSelectionError

@dataclass
class CandidateSelectionConfig:
    max_candidates: int = 20
    max_candidates_per_symbol: int = 1
    max_candidates_per_strategy: int = 10
    min_rank_score: float = 45.0
    min_confidence: float = 0.25
    min_confluence_score: Optional[float] = None
    allow_watch_action: bool = True
    allow_long_action: bool = True
    allow_short_action: bool = False
    reject_high_risk_flags: bool = True
    collapse_mode: SignalCollapseMode = SignalCollapseMode.BEST_PER_SYMBOL_TIMEFRAME

def default_candidate_selection_config() -> CandidateSelectionConfig:
    return CandidateSelectionConfig()

def validate_candidate_selection_config(config: CandidateSelectionConfig) -> None:
    if config.max_candidates <= 0:
        raise CandidateSelectionError("max_candidates must be positive.")
    if config.max_candidates_per_symbol <= 0:
        raise CandidateSelectionError("max_candidates_per_symbol must be positive.")
    if config.max_candidates_per_strategy <= 0:
        raise CandidateSelectionError("max_candidates_per_strategy must be positive.")
    if not (0.0 <= config.min_rank_score <= 100.0):
        raise CandidateSelectionError("min_rank_score must be between 0 and 100.")
    if not (0.0 <= config.min_confidence <= 1.0):
        raise CandidateSelectionError("min_confidence must be between 0 and 1.")

@dataclass
class SelectedCandidate:
    candidate_id: str
    ranked_signal: RankedSignal
    selection_status: CandidateSelectionStatus
    rejection_reason: Optional[CandidateRejectionReason]
    selection_rank: Optional[int]
    notes: List[str]
    created_at_utc: str

@dataclass
class CandidateSelectionReport:
    report_id: str
    created_at_utc: str
    total_ranked_signals: int
    selected_count: int
    rejected_count: int
    watchlisted_count: int
    selected_candidates: List[SelectedCandidate]
    rejected_candidates: List[SelectedCandidate]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def candidate_id_from_signal(signal: StrategySignal) -> str:
    return f"cand_{signal.signal_id}"

def evaluate_candidate(ranked_signal: RankedSignal, config: CandidateSelectionConfig) -> SelectedCandidate:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cid = candidate_id_from_signal(ranked_signal.signal)

    sig = ranked_signal.signal
    notes = []

    if sig.action == SignalAction.SHORT and not config.allow_short_action:
        return SelectedCandidate(
            candidate_id=cid, ranked_signal=ranked_signal,
            selection_status=CandidateSelectionStatus.REJECTED,
            rejection_reason=CandidateRejectionReason.UNKNOWN,
            selection_rank=None, notes=["SHORT action not allowed"], created_at_utc=now_utc
        )

    if sig.action == SignalAction.LONG and not config.allow_long_action:
        return SelectedCandidate(
            candidate_id=cid, ranked_signal=ranked_signal,
            selection_status=CandidateSelectionStatus.REJECTED,
            rejection_reason=CandidateRejectionReason.UNKNOWN,
            selection_rank=None, notes=["LONG action not allowed"], created_at_utc=now_utc
        )

    if ranked_signal.rank_score < config.min_rank_score:
        return SelectedCandidate(
            candidate_id=cid, ranked_signal=ranked_signal,
            selection_status=CandidateSelectionStatus.REJECTED,
            rejection_reason=CandidateRejectionReason.LOW_RANK_SCORE,
            selection_rank=None, notes=[f"Rank score {ranked_signal.rank_score:.2f} < min {config.min_rank_score}"],
            created_at_utc=now_utc
        )

    if sig.confidence < config.min_confidence:
        return SelectedCandidate(
            candidate_id=cid, ranked_signal=ranked_signal,
            selection_status=CandidateSelectionStatus.REJECTED,
            rejection_reason=CandidateRejectionReason.LOW_CONFIDENCE,
            selection_rank=None, notes=[f"Confidence {sig.confidence:.2f} < min {config.min_confidence}"],
            created_at_utc=now_utc
        )

    if config.min_confluence_score is not None:
        c_score = sig.confluence_score if sig.confluence_score is not None else 0.0
        if c_score < config.min_confluence_score:
            return SelectedCandidate(
                candidate_id=cid, ranked_signal=ranked_signal,
                selection_status=CandidateSelectionStatus.REJECTED,
                rejection_reason=CandidateRejectionReason.LOW_CONFLUENCE,
                selection_rank=None, notes=[f"Confluence {c_score:.2f} < min {config.min_confluence_score}"],
                created_at_utc=now_utc
            )

    if config.reject_high_risk_flags and sig.risk_flags:
        return SelectedCandidate(
            candidate_id=cid, ranked_signal=ranked_signal,
            selection_status=CandidateSelectionStatus.REJECTED,
            rejection_reason=CandidateRejectionReason.HIGH_RISK_FLAGS,
            selection_rank=None, notes=[f"High risk flags present: {sig.risk_flags}"],
            created_at_utc=now_utc
        )

    status = CandidateSelectionStatus.WATCHLISTED if sig.action == SignalAction.WATCH else CandidateSelectionStatus.SELECTED

    return SelectedCandidate(
        candidate_id=cid, ranked_signal=ranked_signal,
        selection_status=status,
        rejection_reason=None,
        selection_rank=None,
        notes=["Passed evaluation"],
        created_at_utc=now_utc
    )

def enforce_candidate_limits(candidates: List[SelectedCandidate], config: CandidateSelectionConfig) -> Tuple[List[SelectedCandidate], List[SelectedCandidate]]:
    sorted_cands = sorted(candidates, key=lambda c: c.ranked_signal.rank_score, reverse=True)

    accepted = []
    rejected = []

    symbol_counts = {}
    strategy_counts = {}

    for cand in sorted_cands:
        sig = cand.ranked_signal.signal
        sym = sig.symbol
        strat = sig.strategy_name

        if len(accepted) >= config.max_candidates:
            cand.selection_status = CandidateSelectionStatus.REJECTED
            cand.rejection_reason = CandidateRejectionReason.UNKNOWN
            cand.notes.append(f"Global limit {config.max_candidates} reached")
            rejected.append(cand)
            continue

        if symbol_counts.get(sym, 0) >= config.max_candidates_per_symbol:
            cand.selection_status = CandidateSelectionStatus.REJECTED
            cand.rejection_reason = CandidateRejectionReason.TOO_MANY_PER_SYMBOL
            cand.notes.append(f"Symbol limit {config.max_candidates_per_symbol} reached for {sym}")
            rejected.append(cand)
            continue

        if strategy_counts.get(strat, 0) >= config.max_candidates_per_strategy:
            cand.selection_status = CandidateSelectionStatus.REJECTED
            cand.rejection_reason = CandidateRejectionReason.TOO_MANY_PER_STRATEGY
            cand.notes.append(f"Strategy limit {config.max_candidates_per_strategy} reached for {strat}")
            rejected.append(cand)
            continue

        symbol_counts[sym] = symbol_counts.get(sym, 0) + 1
        strategy_counts[strat] = strategy_counts.get(strat, 0) + 1
        cand.selection_rank = len(accepted) + 1
        accepted.append(cand)

    return accepted, rejected

def select_candidates(ranking_report: SignalRankingReport, config: Optional[CandidateSelectionConfig] = None) -> CandidateSelectionReport:
    if config is None:
        config = default_candidate_selection_config()

    validate_candidate_selection_config(config)

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report_id = f"sel_{uuid.uuid4().hex[:8]}"

    preliminary_selected = []
    rejected_candidates = []

    for rs in ranking_report.ranked_signals:
        if rs.ranking_status.value == "FILTERED":
            pass

        cand = evaluate_candidate(rs, config)
        if cand.selection_status == CandidateSelectionStatus.REJECTED:
            rejected_candidates.append(cand)
        else:
            preliminary_selected.append(cand)

    final_selected, limit_rejected = enforce_candidate_limits(preliminary_selected, config)
    rejected_candidates.extend(limit_rejected)

    watchlisted_count = sum(1 for c in final_selected if c.selection_status == CandidateSelectionStatus.WATCHLISTED)
    selected_count = len(final_selected) - watchlisted_count

    return CandidateSelectionReport(
        report_id=report_id,
        created_at_utc=now_utc,
        total_ranked_signals=len(ranking_report.ranked_signals),
        selected_count=selected_count,
        rejected_count=len(rejected_candidates),
        watchlisted_count=watchlisted_count,
        selected_candidates=final_selected,
        rejected_candidates=rejected_candidates
    )

def candidate_selection_report_to_text(report: CandidateSelectionReport, limit: int = 20) -> str:
    lines = [
        f"--- Candidate Selection Report ({report.report_id}) ---",
        f"Total Ranked: {report.total_ranked_signals} | Selected: {report.selected_count} | Watchlisted: {report.watchlisted_count} | Rejected: {report.rejected_count}",
        ""
    ]

    if report.warnings:
        lines.append("WARNINGS:")
        for w in report.warnings:
            lines.append(f"  - {w}")
        lines.append("")

    if report.selected_candidates:
        lines.append(f"Top {limit} Candidates:")
        for i, c in enumerate(report.selected_candidates[:limit]):
            rs = c.ranked_signal
            lines.append(f"  {c.selection_rank}. {rs.signal.symbol} [{rs.signal.timeframe}] {rs.signal.action.value} - Score: {rs.rank_score:.2f} ({c.selection_status.value})")

    return "\n".join(lines)

def get_selected_signals(report: CandidateSelectionReport) -> List[StrategySignal]:
    return [c.ranked_signal.signal for c in report.selected_candidates]

def get_selected_ranked_signals(report: CandidateSelectionReport) -> List[RankedSignal]:
    return [c.ranked_signal for c in report.selected_candidates]
