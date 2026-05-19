from typing import Any, Dict, List, Optional, Union
from usa_signal_bot.core.enums import SandboxOperation, SandboxOperationDecision
from usa_signal_bot.release_sandbox.sandbox_models import SandboxRuntimeContext, SandboxMountPlan
from usa_signal_bot.core.exceptions import BlockedOperationGuardError

def denied_operations_for_sandbox() -> List[SandboxOperation]:
    return [
        SandboxOperation.SEND_ORDER,
        SandboxOperation.NETWORK_BROKER_CALL,
        SandboxOperation.SEND_TELEGRAM_REAL,
        SandboxOperation.WRITE_PRODUCTION_CONFIG,
        SandboxOperation.MUTATE_PAPER_STATE
    ]

def sandbox_operation_decision(
    operation: SandboxOperation,
    context: Optional[Union[SandboxRuntimeContext, SandboxMountPlan]] = None
) -> SandboxOperationDecision:

    if operation in denied_operations_for_sandbox():
        return SandboxOperationDecision.DENY

    if context:
        if operation in getattr(context, "denied_operations", []):
            return SandboxOperationDecision.DENY

        if operation in getattr(context, "allowed_operations", []):
            return SandboxOperationDecision.ALLOW

    return SandboxOperationDecision.ALLOW

def assert_operation_allowed(
    operation: SandboxOperation,
    context: Optional[Union[SandboxRuntimeContext, SandboxMountPlan]] = None
) -> None:
    decision = sandbox_operation_decision(operation, context)
    if decision == SandboxOperationDecision.DENY:
        raise BlockedOperationGuardError(f"Operation {operation.value} is denied in sandbox mode.")

def operation_guard_summary(
    operations: List[SandboxOperation],
    context: Optional[SandboxRuntimeContext] = None
) -> Dict[str, Any]:
    decisions = {}
    for op in operations:
        decisions[op.value] = sandbox_operation_decision(op, context).value
    return {"decisions": decisions}

def blocked_operation_guard_to_text(payload: Dict[str, Any]) -> str:
    decisions = payload.get("decisions", {})
    return f"Blocked Operation Guard Summary: {len(decisions)} operations evaluated."
