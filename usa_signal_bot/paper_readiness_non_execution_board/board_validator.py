from typing import Any, Dict, List
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    PaperReadinessNonExecutionBoard,
    NonExecutionBoardGateStatus,
    NonExecutionBoardAssertionStatus
)

def validate_non_execution_board_safety(board: PaperReadinessNonExecutionBoard) -> List[str]:
    errors = []
    if not board.sealed:
        errors.append("Board must be sealed")
    if not board.immutable:
        errors.append("Board must be immutable")
    if not board.activation_denied:
        errors.append("Activation must be explicitly denied")
    if board.activation_allowed:
        errors.append("Activation must not be allowed")
    if board.admission_allowed:
        errors.append("Admission must not be allowed")
    if board.transition_allowed:
        errors.append("Transition must not be allowed")
    if not board.all_writes_blocked:
        errors.append("All writes must be blocked")
    if board.order_created:
        errors.append("Order must not be created")
    if board.mutation_detected:
        errors.append("Mutation must not be detected")

    for param in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
        if getattr(board, param):
            errors.append(f"{param} must be false")

    if not board.runtime_map_safe:
        errors.append("Runtime map must be safe")
    if not board.non_execution_confirmed:
        errors.append("Non-execution must be confirmed")

    for g in board.gates:
        if g.status in [NonExecutionBoardGateStatus.FAIL, NonExecutionBoardGateStatus.BLOCKED]:
            errors.append(f"Gate failed/blocked: {g.gate_name}")

    for a in board.assertions:
        if a.status in [NonExecutionBoardAssertionStatus.FAIL, NonExecutionBoardAssertionStatus.BLOCKED]:
            errors.append(f"Assertion failed/blocked: {a.assertion_name}")

    return errors

def non_execution_board_allows_activation(board: PaperReadinessNonExecutionBoard) -> bool:
    return board.activation_allowed or not board.activation_denied

def non_execution_board_allows_admission(board: PaperReadinessNonExecutionBoard) -> bool:
    return board.admission_allowed

def non_execution_board_requires_followup(board: PaperReadinessNonExecutionBoard) -> bool:
    return len(board.required_followups) > 0 or len(validate_non_execution_board_safety(board)) > 0

def non_execution_board_blocks_next_stage(board: PaperReadinessNonExecutionBoard) -> bool:
    return len(validate_non_execution_board_safety(board)) > 0

def non_execution_board_validator_summary(board: PaperReadinessNonExecutionBoard) -> Dict[str, Any]:
    return {
        "valid": len(validate_non_execution_board_safety(board)) == 0,
        "errors": validate_non_execution_board_safety(board)
    }

def non_execution_board_validator_to_text(payload: Dict[str, Any]) -> str:
    lines = ["--- BOARD VALIDATOR ---"]
    lines.append(f"Valid: {payload.get('valid')}")
    if payload.get("errors"):
        lines.append("Errors:")
        for e in payload.get("errors"):
            lines.append(f"  - {e}")
    return "\n".join(lines)
