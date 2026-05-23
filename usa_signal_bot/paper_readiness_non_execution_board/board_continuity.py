from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    PaperReadinessNonExecutionBoard,
    RuntimeMapReplayResult,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardRiskFlag,
    NonExecutionBoardGateStatus,
    NonExecutionBoardAssertionStatus
)

def validate_non_execution_board_continuity(board: Optional[PaperReadinessNonExecutionBoard] = None, replay_result: Optional[RuntimeMapReplayResult] = None, seal_audit: Optional[NonExecutionSealIntegrityAudit] = None) -> List[str]:
    errors = []

    if board:
        if not board.activation_denied: errors.append("Board activation not denied")
        if board.activation_allowed: errors.append("Board allows activation")
        if board.admission_allowed: errors.append("Board allows admission")
        if board.transition_allowed: errors.append("Board allows transition")
        if not board.all_writes_blocked: errors.append("Board writes not blocked")
        if board.order_created: errors.append("Board order created")
        if board.mutation_detected: errors.append("Board mutation detected")
        if board.allows_active_paper: errors.append("Board allows active paper")
        if board.allows_broker_execution: errors.append("Board allows broker execution")

    if replay_result:
        if not replay_result.passed: errors.append("Runtime replay not passed")
        if replay_result.dangerous_allowed_count > 0: errors.append("Dangerous route allowed in replay")

    if seal_audit:
        if not seal_audit.integrity_valid: errors.append("Seal integrity not valid")

    return errors

def non_execution_board_continuity_flags(payload: Dict[str, Any]) -> List[NonExecutionBoardRiskFlag]:
    flags = []
    if payload.get("activation_allowed"): flags.append(NonExecutionBoardRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed"): flags.append(NonExecutionBoardRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed"): flags.append(NonExecutionBoardRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("order_created"): flags.append(NonExecutionBoardRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected"): flags.append(NonExecutionBoardRiskFlag.MUTATION_DETECTED_RISK)

    # We could also check replay and seal flags if included in payload, but typically this is checked via models
    if payload.get("dangerous_allowed_count", 0) > 0:
        flags.append(NonExecutionBoardRiskFlag.DANGEROUS_RUNTIME_ROUTE_ALLOWED)

    if payload.get("seal_valid") is False:
        flags.append(NonExecutionBoardRiskFlag.NON_EXECUTION_SEAL_CONFIRMATION_FAILED)

    return flags

def non_execution_board_continuity_is_preserved(payload: Dict[str, Any]) -> bool:
    flags = non_execution_board_continuity_flags(payload)
    return len(flags) == 0

def non_execution_board_continuity_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    flags = non_execution_board_continuity_flags(payload)
    return {
        "preserved": len(flags) == 0,
        "flags": [f.value for f in flags]
    }

def non_execution_board_continuity_to_text(payload: Dict[str, Any]) -> str:
    summary = non_execution_board_continuity_summary(payload)
    lines = ["--- CONTINUITY CHECKER ---"]
    lines.append(f"Preserved: {summary['preserved']}")
    if summary['flags']:
        lines.append("Risk Flags:")
        for f in summary['flags']:
            lines.append(f"  - {f}")
    return "\n".join(lines)
