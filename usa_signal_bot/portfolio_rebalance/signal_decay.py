import datetime
from typing import Any, Dict, Optional
from datetime import timezone
from usa_signal_bot.core.enums import DriftType, DriftSeverity
from usa_signal_bot.portfolio_rebalance.rebalance_models import DriftMeasurement, create_drift_measurement_id

def estimate_signal_age_minutes(signal_or_candidate: Dict[str, Any], now_utc: Optional[str] = None) -> Optional[float]:
    if "timestamp_utc" not in signal_or_candidate and "created_at_utc" not in signal_or_candidate:
        return None

    ts_str = signal_or_candidate.get("timestamp_utc") or signal_or_candidate.get("created_at_utc")
    try:
        ts = datetime.datetime.fromisoformat(ts_str)
        now = datetime.datetime.fromisoformat(now_utc) if now_utc else datetime.datetime.now(timezone.utc)
        diff = now - ts
        return max(0.0, diff.total_seconds() / 60.0)
    except Exception:
        return None

def signal_decay_multiplier(age_minutes: Optional[float], half_life_minutes: float = 240.0) -> float:
    if age_minutes is None or age_minutes <= 0:
        return 1.0
    return max(0.0, 1.0 - (age_minutes / half_life_minutes))

def classify_signal_decay_severity(age_minutes: Optional[float], max_age_minutes: float = 1440.0) -> DriftSeverity:
    if age_minutes is None:
        return DriftSeverity.INSUFFICIENT_DATA
    if age_minutes >= max_age_minutes:
        return DriftSeverity.CRITICAL
    if age_minutes >= max_age_minutes * 0.75:
        return DriftSeverity.HIGH
    if age_minutes >= max_age_minutes * 0.5:
        return DriftSeverity.MODERATE
    if age_minutes >= max_age_minutes * 0.25:
        return DriftSeverity.LOW
    return DriftSeverity.NONE

def signal_valid_for_rebalance(signal_or_candidate: Dict[str, Any], max_age_minutes: float = 1440.0) -> bool:
    age = estimate_signal_age_minutes(signal_or_candidate)
    if age is None:
        return False
    return age < max_age_minutes

def signal_decay_drift_measurement(symbol: str, signal_or_candidate: Dict[str, Any]) -> DriftMeasurement:
    age = estimate_signal_age_minutes(signal_or_candidate)
    severity = classify_signal_decay_severity(age)
    multiplier = signal_decay_multiplier(age)

    warnings = []
    if age is None:
        warnings.append(f"Missing or invalid timestamp for signal: {symbol}")

    now_str = datetime.datetime.now(timezone.utc).isoformat()
    return DriftMeasurement(
        drift_id=create_drift_measurement_id(symbol),
        created_at_utc=now_str,
        drift_type=DriftType.SIGNAL_DECAY,
        name=f"SignalDecay_{symbol}",
        current_value=1.0,
        target_value=multiplier,
        absolute_drift=abs(1.0 - multiplier) if age is not None else None,
        pct_drift=(multiplier - 1.0) * 100.0 if age is not None else None,
        severity=severity,
        threshold=None,
        warnings=warnings,
        metadata={"age_minutes": age, "decay_multiplier": multiplier}
    )

def signal_decay_to_text(payload: Dict[str, Any]) -> str:
    age = payload.get("age_minutes")
    mult = payload.get("decay_multiplier")
    if age is None or mult is None:
        return "Signal Decay: Insufficient Data"
    return f"Signal Decay: Age {age:.1f} mins, Multiplier {mult:.2f}"
