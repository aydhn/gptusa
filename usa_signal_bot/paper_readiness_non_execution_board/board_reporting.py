from typing import Any, Dict
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    RuntimeRouteReplayItem,
    RuntimeMapReplayPlan,
    RuntimeMapReplayResult,
    NonExecutionSealIntegrityItem,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardGate,
    NonExecutionBoardAssertion,
    PaperReadinessNonExecutionBoard,
    NonExecutionBoardAuditEntry,
    NonExecutionBoardFullReview
)

def runtime_route_replay_item_to_text(item: RuntimeRouteReplayItem) -> str:
    return f"Route: {item.route_name} | Decision: {item.decision.value} | Blocked: {item.blocked}"

def runtime_map_replay_plan_to_text(item: RuntimeMapReplayPlan) -> str:
    from usa_signal_bot.paper_readiness_non_execution_board.runtime_map_replay_plan import runtime_map_replay_plan_to_text as _r
    return _r(item)

def runtime_map_replay_result_to_text(item: RuntimeMapReplayResult) -> str:
    return f"Result: {item.outcome.value} | Passed: {item.passed} | Dangerous Allowed: {item.dangerous_allowed_count}"

def non_execution_seal_integrity_item_to_text(item: NonExecutionSealIntegrityItem) -> str:
    return f"Field: {item.field_name} | Matched: {item.matched}"

def non_execution_seal_integrity_audit_to_text(item: NonExecutionSealIntegrityAudit, limit: int = 100) -> str:
    from usa_signal_bot.paper_readiness_non_execution_board.seal_integrity_audit import seal_integrity_audit_to_text as _s
    return _s(item, limit)

def non_execution_board_gate_to_text(item: NonExecutionBoardGate) -> str:
    return f"Gate: {item.gate_name} | Status: {item.status.value}"

def non_execution_board_assertion_to_text(item: NonExecutionBoardAssertion) -> str:
    return f"Assertion: {item.assertion_name} | Status: {item.status.value}"

def paper_readiness_non_execution_board_to_text(item: PaperReadinessNonExecutionBoard, limit: int = 100) -> str:
    from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board import non_execution_board_to_text as _b
    return _b(item, limit)

def non_execution_board_audit_entry_to_text(item: NonExecutionBoardAuditEntry) -> str:
    return f"Audit: {item.action} on {item.entity_type} -> {item.decision}"

def non_execution_board_full_review_to_text(item: NonExecutionBoardFullReview, limit: int = 100) -> str:
    from usa_signal_bot.paper_readiness_non_execution_board.board_report import non_execution_board_full_review_to_text as _f
    return _f(item, limit)

def non_execution_board_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in summary.items()])

def non_execution_board_limitations_text() -> str:
    from usa_signal_bot.paper_readiness_non_execution_board.board_report import non_execution_board_limitations_text as _l
    return _l()
