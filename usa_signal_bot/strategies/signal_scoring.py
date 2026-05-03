"""Signal scoring models and calculations."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import SignalScoreComponent, SignalConfidenceBucket, SignalRiskFlag
from usa_signal_bot.core.config_schema import SignalScoringConfigSchema
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.exceptions import SignalScoringError

@dataclass
class SignalScoreBreakdown:
    signal_id: str
    total_score: float
    components: Dict[str, float]
    penalties: Dict[str, float]
    bonuses: Dict[str, float]
    final_confidence: float
    confidence_bucket: SignalConfidenceBucket
    notes: List[str] = field(default_factory=list)

@dataclass
class SignalScoringResult:
    original_signal: StrategySignal
    scored_signal: StrategySignal
    breakdown: SignalScoreBreakdown
    accepted_for_review: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def default_signal_scoring_config() -> SignalScoringConfigSchema:
    return SignalScoringConfigSchema()

def validate_signal_scoring_config(config: SignalScoringConfigSchema) -> None:
    if config.min_score < 0:
        raise SignalScoringError("min_score must be >= 0")
    if config.max_score <= config.min_score:
        raise SignalScoringError("max_score must be greater than min_score")
    if config.max_score > 100:
        raise SignalScoringError("max_score must be <= 100")
    if not (0 <= config.base_score <= 100):
        raise SignalScoringError("base_score must be between 0 and 100")
    if not (0 <= config.max_allowed_score_without_backtest <= 100):
        raise SignalScoringError("max_allowed_score_without_backtest must be between 0 and 100")
    if config.confidence_weight < 0 or config.reason_quality_weight < 0 or config.feature_snapshot_weight < 0 or config.risk_penalty_weight < 0:
        raise SignalScoringError("weights cannot be negative")

def clamp_score(score: float, min_score: float = 0.0, max_score: float = 100.0) -> float:
    return max(min_score, min(score, max_score))

def calculate_reason_quality_score(reasons: List[str]) -> float:
    if not reasons:
        return 0.0

    unique_reasons = set(r.strip().lower() for r in reasons if r.strip())
    count = len(unique_reasons)

    if count == 0:
        return 0.0
    elif count == 1:
        return 0.4
    elif count == 2:
        return 0.7
    elif count == 3:
        return 0.9
    else:
        return 1.0

def calculate_feature_snapshot_score(feature_snapshot: Dict[str, Any]) -> float:
    if not feature_snapshot:
        return 0.0

    keys = [k for k in feature_snapshot.keys() if not k.startswith('_')]
    count = len(keys)

    if count == 0:
        return 0.1
    elif count <= 2:
        return 0.4
    elif count <= 5:
        return 0.7
    elif count <= 10:
        return 0.9
    else:
        return 1.0

def calculate_risk_penalty(risk_flags: List[SignalRiskFlag], config: Optional[SignalScoringConfigSchema] = None) -> float:
    if not risk_flags:
        return 0.0

    # Standardize penalty based on number of flags and severity
    penalty_ratio = min(1.0, len(risk_flags) * 0.25)
    return penalty_ratio

def calibrate_confidence_from_score(score: float) -> float:
    # A simple linear mapping from 0-100 to 0.0-1.0
    return max(0.0, min(1.0, score / 100.0))

def score_signal(signal: StrategySignal, config: Optional[SignalScoringConfigSchema] = None) -> SignalScoringResult:
    if config is None:
        config = default_signal_scoring_config()

    validate_signal_scoring_config(config)

    warnings = []
    errors = []
    components = {}
    penalties = {}
    bonuses = {}
    notes = []

    try:
        # 1. Base Score
        base = config.base_score
        components[SignalScoreComponent.STRATEGY_BASE.value] = base

        # 2. Reason Quality Score
        reason_ratio = calculate_reason_quality_score(signal.reasons)
        reason_score = reason_ratio * config.reason_quality_weight
        components[SignalScoreComponent.REASON_QUALITY.value] = reason_score
        if reason_ratio == 0:
            notes.append("No valid reasons provided.")

        # 3. Feature Snapshot Score
        feature_ratio = calculate_feature_snapshot_score(signal.feature_snapshot)
        feature_score = feature_ratio * config.feature_snapshot_weight
        components[SignalScoreComponent.FEATURE_ALIGNMENT.value] = feature_score
        if feature_ratio < 0.2:
            notes.append("Feature snapshot is empty or insufficient.")

        # 4. Confidence Contribution
        conf_score = signal.confidence * config.confidence_weight
        components[SignalScoreComponent.CONFIDENCE.value] = conf_score

        # 5. Risk Penalty
        risk_ratio = calculate_risk_penalty(signal.risk_flags, config)
        risk_penalty = risk_ratio * config.risk_penalty_weight
        if risk_penalty > 0:
            penalties[SignalScoreComponent.RISK_PENALTY.value] = -risk_penalty
            notes.append(f"Applied risk penalty due to {len(signal.risk_flags)} flags.")

        # 6. Overconfidence Check (Backtest guard)
        # Without a backtest, confidence > 0.8 is penalized
        overconfidence_penalty = 0.0
        if signal.confidence > 0.8:
            overconfidence_penalty = config.overconfidence_penalty
            penalties["OVERCONFIDENCE"] = -overconfidence_penalty
            notes.append("Applied overconfidence penalty (no backtest validation).")

        # Calculate Total
        total_raw = sum(components.values()) + sum(penalties.values()) + sum(bonuses.values())
        total_clamped = clamp_score(total_raw, config.min_score, config.max_score)

        # Apply Backtest Guard Limit
        if total_clamped > config.max_allowed_score_without_backtest:
            total_clamped = config.max_allowed_score_without_backtest
            notes.append(f"Score capped at {config.max_allowed_score_without_backtest} (no backtest).")

        # Final calibrated confidence
        final_confidence = calibrate_confidence_from_score(total_clamped)

        # Re-evaluate confidence bucket based on final confidence
        if final_confidence >= 0.8:
            bucket = SignalConfidenceBucket.VERY_HIGH
        elif final_confidence >= 0.6:
            bucket = SignalConfidenceBucket.HIGH
        elif final_confidence >= 0.4:
            bucket = SignalConfidenceBucket.MODERATE
        elif final_confidence >= 0.2:
            bucket = SignalConfidenceBucket.LOW
        else:
            bucket = SignalConfidenceBucket.VERY_LOW

        accepted = total_clamped >= config.min_score_for_review

        # Update the signal (create a copy)
        import copy
        scored_signal = copy.deepcopy(signal)
        scored_signal.score = total_clamped
        scored_signal.confidence = final_confidence
        scored_signal.confidence_bucket = bucket
        scored_signal.score_breakdown = {
            "components": components,
            "penalties": penalties,
            "bonuses": bonuses
        }

        breakdown = SignalScoreBreakdown(
            signal_id=signal.signal_id,
            total_score=total_clamped,
            components=components,
            penalties=penalties,
            bonuses=bonuses,
            final_confidence=final_confidence,
            confidence_bucket=bucket,
            notes=notes
        )

        return SignalScoringResult(
            original_signal=signal,
            scored_signal=scored_signal,
            breakdown=breakdown,
            accepted_for_review=accepted,
            warnings=warnings,
            errors=errors
        )

    except Exception as e:
        errors.append(f"Scoring failed: {str(e)}")
        # Return a failed result
        breakdown = SignalScoreBreakdown(
            signal_id=signal.signal_id,
            total_score=0.0,
            components={},
            penalties={},
            bonuses={},
            final_confidence=0.0,
            confidence_bucket=SignalConfidenceBucket.VERY_LOW,
            notes=["Scoring failed"]
        )
        scored_signal = copy.deepcopy(signal) if 'copy' in locals() else signal
        return SignalScoringResult(
            original_signal=signal,
            scored_signal=scored_signal,
            breakdown=breakdown,
            accepted_for_review=False,
            warnings=warnings,
            errors=errors
        )

def score_signal_list(signals: List[StrategySignal], config: Optional[SignalScoringConfigSchema] = None) -> List[SignalScoringResult]:
    if not signals:
        return []
    return [score_signal(sig, config) for sig in signals]
