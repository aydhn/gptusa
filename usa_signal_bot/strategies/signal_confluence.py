"""Confluence engine for multi-strategy signal aggregation."""

import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path

from usa_signal_bot.core.enums import SignalAction, SignalAggregationMode, ConfluenceDirection, ConfluenceStrength
from usa_signal_bot.core.config_schema import ConfluenceConfig
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.serialization import dataclass_to_json
from usa_signal_bot.core.exceptions import SignalConfluenceError

@dataclass
class ConfluenceGroupResult:
    symbol: str
    timeframe: Optional[str]
    direction: ConfluenceDirection
    strength: ConfluenceStrength
    confluence_score: float
    signal_count: int
    strategies: List[str]
    actions: Dict[str, int]
    average_confidence: Optional[float]
    average_score: Optional[float]
    conflicting: bool
    reasons: List[str]
    signal_ids: List[str]

@dataclass
class ConfluenceReport:
    report_id: str
    created_at_utc: str
    aggregation_mode: SignalAggregationMode
    group_results: List[ConfluenceGroupResult]
    total_groups: int
    conflicted_groups: int
    strong_groups: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def group_signals_for_confluence(
    signals: List[StrategySignal],
    mode: SignalAggregationMode = SignalAggregationMode.BY_SYMBOL_TIMEFRAME
) -> Dict[str, List[StrategySignal]]:
    groups: Dict[str, List[StrategySignal]] = {}

    for sig in signals:
        if mode == SignalAggregationMode.BY_SYMBOL_TIMEFRAME:
            key = f"{sig.symbol}_{sig.timeframe}"
        elif mode == SignalAggregationMode.BY_SYMBOL:
            key = sig.symbol
        elif mode == SignalAggregationMode.BY_STRATEGY:
            key = sig.strategy_name
        else: # GLOBAL
            key = "global"

        if key not in groups:
            groups[key] = []
        groups[key].append(sig)

    return groups

def detect_conflicting_signals(signals: List[StrategySignal]) -> bool:
    has_long = any(s.action == SignalAction.LONG for s in signals)
    has_short = any(s.action == SignalAction.SHORT for s in signals)
    return has_long and has_short

def classify_confluence_direction(signals: List[StrategySignal]) -> ConfluenceDirection:
    if not signals:
        return ConfluenceDirection.NONE

    if detect_conflicting_signals(signals):
        return ConfluenceDirection.CONFLICTED

    longs = sum(1 for s in signals if s.action == SignalAction.LONG)
    shorts = sum(1 for s in signals if s.action == SignalAction.SHORT)
    flats = sum(1 for s in signals if s.action == SignalAction.FLAT)
    watches = sum(1 for s in signals if s.action == SignalAction.WATCH)
    avoids = sum(1 for s in signals if s.action == SignalAction.AVOID)

    total = len(signals)

    if longs > 0 and longs > (total / 2):
        return ConfluenceDirection.LONG_BIAS
    if shorts > 0 and shorts > (total / 2):
        return ConfluenceDirection.SHORT_BIAS
    if watches > 0 and watches > (total / 2):
        return ConfluenceDirection.WATCH_BIAS
    if (flats + avoids) > 0 and (flats + avoids) > (total / 2):
        return ConfluenceDirection.FLAT_BIAS

    return ConfluenceDirection.MIXED

def calculate_confluence_score(signals: List[StrategySignal], config: Optional[ConfluenceConfig] = None) -> float:
    if not signals:
        return 0.0

    if config is None:
        config = ConfluenceConfig()

    if detect_conflicting_signals(signals):
        return max(0.0, 50.0 - config.conflict_penalty)

    # Simple scoring: more signals aligned = higher score.
    # Base confluence score depends on the number of aligning strategies and their confidences.
    action_counts = {}
    for s in signals:
        action = s.action
        action_counts[action] = action_counts.get(action, 0) + 1

    max_action_count = max(action_counts.values()) if action_counts else 0
    ratio = max_action_count / len(signals)

    # Weight by confidences
    avg_conf = sum(s.confidence for s in signals) / len(signals)

    # Scale: 2 signals aligned with 0.8 conf = ~60. 3 signals = ~80.
    base_score = min(100.0, (max_action_count * 25.0))
    score = base_score * ratio * avg_conf

    return max(0.0, min(100.0, score))

