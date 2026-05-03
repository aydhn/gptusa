"""Signal aggregation and collapse system."""

import datetime
import uuid
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import SignalCollapseMode, SignalAction
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.strategies.signal_ranking import RankedSignal
from usa_signal_bot.core.exceptions import SignalAggregationError

@dataclass
class AggregatedSignalGroup:
    group_key: str
    symbol: str
    timeframe: Optional[str]
    signals: List[StrategySignal]
    ranked_signals: List[RankedSignal]
    best_signal_id: Optional[str]
    average_rank_score: Optional[float]
    max_rank_score: Optional[float]
    actions: Dict[str, int]
    strategies: List[str]
    conflicted: bool
    warnings: List[str] = field(default_factory=list)

@dataclass
class SignalAggregationReport:
    report_id: str
    created_at_utc: str
    collapse_mode: SignalCollapseMode
    total_input_signals: int
    total_groups: int
    conflicted_groups: int
    groups: List[AggregatedSignalGroup]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def build_signal_group_key(signal: StrategySignal, collapse_mode: SignalCollapseMode) -> str:
    if collapse_mode == SignalCollapseMode.BEST_PER_SYMBOL_TIMEFRAME or collapse_mode == SignalCollapseMode.MERGE_BY_SYMBOL_TIMEFRAME:
        return f"{signal.symbol}_{signal.timeframe}"
    elif collapse_mode == SignalCollapseMode.BEST_PER_SYMBOL:
        return signal.symbol
    else:
        return f"{signal.signal_id}"

def detect_group_conflict(signals: List[StrategySignal]) -> bool:
    actions = set(s.action for s in signals if s.action in [SignalAction.LONG, SignalAction.SHORT])
    return len(actions) > 1

def select_best_ranked_signal(ranked_signals: List[RankedSignal]) -> Optional[RankedSignal]:
    if not ranked_signals:
        return None
    sorted_rs = sorted(ranked_signals, key=lambda x: x.rank_score, reverse=True)
    return sorted_rs[0]

def aggregate_signals(signals: List[StrategySignal], ranked_signals: Optional[List[RankedSignal]] = None, collapse_mode: SignalCollapseMode = SignalCollapseMode.BEST_PER_SYMBOL_TIMEFRAME) -> SignalAggregationReport:
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report_id = f"agg_{uuid.uuid4().hex[:8]}"

    if ranked_signals is None:
        ranked_signals = []

    signal_map = {s.signal_id: s for s in signals}
    ranked_map = {rs.signal.signal_id: rs for rs in ranked_signals}

    if ranked_signals:
        for rs in ranked_signals:
            if rs.signal.signal_id not in signal_map:
                signal_map[rs.signal.signal_id] = rs.signal

    groups: Dict[str, AggregatedSignalGroup] = {}
    warnings = []

    if collapse_mode == SignalCollapseMode.KEEP_ALL:
        for sig in signal_map.values():
            key = build_signal_group_key(sig, collapse_mode)
            rs = ranked_map.get(sig.signal_id)

            groups[key] = AggregatedSignalGroup(
                group_key=key,
                symbol=sig.symbol,
                timeframe=sig.timeframe,
                signals=[sig],
                ranked_signals=[rs] if rs else [],
                best_signal_id=sig.signal_id,
                average_rank_score=rs.rank_score if rs else None,
                max_rank_score=rs.rank_score if rs else None,
                actions={sig.action.value: 1},
                strategies=[sig.strategy_name],
                conflicted=False
            )
    else:
        for sig in signal_map.values():
            key = build_signal_group_key(sig, collapse_mode)
            rs = ranked_map.get(sig.signal_id)

            if key not in groups:
                groups[key] = AggregatedSignalGroup(
                    group_key=key,
                    symbol=sig.symbol,
                    timeframe=sig.timeframe if collapse_mode != SignalCollapseMode.BEST_PER_SYMBOL else None,
                    signals=[],
                    ranked_signals=[],
                    best_signal_id=None,
                    average_rank_score=None,
                    max_rank_score=None,
                    actions={},
                    strategies=[],
                    conflicted=False
                )

            groups[key].signals.append(sig)
            if rs:
                groups[key].ranked_signals.append(rs)

            action_val = sig.action.value
            groups[key].actions[action_val] = groups[key].actions.get(action_val, 0) + 1

            if sig.strategy_name not in groups[key].strategies:
                groups[key].strategies.append(sig.strategy_name)

        for key, group in groups.items():
            group.conflicted = detect_group_conflict(group.signals)
            if group.conflicted:
                group.warnings.append("Conflicting LONG/SHORT signals detected in group.")

            if group.ranked_signals:
                best_rs = select_best_ranked_signal(group.ranked_signals)
                group.best_signal_id = best_rs.signal.signal_id if best_rs else None
                group.max_rank_score = best_rs.rank_score if best_rs else None
                group.average_rank_score = sum(rs.rank_score for rs in group.ranked_signals) / len(group.ranked_signals)
            else:
                group.best_signal_id = group.signals[0].signal_id if group.signals else None

    conflicted_count = sum(1 for g in groups.values() if g.conflicted)

    return SignalAggregationReport(
        report_id=report_id,
        created_at_utc=now_utc,
        collapse_mode=collapse_mode,
        total_input_signals=len(signal_map),
        total_groups=len(groups),
        conflicted_groups=conflicted_count,
        groups=list(groups.values()),
        warnings=warnings
    )

