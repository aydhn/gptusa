"""Signal ranking system."""

import datetime
import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

from usa_signal_bot.core.enums import SignalRankingStatus, SignalAction, SignalQualityStatus, SignalRiskFlag
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.exceptions import SignalRankingError

@dataclass
class SignalRankingConfig:
    min_rank_score: float = 0.0
    max_rank_score: float = 100.0
    signal_score_weight: float = 35.0
    confidence_weight: float = 15.0
    confluence_weight: float = 20.0
    quality_weight: float = 15.0
    recency_weight: float = 5.0
    risk_penalty_weight: float = 20.0
    action_priority_weight: float = 10.0
    max_rank_score_without_backtest: float = 75.0

def default_signal_ranking_config() -> SignalRankingConfig:
    return SignalRankingConfig()

def validate_signal_ranking_config(config: SignalRankingConfig) -> None:
    if not (0.0 <= config.min_rank_score <= 100.0):
        raise SignalRankingError("min_rank_score must be between 0 and 100.")
    if not (0.0 <= config.max_rank_score <= 100.0):
        raise SignalRankingError("max_rank_score must be between 0 and 100.")
    if config.min_rank_score > config.max_rank_score:
        raise SignalRankingError("min_rank_score cannot be greater than max_rank_score.")
    if config.max_rank_score_without_backtest > 75.0:
        raise SignalRankingError("max_rank_score_without_backtest cannot be greater than 75.0.")
    if any(w < 0 for w in [
        config.signal_score_weight, config.confidence_weight,
        config.confluence_weight, config.quality_weight,
        config.recency_weight, config.risk_penalty_weight,
        config.action_priority_weight
    ]):
        raise SignalRankingError("Weights cannot be negative.")

@dataclass
class RankedSignal:
    signal: StrategySignal
    rank_score: float
    rank: Optional[int]
    ranking_status: SignalRankingStatus
    components: Dict[str, float]
    penalties: Dict[str, float]
    bonuses: Dict[str, float]
    ranking_notes: List[str]
    created_at_utc: str

@dataclass
class SignalRankingReport:
    report_id: str
    created_at_utc: str
    total_signals: int
    ranked_count: int
    filtered_count: int
    top_rank_score: Optional[float]
    average_rank_score: Optional[float]
    ranked_signals: List[RankedSignal]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def action_priority_score(action: SignalAction) -> float:
    if action == SignalAction.LONG:
        return 1.0
    elif action == SignalAction.SHORT:
        return 0.8
    elif action == SignalAction.WATCH:
        return 0.5
    else:
        return 0.0

def quality_status_score(status: Optional[SignalQualityStatus]) -> float:
    if status == SignalQualityStatus.ACCEPTED:
        return 1.0
    elif status == SignalQualityStatus.WARNING:
        return 0.6
    elif status == SignalQualityStatus.REJECTED:
        return 0.0
    else:
        return 0.5

def recency_score(timestamp_utc: str, now_utc: Optional[str] = None) -> float:
    try:
        if now_utc is None:
            now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        signal_time = datetime.datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
        now_time = datetime.datetime.fromisoformat(now_utc.replace("Z", "+00:00"))

        diff_hours = (now_time - signal_time).total_seconds() / 3600.0

        if diff_hours < 0:
            diff_hours = 0

        score = max(0.0, 100.0 - (diff_hours * 1.5))
        return min(100.0, score)
    except Exception:
        return 50.0

def risk_penalty_score(flags: List[SignalRiskFlag]) -> float:
    if not flags:
        return 0.0

    score = 0.0
    for flag in flags:
        if flag in [SignalRiskFlag.HIGH_VOLATILITY, SignalRiskFlag.LOW_LIQUIDITY]:
            score += 0.4
        elif flag in [SignalRiskFlag.DATA_QUALITY_WARNING, SignalRiskFlag.CONFLICTING_FEATURES]:
            score += 0.2
        else:
            score += 0.1

    return min(1.0, score)

def calculate_rank_score(signal: StrategySignal, config: SignalRankingConfig) -> Tuple[float, Dict[str, float], Dict[str, float], Dict[str, float]]:
    components = {}
    penalties = {}
    bonuses = {}

    components["SIGNAL_SCORE"] = signal.score * (config.signal_score_weight / 100.0)
    components["CONFIDENCE"] = (signal.confidence * 100.0) * (config.confidence_weight / 100.0)

    confluence = signal.confluence_score if signal.confluence_score is not None else 50.0
    components["CONFLUENCE"] = confluence * (config.confluence_weight / 100.0)

    q_score = quality_status_score(signal.quality_status) * 100.0
    components["QUALITY"] = q_score * (config.quality_weight / 100.0)

    r_score = recency_score(signal.timestamp_utc)
    components["RECENCY"] = r_score * (config.recency_weight / 100.0)

    a_score = action_priority_score(signal.action) * 100.0
    components["ACTION_PRIORITY"] = a_score * (config.action_priority_weight / 100.0)

    total_weights = (config.signal_score_weight + config.confidence_weight +
                     config.confluence_weight + config.quality_weight +
                     config.recency_weight + config.action_priority_weight)

    raw_score = sum(components.values())

    if total_weights > 0:
        raw_score = (raw_score / total_weights) * 100.0

    risk_factor = risk_penalty_score(signal.risk_flags)
    penalty_value = raw_score * risk_factor * (config.risk_penalty_weight / 100.0)
    if penalty_value > 0:
        penalties["RISK_PENALTY"] = penalty_value

    final_score = raw_score - penalty_value

    if signal.quality_status == SignalQualityStatus.REJECTED:
        final_score = min(final_score, 20.0)

    final_score = min(final_score, config.max_rank_score_without_backtest)
    final_score = max(0.0, final_score)

    return final_score, components, penalties, bonuses

