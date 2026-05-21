from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def risk_warning_ratio(sessions: List[dict[str, Any]]) -> float | None:
    total_proposals = sum(len(s.get("proposals", [])) for s in sessions)
    if total_proposals == 0:
        return None
    warnings = sum(s.get("risk_warning_count", 0) for s in sessions)
    return min(1.0, warnings / total_proposals)

def risk_rejection_ratio(sessions: List[dict[str, Any]]) -> float | None:
    total_proposals = sum(len(s.get("proposals", [])) for s in sessions)
    if total_proposals == 0:
        return None
    rejections = sum(s.get("risk_rejected_count", 0) for s in sessions)
    return min(1.0, rejections / total_proposals)

def risk_history_flags(sessions: List[dict[str, Any]]) -> List[ObservationRiskFlag]:
    flags = set()
    for s in sessions:
        if s.get("real_order_risk_detected"):
            flags.add(ObservationRiskFlag.REAL_ORDER_RISK)
        if s.get("paper_state_mutation_detected"):
            flags.add(ObservationRiskFlag.PAPER_STATE_MUTATION_RISK)

    rej_ratio = risk_rejection_ratio(sessions)
    if rej_ratio is not None and rej_ratio > 0.5:
        flags.add(ObservationRiskFlag.RISK_REJECTION_HIGH)

    return list(flags)

def aggregate_risk_outcome_history(sessions: List[dict[str, Any]]) -> dict[str, Any]:
    return {
        "session_count": len(sessions),
        "warning_ratio": risk_warning_ratio(sessions),
        "rejection_ratio": risk_rejection_ratio(sessions),
        "risk_flags": [f.value for f in risk_history_flags(sessions)]
    }

def risk_history_to_text(payload: dict[str, Any]) -> str:
    rej = payload.get('rejection_ratio')
    r_str = f"{rej:.2f}" if rej is not None else "N/A"
    return f"Risk History\nSessions: {payload.get('session_count', 0)}\nRejection Ratio: {r_str}\nFlags: {len(payload.get('risk_flags', []))}"