def classify_confluence_strength(score: float, signal_count: int, config: Optional[ConfluenceConfig] = None) -> ConfluenceStrength:
    if config is None:
        config = ConfluenceConfig()

    if signal_count < config.min_signals_for_confluence:
        return ConfluenceStrength.NONE

    if score >= config.strong_threshold:
        return ConfluenceStrength.STRONG
    elif score >= config.moderate_threshold:
        return ConfluenceStrength.MODERATE
    elif score >= config.weak_threshold:
        return ConfluenceStrength.WEAK
    else:
        return ConfluenceStrength.NONE

def evaluate_confluence_group(
    signals: List[StrategySignal],
    config: Optional[ConfluenceConfig] = None
) -> ConfluenceGroupResult:

    if not signals:
        raise SignalConfluenceError("Cannot evaluate empty signal group.")

    symbol = signals[0].symbol
    # Check if all timeframes match, else None
    timeframe = signals[0].timeframe if all(s.timeframe == signals[0].timeframe for s in signals) else None

    direction = classify_confluence_direction(signals)
    conflicting = detect_conflicting_signals(signals)
    score = calculate_confluence_score(signals, config)
    strength = classify_confluence_strength(score, len(signals), config)

    actions = {}
    for s in signals:
        action_str = s.action.value if hasattr(s.action, 'value') else str(s.action)
        actions[action_str] = actions.get(action_str, 0) + 1

    avg_conf = sum(s.confidence for s in signals) / len(signals) if signals else None

    valid_scores = [s.score for s in signals if s.score is not None]
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else None

    strategies = list(set(s.strategy_name for s in signals))
    signal_ids = [s.signal_id for s in signals]

    reasons = [f"{s.strategy_name}: {s.action.value}" for s in signals]
    if conflicting:
        reasons.append("Conflicting directions detected.")

    return ConfluenceGroupResult(
        symbol=symbol,
        timeframe=timeframe,
        direction=direction,
        strength=strength,
        confluence_score=score,
        signal_count=len(signals),
        strategies=strategies,
        actions=actions,
        average_confidence=avg_conf,
        average_score=avg_score,
        conflicting=conflicting,
        reasons=reasons,
        signal_ids=signal_ids
    )

def evaluate_confluence(
    signals: List[StrategySignal],
    mode: SignalAggregationMode = SignalAggregationMode.BY_SYMBOL_TIMEFRAME,
    config: Optional[ConfluenceConfig] = None
) -> ConfluenceReport:

    if config is None:
        config = ConfluenceConfig()

    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    import uuid
    report_id = f"confluence_{uuid.uuid4().hex[:8]}"

    warnings = []
    errors = []
    results = []

    if not signals:
        warnings.append("No signals provided for confluence.")
    else:
        try:
            groups = group_signals_for_confluence(signals, mode)
            for group_key, group_signals in groups.items():
                if len(group_signals) >= config.min_signals_for_confluence:
                    res = evaluate_confluence_group(group_signals, config)
                    results.append(res)
        except Exception as e:
            errors.append(f"Confluence evaluation failed: {str(e)}")

    conflicted = sum(1 for r in results if r.conflicting)
    strong = sum(1 for r in results if r.strength in [ConfluenceStrength.STRONG, ConfluenceStrength.VERY_STRONG])

    return ConfluenceReport(
        report_id=report_id,
        created_at_utc=now_utc,
        aggregation_mode=mode,
        group_results=results,
        total_groups=len(results),
        conflicted_groups=conflicted,
        strong_groups=strong,
        warnings=warnings,
        errors=errors
    )

def confluence_report_to_text(report: ConfluenceReport) -> str:
    lines = [
        f"--- Confluence Report: {report.report_id} ---",
        f"Mode: {report.aggregation_mode.value if hasattr(report.aggregation_mode, 'value') else report.aggregation_mode}",
        f"Total Groups Evaluated: {report.total_groups}",
        f"Conflicted Groups: {report.conflicted_groups}",
        f"Strong/Very Strong Groups: {report.strong_groups}",
        ""
    ]
    for grp in report.group_results:
        lines.append(f"Symbol: {grp.symbol} (TF: {grp.timeframe})")
        lines.append(f"  Direction: {grp.direction.value if hasattr(grp.direction, 'value') else grp.direction}")
        lines.append(f"  Strength: {grp.strength.value if hasattr(grp.strength, 'value') else grp.strength} (Score: {grp.confluence_score:.1f})")
        lines.append(f"  Signals: {grp.signal_count} across {len(grp.strategies)} strategies")
        lines.append("")

    if report.warnings:
        lines.append("Warnings:")
        for w in report.warnings:
            lines.append(f"  - {w}")
    if report.errors:
        lines.append("Errors:")
        for e in report.errors:
            lines.append(f"  - {e}")

    return "\n".join(lines)
