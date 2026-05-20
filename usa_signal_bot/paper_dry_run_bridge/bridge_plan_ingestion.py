from typing import Any, Tuple, List, Optional
from usa_signal_bot.core.enums import BridgePlanStatus

def ingest_bridge_plan_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.copy()

def extract_bridge_plan_id(payload: dict[str, Any]) -> Optional[str]:
    return payload.get("bridge_plan_id")

def extract_bridge_plan_status(payload: dict[str, Any]) -> Optional[str]:
    return payload.get("status")

def bridge_plan_supports_session(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    status = extract_bridge_plan_status(payload)
    if not status:
        return False, ["Missing bridge plan status"]

    warnings = []
    if status == BridgePlanStatus.VALIDATED.value:
        pass
    elif status in [
        BridgePlanStatus.BLOCKED.value,
        BridgePlanStatus.EXPIRED.value
    ]:
        return False, [f"Bridge plan status {status} is not supported for session"]
    else:
        warnings.append(f"Bridge plan status {status} is not optimal for session")

    return True, warnings

def bridge_plan_safety_checks(payload: dict[str, Any]) -> List[str]:
    errors = []
    if payload.get("execution_enabled", False):
        errors.append("Bridge plan has execution enabled. This is strictly forbidden.")
    if payload.get("paper_write_enabled", False):
        errors.append("Bridge plan has paper write enabled. This is strictly forbidden.")
    if payload.get("broker_write_enabled", False):
        errors.append("Bridge plan has broker write enabled. This is strictly forbidden.")
    if payload.get("telegram_write_enabled", False):
        errors.append("Bridge plan has telegram write enabled. This is strictly forbidden.")
    if payload.get("config_write_enabled", False):
        errors.append("Bridge plan has config write enabled. This is strictly forbidden.")

    allowed_ops = payload.get("allowed_operations", [])
    dangerous_ops = ["write_paper_state", "send_paper_order", "send_broker_order", "send_telegram_real", "write_production_config"]
    for op in allowed_ops:
        if op in dangerous_ops:
            errors.append(f"Bridge plan allows dangerous operation: {op}")

    return errors

def bridge_plan_ingestion_to_text(payload: dict[str, Any]) -> str:
    plan_id = extract_bridge_plan_id(payload)
    status = extract_bridge_plan_status(payload)
    return f"Bridge Plan Ingestion: Plan {plan_id} (Status: {status})"
