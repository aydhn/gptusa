from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import hashlib
from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket, SignalRiskFlag, SignalLifecycleStatus
from usa_signal_bot.core.exceptions import SignalContractError

@dataclass
class StrategySignal:
    signal_id: str
    strategy_name: str
    symbol: str
    timeframe: str
    timestamp_utc: str
    action: SignalAction
    confidence: float
    confidence_bucket: SignalConfidenceBucket
    score: float
    reasons: List[str]
    feature_snapshot: Dict[str, Any]
    risk_flags: List[SignalRiskFlag]
    lifecycle_status: SignalLifecycleStatus = SignalLifecycleStatus.CREATED
    expires_at_utc: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

def validate_strategy_signal(signal: StrategySignal) -> None:
    if not signal.signal_id:
        raise SignalContractError("signal_id cannot be empty")
    if not signal.strategy_name:
        raise SignalContractError("strategy_name cannot be empty")
    if not signal.symbol:
        raise SignalContractError("symbol cannot be empty")
    if not signal.timeframe:
        raise SignalContractError("timeframe cannot be empty")
    if not signal.timestamp_utc:
        raise SignalContractError("timestamp_utc cannot be empty")

    if not (0.0 <= signal.confidence <= 1.0):
        raise SignalContractError(f"confidence must be between 0.0 and 1.0, got {signal.confidence}")
    if not (0.0 <= signal.score <= 100.0):
        raise SignalContractError(f"score must be between 0.0 and 100.0, got {signal.score}")

    if not isinstance(signal.reasons, list):
        raise SignalContractError("reasons must be a list")
    if not isinstance(signal.action, SignalAction):
        raise SignalContractError("action must be a SignalAction")
    if not isinstance(signal.lifecycle_status, SignalLifecycleStatus):
        raise SignalContractError("lifecycle_status must be a SignalLifecycleStatus")

def create_signal_id(strategy_name: str, symbol: str, timeframe: str, timestamp_utc: str) -> str:
    raw = f"{strategy_name}_{symbol}_{timeframe}_{timestamp_utc}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]

def confidence_to_bucket(confidence: float) -> SignalConfidenceBucket:
    if confidence < 0.20:
        return SignalConfidenceBucket.VERY_LOW
    elif confidence < 0.40:
        return SignalConfidenceBucket.LOW
    elif confidence < 0.60:
        return SignalConfidenceBucket.MODERATE
    elif confidence < 0.80:
        return SignalConfidenceBucket.HIGH
    else:
        return SignalConfidenceBucket.VERY_HIGH

def signal_to_dict(signal: StrategySignal) -> dict:
    return {
        "signal_id": signal.signal_id,
        "strategy_name": signal.strategy_name,
        "symbol": signal.symbol,
        "timeframe": signal.timeframe,
        "timestamp_utc": signal.timestamp_utc,
        "action": signal.action.value if isinstance(signal.action, SignalAction) else signal.action,
        "confidence": signal.confidence,
        "confidence_bucket": signal.confidence_bucket.value if isinstance(signal.confidence_bucket, SignalConfidenceBucket) else signal.confidence_bucket,
        "score": signal.score,
        "reasons": signal.reasons,
        "feature_snapshot": signal.feature_snapshot,
        "risk_flags": [f.value if isinstance(f, SignalRiskFlag) else f for f in signal.risk_flags],
        "lifecycle_status": signal.lifecycle_status.value if isinstance(signal.lifecycle_status, SignalLifecycleStatus) else signal.lifecycle_status,
        "expires_at_utc": signal.expires_at_utc,
        "metadata": signal.metadata
    }

def signal_to_text(signal: StrategySignal) -> str:
    lines = [
        f"Signal [{signal.signal_id}] {signal.symbol} ({signal.timeframe}) - {signal.action.value if hasattr(signal.action, 'value') else signal.action}",
        f"  Strategy: {signal.strategy_name}",
        f"  Confidence: {signal.confidence:.2f} ({signal.confidence_bucket.value if hasattr(signal.confidence_bucket, 'value') else signal.confidence_bucket}) | Score: {signal.score:.1f}",
        f"  Timestamp: {signal.timestamp_utc}"
    ]
    if signal.reasons:
        lines.append("  Reasons:")
        for r in signal.reasons:
            lines.append(f"    - {r}")
    if signal.risk_flags and any(f != SignalRiskFlag.NONE for f in signal.risk_flags):
        flags = [f.value if hasattr(f, 'value') else f for f in signal.risk_flags if f != SignalRiskFlag.NONE]
        if flags:
            lines.append(f"  Risk Flags: {', '.join(flags)}")
    return "\n".join(lines)

def create_watch_signal(strategy_name: str, symbol: str, timeframe: str, timestamp_utc: str, reason: str, confidence: float = 0.5) -> StrategySignal:
    signal_id = create_signal_id(strategy_name, symbol, timeframe, timestamp_utc)
    return StrategySignal(
        signal_id=signal_id,
        strategy_name=strategy_name,
        symbol=symbol,
        timeframe=timeframe,
        timestamp_utc=timestamp_utc,
        action=SignalAction.WATCH,
        confidence=confidence,
        confidence_bucket=confidence_to_bucket(confidence),
        score=confidence * 100.0,
        reasons=[reason, "Candidate only, not for execution"],
        feature_snapshot={},
        risk_flags=[SignalRiskFlag.NONE],
        lifecycle_status=SignalLifecycleStatus.CREATED
    )