def collapse_ranked_signals(report: SignalAggregationReport) -> List[RankedSignal]:
    collapsed = []

    if report.collapse_mode == SignalCollapseMode.KEEP_ALL:
        for group in report.groups:
            collapsed.extend(group.ranked_signals)
    else:
        for group in report.groups:
            best_rs = select_best_ranked_signal(group.ranked_signals)
            if best_rs:
                collapsed.append(best_rs)

    return collapsed

def aggregation_report_to_text(report: SignalAggregationReport, limit: int = 20) -> str:
    lines = [
        f"--- Signal Aggregation Report ({report.report_id}) ---",
        f"Mode: {report.collapse_mode.value}",
        f"Input Signals: {report.total_input_signals} | Groups: {report.total_groups} | Conflicted: {report.conflicted_groups}",
        ""
    ]

    if report.warnings:
        lines.append("WARNINGS:")
        for w in report.warnings:
            lines.append(f"  - {w}")
        lines.append("")

    lines.append(f"Top {limit} Groups:")

    sorted_groups = sorted(report.groups, key=lambda g: g.max_rank_score or 0.0, reverse=True)

    for i, g in enumerate(sorted_groups[:limit]):
        actions_str = ", ".join(f"{k}:{v}" for k,v in g.actions.items())
        score_str = f"{g.max_rank_score:.2f}" if g.max_rank_score else "N/A"
        lines.append(f"  {i+1}. {g.group_key} - Max Score: {score_str} | Actions: [{actions_str}] | Strategies: {len(g.strategies)}")

    return "\n".join(lines)

def write_signal_aggregation_report_json(path: Path, report: SignalAggregationReport) -> Path:
    from usa_signal_bot.core.serialization import serialize_value
    path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "collapse_mode": report.collapse_mode.value,
        "total_input_signals": report.total_input_signals,
        "total_groups": report.total_groups,
        "conflicted_groups": report.conflicted_groups,
        "warnings": report.warnings,
        "errors": report.errors,
        "groups": []
    }

    for g in report.groups:
        group_data = {
            "group_key": g.group_key,
            "symbol": g.symbol,
            "timeframe": g.timeframe,
            "best_signal_id": g.best_signal_id,
            "average_rank_score": g.average_rank_score,
            "max_rank_score": g.max_rank_score,
            "actions": g.actions,
            "strategies": g.strategies,
            "conflicted": g.conflicted,
            "warnings": g.warnings
        }
        data["groups"].append(group_data)

    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=serialize_value)

    return path
