from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    NonExecutionBoardFullReview,
    PaperReadinessNonExecutionBoard,
    RuntimeMapReplayResult,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardReportType,
    create_non_execution_board_full_review_id,
    _now_utc_str
)

def build_non_execution_board_full_review(dossier_payload: Dict[str, Any]) -> NonExecutionBoardFullReview:
    # This acts as a dummy/stub wrapper, usually called after all components are built
    # The actual construction happens via build_non_execution_board_review_from_parts
    pass

def build_non_execution_board_review_from_parts(
    board: PaperReadinessNonExecutionBoard,
    replay_result: Optional[RuntimeMapReplayResult] = None,
    seal_audit: Optional[NonExecutionSealIntegrityAudit] = None,
    replay_plan = None,
    route_items = None,
    audit_entries = None
) -> NonExecutionBoardFullReview:
    return NonExecutionBoardFullReview(
        review_id=create_non_execution_board_full_review_id(),
        created_at_utc=_now_utc_str(),
        report_type=NonExecutionBoardReportType.FULL_NON_EXECUTION_BOARD_REVIEW,
        boards=[board],
        runtime_replay_plans=[replay_plan] if replay_plan else [],
        runtime_replay_results=[replay_result] if replay_result else [],
        runtime_route_replay_items=route_items if route_items else [],
        seal_integrity_audits=[seal_audit] if seal_audit else [],
        gates=board.gates,
        assertions=board.assertions,
        audit_entries=audit_entries if audit_entries else [],
        output_paths={},
        warnings=[],
        errors=[]
    )

def non_execution_board_full_review_summary(review: NonExecutionBoardFullReview) -> Dict[str, Any]:
    board = review.boards[0] if review.boards else None
    return {
        "review_id": review.review_id,
        "type": review.report_type.value,
        "board_decision": board.decision.value if board else "UNKNOWN",
        "sealed": board.sealed if board else False,
        "activation_denied": board.activation_denied if board else False
    }

def non_execution_board_limitations_text() -> str:
    return """
--- NON-EXECUTION BOARD LIMITATIONS ---
- No broker/live/demo order.
- No active paper enable.
- No paper admission.
- No real paper mutation.
- No paper order.
- No Telegram real send.
- No production config patch.
- Runtime map replay is metadata-only.
- Non-execution seal integrity audit is metadata-only.
- Non-execution board is not activation.
- Not investment advice.
"""

def non_execution_board_full_review_to_text(review: NonExecutionBoardFullReview, limit: int = 100) -> str:
    summary = non_execution_board_full_review_summary(review)
    lines = [
        "--- FULL NON-EXECUTION BOARD REVIEW ---",
        f"Review ID: {summary['review_id']}",
        f"Decision: {summary['board_decision']}",
        f"Sealed: {summary['sealed']}",
        non_execution_board_limitations_text()
    ]
    return "\n".join(lines)
