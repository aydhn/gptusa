from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    NonExecutionBoardAuditEntry,
    PaperReadinessNonExecutionBoard,
    RuntimeMapReplayResult,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardRiskFlag,
    create_non_execution_board_audit_id,
    _now_utc_str
)

def create_non_execution_board_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
    risk_flags: Optional[List[NonExecutionBoardRiskFlag]] = None
) -> NonExecutionBoardAuditEntry:
    return NonExecutionBoardAuditEntry(
        audit_id=create_non_execution_board_audit_id(),
        created_at_utc=_now_utc_str(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[],
        metadata={}
    )

def audit_entry_from_non_execution_board(board: PaperReadinessNonExecutionBoard) -> NonExecutionBoardAuditEntry:
    return create_non_execution_board_audit_entry(
        entity_type="PaperReadinessNonExecutionBoard",
        entity_id=board.board_id,
        action="evaluate_board",
        rationale="Final non-execution board evaluation",
        decision=board.decision.value,
        evidence_refs=[board.source_paper_safe_dossier_id] if board.source_paper_safe_dossier_id else [],
        risk_flags=board.safety_flags
    )

def audit_entry_from_runtime_map_replay(result: RuntimeMapReplayResult) -> NonExecutionBoardAuditEntry:
    return create_non_execution_board_audit_entry(
        entity_type="RuntimeMapReplayResult",
        entity_id=result.replay_result_id,
        action="replay_runtime_map",
        rationale="Simulate runtime map execution paths",
        decision=result.status.value,
        evidence_refs=[result.replay_plan_id] if result.replay_plan_id else [],
        risk_flags=result.risk_flags
    )

def audit_entry_from_seal_integrity_audit(audit: NonExecutionSealIntegrityAudit) -> NonExecutionBoardAuditEntry:
    return create_non_execution_board_audit_entry(
        entity_type="NonExecutionSealIntegrityAudit",
        entity_id=audit.audit_id,
        action="audit_seal_integrity",
        rationale="Verify non-execution seal integrity and hashes",
        decision=audit.decision.value,
        evidence_refs=[audit.source_seal_id] if audit.source_seal_id else [],
        risk_flags=audit.risk_flags
    )

def append_non_execution_board_audit_entry(entries: List[NonExecutionBoardAuditEntry], entry: NonExecutionBoardAuditEntry) -> List[NonExecutionBoardAuditEntry]:
    # In a real app we might append to a file directly, here we just append to list
    entries.append(entry)
    return entries

def non_execution_board_audit_summary(entries: List[NonExecutionBoardAuditEntry]) -> Dict[str, Any]:
    return {
        "entry_count": len(entries),
        "actions": list(set([e.action for e in entries]))
    }

def non_execution_board_audit_to_text(entries: List[NonExecutionBoardAuditEntry], limit: int = 100) -> str:
    summary = non_execution_board_audit_summary(entries)
    lines = ["--- BOARD AUDIT TRAIL ---"]
    lines.append(f"Total Entries: {summary['entry_count']}")
    for e in entries[:limit]:
        lines.append(f"  [{e.created_at_utc}] {e.entity_type} ({e.action}): {e.decision}")
    return "\n".join(lines)
