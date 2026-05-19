from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import SandboxOperation, SandboxOperationDecision
from usa_signal_bot.release_sandbox.sandbox_models import SandboxRuntimeContext, SandboxMountPlan
from usa_signal_bot.core.exceptions import BlockedOperationGuardError

def sandbox_operation_decision(operation: SandboxOperation, context: Optional[Any] = None) -> SandboxOperationDecision:
    if operation in denied_operations_for_sandbox():
        return SandboxOperationDecision.DENY
    return SandboxOperationDecision.ALLOW

def assert_operation_allowed(operation: SandboxOperation, context: Optional[Any] = None) -> None:
    if sandbox_operation_decision(operation, context) == SandboxOperationDecision.DENY:
        raise BlockedOperationGuardError(f"Operation {operation} is denied in sandbox.")

def denied_operations_for_sandbox() -> List[SandboxOperation]:
    return [
        SandboxOperation.WRITE_PRODUCTION_CONFIG,
        SandboxOperation.MUTATE_PAPER_STATE,
        SandboxOperation.SEND_ORDER,
        SandboxOperation.SEND_TELEGRAM_REAL,
        SandboxOperation.NETWORK_BROKER_CALL
    ]

def operation_guard_summary(operations: List[SandboxOperation], context: Optional[SandboxRuntimeContext] = None) -> Dict[str, Any]:
    return {"checked": len(operations)}

def blocked_operation_guard_to_text(payload: Dict[str, Any]) -> str:
    return "Operation Guard Check Completed"
