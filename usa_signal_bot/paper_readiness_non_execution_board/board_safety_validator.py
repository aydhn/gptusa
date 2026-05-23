from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    PaperReadinessNonExecutionBoard,
    RuntimeMapReplayResult,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardRiskFlag
)
from usa_signal_bot.paper_readiness_non_execution_board.board_continuity import non_execution_board_continuity_flags

def collect_non_execution_board_safety_flags(board: Optional[PaperReadinessNonExecutionBoard] = None, replay_result: Optional[RuntimeMapReplayResult] = None, seal_audit: Optional[NonExecutionSealIntegrityAudit] = None) -> List[NonExecutionBoardRiskFlag]:
    flags = set()
    if board:
        for f in board.safety_flags: flags.add(f)
    if replay_result:
        for f in replay_result.risk_flags: flags.add(f)
    if seal_audit:
        for f in seal_audit.risk_flags: flags.add(f)
    return list(flags)

def non_execution_board_has_blocking_flags(flags: List[NonExecutionBoardRiskFlag]) -> bool:
    blocking_types = [
        NonExecutionBoardRiskFlag.REAL_ORDER_RISK,
        NonExecutionBoardRiskFlag.PAPER_ORDER_RISK,
        NonExecutionBoardRiskFlag.BROKER_ORDER_RISK,
        NonExecutionBoardRiskFlag.PAPER_STATE_MUTATION_RISK,
        NonExecutionBoardRiskFlag.PAPER_POSITION_MUTATION_RISK,
        NonExecutionBoardRiskFlag.PAPER_PORTFOLIO_MUTATION_RISK,
        NonExecutionBoardRiskFlag.TELEGRAM_REAL_SEND_RISK,
        NonExecutionBoardRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        NonExecutionBoardRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        NonExecutionBoardRiskFlag.PAPER_ADMISSION_RISK,
        NonExecutionBoardRiskFlag.ACTIVATION_ALLOWED_RISK,
        NonExecutionBoardRiskFlag.ADMISSION_ALLOWED_RISK,
        NonExecutionBoardRiskFlag.TRANSITION_ALLOWED_RISK,
        NonExecutionBoardRiskFlag.ORDER_CREATED_RISK,
        NonExecutionBoardRiskFlag.MUTATION_DETECTED_RISK,
        NonExecutionBoardRiskFlag.RUNTIME_MAP_REPLAY_FAILED,
        NonExecutionBoardRiskFlag.RUNTIME_ROUTE_PERMISSION_RISK,
        NonExecutionBoardRiskFlag.DANGEROUS_RUNTIME_ROUTE_ALLOWED,
        NonExecutionBoardRiskFlag.NON_EXECUTION_SEAL_HASH_MISMATCH,
        NonExecutionBoardRiskFlag.NON_EXECUTION_SEAL_CONFIRMATION_FAILED,
        NonExecutionBoardRiskFlag.NON_EXECUTION_BOARD_GATE_FAILED,
        NonExecutionBoardRiskFlag.NON_EXECUTION_BOARD_ASSERTION_FAILED,
        NonExecutionBoardRiskFlag.SECRET_RISK
    ]
    for f in flags:
        if f in blocking_types:
            return True
    return False

def validate_non_execution_board_safety(board: Optional[PaperReadinessNonExecutionBoard] = None, replay_result: Optional[RuntimeMapReplayResult] = None, seal_audit: Optional[NonExecutionSealIntegrityAudit] = None) -> List[str]:
    flags = collect_non_execution_board_safety_flags(board, replay_result, seal_audit)
    errors = []
    if non_execution_board_has_blocking_flags(flags):
        for f in flags:
            errors.append(f"Blocking flag detected: {f.value}")
    return errors

def non_execution_board_safety_summary(flags: List[NonExecutionBoardRiskFlag]) -> Dict[str, Any]:
    return {
        "safe": not non_execution_board_has_blocking_flags(flags),
        "flags": [f.value for f in flags]
    }

def non_execution_board_safety_validator_to_text(payload: Dict[str, Any]) -> str:
    lines = ["--- BOARD SAFETY VALIDATOR ---"]
    lines.append(f"Safe: {payload.get('safe')}")
    if payload.get("flags"):
        lines.append("Flags:")
        for f in payload.get("flags"):
            lines.append(f"  - {f}")
    return "\n".join(lines)
