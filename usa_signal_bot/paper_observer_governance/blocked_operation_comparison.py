from typing import Any
from usa_signal_bot.core.enums import ObserverGovernanceRiskFlag

def compare_observer_blocked_operations(observer_payload: dict[str, Any]) -> dict[str, Any]:
    return {"count": count_observer_blocked_operations(observer_payload), "by_type": blocked_operations_by_type(observer_payload)}

def count_observer_blocked_operations(observer_payload: dict[str, Any]) -> int:
    return len(observer_payload.get("blocked_operations", []))

def blocked_operations_by_type(observer_payload: dict[str, Any]) -> dict[str, int]:
    return {}

def blocked_operation_comparison_risk_flags(payload: dict[str, Any]) -> list[ObserverGovernanceRiskFlag]:
    if payload.get("count", 0) > 0: return [ObserverGovernanceRiskFlag.BLOCKED_OPERATION_HISTORY]
    return []

def blocked_operation_comparison_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
