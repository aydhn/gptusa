from typing import Any, Dict, List
from usa_signal_bot.core.enums import ObserverSafetyFlag
from usa_signal_bot.core.exceptions import ObserverBlockedOperationError

def observer_denied_operations() -> List[str]:
    return [
        "write_paper_state",
        "send_paper_order",
        "send_broker_order",
        "send_telegram_real",
        "write_production_config",
        "enable_active_paper",
        "unlock_observer_runtime",
        "mutate_paper_store"
    ]

def observer_operation_allowed(operation: str) -> bool:
    return operation not in observer_denied_operations()

def assert_observer_operation_allowed(operation: str) -> None:
    if not observer_operation_allowed(operation):
        raise ObserverBlockedOperationError(f"Operation '{operation}' is explicitly BLOCKED in paper observer mode.")

def observer_blocked_operation_flags(operation: str) -> List[ObserverSafetyFlag]:
    flags = []
    if operation in ["send_real_order", "send_broker_order"]:
        flags.append(ObserverSafetyFlag.BROKER_ORDER_RISK)
    if operation == "write_paper_state":
        flags.append(ObserverSafetyFlag.PAPER_STATE_MUTATION_RISK)
    if operation == "send_telegram_real":
        flags.append(ObserverSafetyFlag.TELEGRAM_REAL_SEND_RISK)
    if operation == "write_production_config":
        flags.append(ObserverSafetyFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if operation == "enable_active_paper":
        flags.append(ObserverSafetyFlag.ACTIVE_PAPER_ENABLE_RISK)
    if operation == "unlock_observer_runtime":
        flags.append(ObserverSafetyFlag.OBSERVER_UNLOCK_RISK)
    return flags

def observer_blocked_operation_summary(operations: List[str]) -> Dict[str, Any]:
    return {"operations_checked": len(operations), "blocked": [op for op in operations if not observer_operation_allowed(op)]}

def observer_blocked_operation_guard_to_text(payload: Dict[str, Any]) -> str:
    return f"Blocked Operation Guard checked {payload.get('operations_checked')} items."
