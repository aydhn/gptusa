from typing import Any, Dict, Optional
from usa_signal_bot.core.enums import SizingAdjustmentReason

def normalize_confidence_score(value: Optional[float], default: float = 50.0) -> float:
    if value is None:
        return default
    return max(0.0, min(100.0, value))

def combine_confidence_inputs(
    signal_score: Optional[float] = None,
    signal_confidence: Optional[float] = None,
    ensemble_consensus_score: Optional[float] = None,
    regime_alignment_score: Optional[float] = None,
    cost_robustness_score: Optional[float] = None,
    execution_realism_score: Optional[float] = None
) -> float:
    scores = []
    if signal_score is not None:
        scores.append(normalize_confidence_score(signal_score))
    if signal_confidence is not None:
        scores.append(normalize_confidence_score(signal_confidence))
    if ensemble_consensus_score is not None:
        scores.append(normalize_confidence_score(ensemble_consensus_score))
    if regime_alignment_score is not None:
        scores.append(normalize_confidence_score(regime_alignment_score))
    if cost_robustness_score is not None:
        scores.append(normalize_confidence_score(cost_robustness_score))
    if execution_realism_score is not None:
        scores.append(normalize_confidence_score(execution_realism_score))

    if not scores:
        return 50.0
    return sum(scores) / len(scores)

def confidence_to_size_multiplier(confidence_score: Optional[float], min_multiplier: float = 0.25, max_multiplier: float = 1.50) -> float:
    score = normalize_confidence_score(confidence_score)
    # Linear scale from 0 to 100 mapping to min_multiplier to max_multiplier
    multiplier = min_multiplier + (score / 100.0) * (max_multiplier - min_multiplier)
    return max(min_multiplier, min(max_multiplier, multiplier))

def confidence_adjustment_reason(confidence_score: Optional[float]) -> SizingAdjustmentReason:
    score = normalize_confidence_score(confidence_score)
    if score < 40.0:
        return SizingAdjustmentReason.LOW_CONFIDENCE
    elif score > 75.0:
        return SizingAdjustmentReason.HIGH_CONFIDENCE
    return SizingAdjustmentReason.UNKNOWN

def confidence_scaling_summary_to_text(payload: Dict[str, Any]) -> str:
    return (
        f"Confidence Score: {payload.get('confidence_score', 'N/A')}\n"
        f"Confidence Multiplier: {payload.get('multiplier', 'N/A')}\n"
        f"Reason: {payload.get('reason', 'UNKNOWN')}"
    )
