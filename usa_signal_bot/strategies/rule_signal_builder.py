from typing import Dict, Any, List
from usa_signal_bot.core.enums import SignalAction, SignalRiskFlag, SignalLifecycleStatus, RuleSignalBias
from usa_signal_bot.strategies.signal_contract import StrategySignal, create_signal_id, confidence_to_bucket
from usa_signal_bot.strategies.rule_models import RuleEvaluation, RuleStrategyDefinition

def action_from_rule_bias(bias: RuleSignalBias, default_action: SignalAction, watch_only: bool = True) -> SignalAction:
    if watch_only:
        return SignalAction.WATCH

    if bias == RuleSignalBias.BULLISH:
        return SignalAction.LONG
    elif bias == RuleSignalBias.BEARISH:
        return SignalAction.SHORT
    elif bias == RuleSignalBias.AVOID:
        return SignalAction.AVOID

    return default_action

def confidence_from_rule_score(score: float, max_allowed: float = 0.70) -> float:
    # Scale score (0-100) to confidence (0.0-1.0), capping at max_allowed
    conf = score / 100.0
    return min(conf, max_allowed)

def score_from_rule_evaluation(evaluation: RuleEvaluation) -> float:
    return evaluation.normalized_score

def risk_flags_from_rule_evaluation(evaluation: RuleEvaluation) -> List[SignalRiskFlag]:
    flags = []
    if evaluation.missing_count > 0:
        flags.append(SignalRiskFlag.INSUFFICIENT_FEATURES)
    if evaluation.bias == RuleSignalBias.CONFLICTED:
        flags.append(SignalRiskFlag.CONFLICTING_FEATURES)

    if not flags:
        flags.append(SignalRiskFlag.NONE)
    return flags

def build_signal_from_rule_evaluation(
    evaluation: RuleEvaluation,
    definition: RuleStrategyDefinition,
    feature_snapshot: Dict[str, Any],
    watch_only: bool = True,
    max_confidence: float = 0.70
) -> StrategySignal:

    signal_id = create_signal_id(
        definition.name,
        evaluation.symbol,
        evaluation.timeframe,
        evaluation.timestamp_utc
    )

    action = action_from_rule_bias(evaluation.bias, definition.default_action, watch_only)
    confidence = confidence_from_rule_score(evaluation.normalized_score, max_confidence)
    score = score_from_rule_evaluation(evaluation)
    risk_flags = risk_flags_from_rule_evaluation(evaluation)

    return StrategySignal(
        signal_id=signal_id,
        strategy_name=definition.name,
        symbol=evaluation.symbol,
        timeframe=evaluation.timeframe,
        timestamp_utc=evaluation.timestamp_utc,
        action=action,
        confidence=confidence,
        confidence_bucket=confidence_to_bucket(confidence),
        score=score,
        reasons=evaluation.reasons + evaluation.warnings,
        feature_snapshot=feature_snapshot,
        risk_flags=risk_flags,
        lifecycle_status=SignalLifecycleStatus.CREATED,
        metadata={
            "rule_family": evaluation.family.value if hasattr(evaluation.family, 'value') else evaluation.family,
            "passed_conditions": evaluation.passed_count,
            "failed_conditions": evaluation.failed_count,
            "missing_conditions": evaluation.missing_count,
            "candidate_only": True,
            "no_execution": True
        }
    )

def create_no_feature_watch_signal(
    strategy_name: str,
    symbol: str,
    timeframe: str,
    timestamp_utc: str,
    missing_features: List[str]
) -> StrategySignal:

    signal_id = create_signal_id(strategy_name, symbol, timeframe, timestamp_utc)
    reason = f"Missing required features: {', '.join(missing_features)}"
    confidence = 0.0

    return StrategySignal(
        signal_id=signal_id,
        strategy_name=strategy_name,
        symbol=symbol,
        timeframe=timeframe,
        timestamp_utc=timestamp_utc,
        action=SignalAction.WATCH,
        confidence=confidence,
        confidence_bucket=confidence_to_bucket(confidence),
        score=0.0,
        reasons=[reason, "Candidate only, not for execution"],
        feature_snapshot={},
        risk_flags=[SignalRiskFlag.INSUFFICIENT_FEATURES],
        lifecycle_status=SignalLifecycleStatus.CREATED,
        metadata={
            "candidate_only": True,
            "no_execution": True
        }
    )
