from typing import Any

from usa_signal_bot.core.enums import BridgeOperation, BridgeOperationDecision
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinePolicy
from usa_signal_bot.paper_quarantine.quarantine_policy import allowed_quarantine_bridge_operations, denied_quarantine_bridge_operations
from usa_signal_bot.core.exceptions import BridgeOperationGuardError

def bridge_operation_decision(operation: BridgeOperation, policy: QuarantinePolicy | None = None) -> BridgeOperationDecision:
    allowed = allowed_quarantine_bridge_operations()
    if policy:
        allowed = policy.allowed_bridge_operations

    if operation in allowed:
        return BridgeOperationDecision.ALLOW

    denied = denied_quarantine_bridge_operations()
    if policy:
        denied = policy.denied_bridge_operations

    if operation in denied:
        return BridgeOperationDecision.DENY

    return BridgeOperationDecision.WARN

def assert_bridge_operation_allowed(operation: BridgeOperation, policy: QuarantinePolicy | None = None) -> None:
    decision = bridge_operation_decision(operation, policy)
    if decision == BridgeOperationDecision.DENY:
        raise BridgeOperationGuardError(f"Operation {operation.value} is explicitly DENIED by bridge guard.")

def bridge_operation_guard_summary(policy: QuarantinePolicy | None = None) -> dict[str, Any]:
    denied = denied_quarantine_bridge_operations()
    allowed = allowed_quarantine_bridge_operations()
    if policy:
        denied = policy.denied_bridge_operations
        allowed = policy.allowed_bridge_operations

    return {
        "denied_operations": [op.value for op in denied],
        "allowed_operations": [op.value for op in allowed],
    }

def bridge_operation_guard_to_text(payload: dict[str, Any]) -> str:
    denied = payload.get("denied_operations", [])
    allowed = payload.get("allowed_operations", [])

    lines = [
        "Bridge Operation Guard",
        f"Allowed: {allowed}",
        f"Denied: {denied}",
    ]
    return "\n".join(lines)
