from typing import Any, Dict, List
import hashlib
import json
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    PaperReadinessNonExecutionBoard,
    PaperReadinessNonExecutionBoardStatus,
    PaperReadinessNonExecutionBoardDecision,
    NonExecutionBoardGate,
    NonExecutionBoardGateStatus,
    NonExecutionBoardAssertion,
    NonExecutionBoardAssertionStatus,
    NonExecutionBoardRiskFlag,
    RuntimeMapReplayResult,
    create_non_execution_board_id,
    _now_utc_str,
    validate_paper_readiness_non_execution_board
)
from usa_signal_bot.paper_readiness_non_execution_board.dossier_ingestion import extract_dossier_candidate_id
from usa_signal_bot.paper_readiness_non_execution_board.eligibility_checker import evaluate_non_execution_board_eligibility

def build_paper_readiness_non_execution_board(dossier_payload: Dict[str, Any]) -> PaperReadinessNonExecutionBoard:
    board = build_default_non_execution_board(extract_dossier_candidate_id(dossier_payload))
    board.source_paper_safe_dossier_id = dossier_payload.get("dossier_id")

    eligibility = evaluate_non_execution_board_eligibility(dossier_payload)
    if eligibility == PaperReadinessNonExecutionBoardDecision.PASS_TO_NON_EXECUTION_BOARD_DOSSIER:
        board.decision = PaperReadinessNonExecutionBoardDecision.PASS_TO_NON_EXECUTION_BOARD_DOSSIER
        board.status = PaperReadinessNonExecutionBoardStatus.VALIDATED_NON_EXECUTION
    else:
        board.decision = eligibility
        board.status = PaperReadinessNonExecutionBoardStatus.BLOCKED if eligibility in [PaperReadinessNonExecutionBoardDecision.BLOCK, PaperReadinessNonExecutionBoardDecision.REJECT] else PaperReadinessNonExecutionBoardStatus.REQUEST_CHANGES

    validate_paper_readiness_non_execution_board(board)
    return board

def build_default_non_execution_board(candidate_id: str | None = None) -> PaperReadinessNonExecutionBoard:
    return PaperReadinessNonExecutionBoard(
        board_id=create_non_execution_board_id(),
        created_at_utc=_now_utc_str(),
        status=PaperReadinessNonExecutionBoardStatus.CREATED,
        decision=PaperReadinessNonExecutionBoardDecision.UNKNOWN,
        candidate_id=candidate_id,
        source_paper_safe_dossier_review_id=None,
        source_paper_safe_dossier_id=None,
        source_runtime_map_id=None,
        source_non_execution_seal_id=None,
        runtime_replay_result=None,
        seal_integrity_audit=None,
        gates=[],
        assertions=[],
        board_hash=None,
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        admission_allowed=False,
        transition_allowed=False,
        paper_safe_dossier_valid=True,
        non_execution_confirmed=True,
        runtime_map_safe=True,
        all_writes_blocked=True,
        order_created=False,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def stable_non_execution_board_hash(payload: Dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def collect_non_execution_board_safety_flags(dossier_payload: Dict[str, Any], gates: List[NonExecutionBoardGate], assertions: List[NonExecutionBoardAssertion]) -> List[NonExecutionBoardRiskFlag]:
    flags = set()
    for g in gates:
        for f in g.risk_flags:
            flags.add(f)

    for a in assertions:
        for f in a.risk_flags:
            flags.add(f)

    if dossier_payload.get("activation_allowed"):
        flags.add(NonExecutionBoardRiskFlag.ACTIVATION_ALLOWED_RISK)
    if dossier_payload.get("admission_allowed"):
        flags.add(NonExecutionBoardRiskFlag.ADMISSION_ALLOWED_RISK)
    if dossier_payload.get("order_created"):
        flags.add(NonExecutionBoardRiskFlag.ORDER_CREATED_RISK)
    if dossier_payload.get("mutation_detected"):
        flags.add(NonExecutionBoardRiskFlag.MUTATION_DETECTED_RISK)

    return list(flags)

def non_execution_board_summary(board: PaperReadinessNonExecutionBoard) -> Dict[str, Any]:
    return {
        "id": board.board_id,
        "status": board.status.value,
        "decision": board.decision.value,
        "sealed": board.sealed,
        "activation_denied": board.activation_denied
    }

def non_execution_board_to_text(board: PaperReadinessNonExecutionBoard, limit: int = 100) -> str:
    summary = non_execution_board_summary(board)
    lines = [
        "--- NON-EXECUTION BOARD ---",
        f"ID: {summary['id']}",
        f"Status: {summary['status']}",
        f"Decision: {summary['decision']}",
        f"Sealed: {summary['sealed']}",
        f"Activation Denied: {summary['activation_denied']}"
    ]
    if board.safety_flags:
        lines.append("Safety Flags:")
        for f in board.safety_flags:
            lines.append(f"  - {f.value}")
    return "\n".join(lines)