def rank_signal(signal: StrategySignal, config: Optional[SignalRankingConfig] = None) -> RankedSignal:
    if config is None:
        config = default_signal_ranking_config()

    validate_signal_ranking_config(config)

    score, components, penalties, bonuses = calculate_rank_score(signal, config)

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

    status = SignalRankingStatus.RANKED
    notes = []

    if score < config.min_rank_score:
        status = SignalRankingStatus.FILTERED
        notes.append(f"Score {score:.2f} below min_rank_score {config.min_rank_score}")

    return RankedSignal(
        signal=signal,
        rank_score=score,
        rank=None,
        ranking_status=status,
        components=components,
        penalties=penalties,
        bonuses=bonuses,
        ranking_notes=notes,
        created_at_utc=now_utc
    )

def rank_signals(signals: List[StrategySignal], config: Optional[SignalRankingConfig] = None) -> SignalRankingReport:
    if config is None:
        config = default_signal_ranking_config()

    validate_signal_ranking_config(config)

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report_id = f"rank_{uuid.uuid4().hex[:8]}"

    ranked_signals = []
    filtered_count = 0
    warnings = []

    for sig in signals:
        try:
            ranked = rank_signal(sig, config)
            if ranked.ranking_status == SignalRankingStatus.FILTERED:
                filtered_count += 1
            ranked_signals.append(ranked)
        except Exception as e:
            warnings.append(f"Failed to rank signal {sig.signal_id}: {str(e)}")

    ranked_signals = assign_ranks(ranked_signals)

    ranked_only = [rs for rs in ranked_signals if rs.ranking_status != SignalRankingStatus.FILTERED]
    top_score = ranked_only[0].rank_score if ranked_only else None
    avg_score = sum(rs.rank_score for rs in ranked_only) / len(ranked_only) if ranked_only else None

    return SignalRankingReport(
        report_id=report_id,
        created_at_utc=now_utc,
        total_signals=len(signals),
        ranked_count=len(ranked_only),
        filtered_count=filtered_count,
        top_rank_score=top_score,
        average_rank_score=avg_score,
        ranked_signals=ranked_signals,
        warnings=warnings
    )

def assign_ranks(ranked_signals: List[RankedSignal]) -> List[RankedSignal]:
    sorted_signals = sorted(ranked_signals, key=lambda x: x.rank_score, reverse=True)

    current_rank = 1
    for rs in sorted_signals:
        if rs.ranking_status != SignalRankingStatus.FILTERED:
            rs.rank = current_rank
            current_rank += 1
        else:
            rs.rank = None

    return sorted_signals

def filter_ranked_signals(report: SignalRankingReport, min_rank_score: float) -> SignalRankingReport:
    for rs in report.ranked_signals:
        if rs.rank_score < min_rank_score and rs.ranking_status != SignalRankingStatus.FILTERED:
            rs.ranking_status = SignalRankingStatus.FILTERED
            rs.rank = None
            rs.ranking_notes.append(f"Post-filtered due to min_rank_score {min_rank_score}")

    report.ranked_signals = assign_ranks(report.ranked_signals)

    ranked_only = [rs for rs in report.ranked_signals if rs.ranking_status != SignalRankingStatus.FILTERED]

    report.ranked_count = len(ranked_only)
    report.filtered_count = report.total_signals - report.ranked_count
    report.top_rank_score = ranked_only[0].rank_score if ranked_only else None
    report.average_rank_score = sum(rs.rank_score for rs in ranked_only) / len(ranked_only) if ranked_only else None

    return report

def ranking_report_to_text(report: SignalRankingReport, limit: int = 20) -> str:
    lines = [
        f"--- Signal Ranking Report ({report.report_id}) ---",
        f"Total Signals: {report.total_signals} | Ranked: {report.ranked_count} | Filtered: {report.filtered_count}",
        f"Top Score: {report.top_rank_score:.2f} | Average Score: {report.average_rank_score:.2f}" if report.top_rank_score else "No signals ranked.",
        ""
    ]

    if report.warnings:
        lines.append("WARNINGS:")
        for w in report.warnings:
            lines.append(f"  - {w}")
        lines.append("")

    ranked_only = [rs for rs in report.ranked_signals if rs.ranking_status != SignalRankingStatus.FILTERED]

    if ranked_only:
        lines.append(f"Top {limit} Ranked Signals:")
        for i, rs in enumerate(ranked_only[:limit]):
            lines.append(f"  {rs.rank}. {rs.signal.symbol} [{rs.signal.timeframe}] {rs.signal.action.value} - Score: {rs.rank_score:.2f} (Str: {rs.signal.strategy_name})")

    return "\n".join(lines)
