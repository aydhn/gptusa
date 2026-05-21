from typing import Any, List, Dict
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def blocked_operation_count(events: List[dict[str, Any]]) -> int:
    return sum(1 for e in events if e.get("event_type") == "BLOCKED_OPERATION")

def blocked_operations_by_type(events: List[dict[str, Any]]) -> Dict[str, int]:
    counts = {}
    for ev in events:
        if ev.get("event_type") == "BLOCKED_OPERATION":
            op_type = ev.get("operation_type", "UNKNOWN")
            counts[op_type] = counts.get(op_type, 0) + 1
    return counts

def blocked_operation_risk_flags(events: List[dict[str, Any]]) -> List[ObservationRiskFlag]:
    flags = set()
    if blocked_operation_count(events) > 0:
        flags.add(ObservationRiskFlag.BLOCKED_OPERATION_HISTORY)

    ops = blocked_operations_by_type(events)
    if "REAL_ORDER" in ops:
        flags.add(ObservationRiskFlag.REAL_ORDER_RISK)
    if "PAPER_ORDER" in ops:
        flags.add(ObservationRiskFlag.PAPER_ORDER_RISK)
    if "BROKER_API" in ops:
        flags.add(ObservationRiskFlag.BROKER_ORDER_RISK)
    if "PAPER_STATE_MUTATION" in ops:
        flags.add(ObservationRiskFlag.PAPER_STATE_MUTATION_RISK)
    if "TELEGRAM_REAL_SEND" in ops:
        flags.add(ObservationRiskFlag.TELEGRAM_REAL_SEND_RISK)
    if "CONFIG_PATCH" in ops:
        flags.add(ObservationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

    return list(flags)

def aggregate_blocked_operation_history(events: List[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_blocked": blocked_operation_count(events),
        "by_type": blocked_operations_by_type(events),
        "risk_flags": [f.value for f in blocked_operation_risk_flags(events)]
    }

def blocked_operation_history_to_text(payload: dict[str, Any]) -> str:
    return f"Blocked Operation History\nTotal Blocked: {payload.get('total_blocked', 0)}\nRisk Flags: {len(payload.get('risk_flags', []))}"
