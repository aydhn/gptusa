
from typing import Any, List, Optional
import datetime
from usa_signal_bot.core.enums import PaperReadinessBoardRiskFlag, PaperReadinessBoardReportType
from usa_signal_bot.paper_readiness_board.readiness_board_models import (
    PaperReadinessBoardAuditEntry, PaperReadinessBoardReview, WriteBlockedRuntimeAdapterProof,
    ActivationFirewallEvent, PaperReadinessBoardFullReview, create_board_audit_id, create_board_full_review_id
)

def create_paper_readiness_board_audit_entry(entity_type: str, entity_id: str, action: str, rationale: str, decision: str = None, evidence_refs: List[str] = None, risk_flags: List[PaperReadinessBoardRiskFlag] = None) -> PaperReadinessBoardAuditEntry:
    return PaperReadinessBoardAuditEntry(
        audit_id=create_board_audit_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[], errors=[]
    )

def audit_entry_from_board_review(review: PaperReadinessBoardReview) -> PaperReadinessBoardAuditEntry:
    return create_paper_readiness_board_audit_entry("BoardReview", review.board_review_id, "REVIEW", "Board review completed", review.decision.value, review.evidence_refs, review.safety_flags)

def audit_entry_from_write_block_proof(proof: WriteBlockedRuntimeAdapterProof) -> PaperReadinessBoardAuditEntry:
    return create_paper_readiness_board_audit_entry("WriteBlockProof", proof.proof_id, "PROOF", "Write block proof completed", proof.status.value)

def audit_entry_from_activation_firewall_events(events: List[ActivationFirewallEvent]) -> PaperReadinessBoardAuditEntry:
    return create_paper_readiness_board_audit_entry("FirewallEvents", "events", "EVALUATE", "Evaluated firewall events", "DENY")

def append_board_audit_entry(entries: List[PaperReadinessBoardAuditEntry], entry: PaperReadinessBoardAuditEntry) -> List[PaperReadinessBoardAuditEntry]:
    entries.append(entry)
    return entries

def board_audit_summary(entries: List[PaperReadinessBoardAuditEntry]) -> dict:
    return {"audit_count": len(entries)}

def board_audit_to_text(entries: List[PaperReadinessBoardAuditEntry], limit: int = 100) -> str:
    return "\n".join([f"{e.action} - {e.decision}" for e in entries[:limit]])

def build_paper_readiness_board_review(confirmation_payload: dict) -> PaperReadinessBoardReview:
    from usa_signal_bot.paper_readiness_board.board_decision import PaperReadinessBoardDecisionEngine
    from usa_signal_bot.paper_readiness_board.board_gates import default_paper_readiness_board_gates
    engine = PaperReadinessBoardDecisionEngine()
    gates = default_paper_readiness_board_gates(confirmation_payload)
    return engine.decide(confirmation_payload, gates)

def build_paper_readiness_board_full_review(board_review: PaperReadinessBoardReview, write_block_proof: WriteBlockedRuntimeAdapterProof = None, activation_events: List[ActivationFirewallEvent] = None) -> PaperReadinessBoardFullReview:
    return PaperReadinessBoardFullReview(
        review_id=create_board_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        report_type=PaperReadinessBoardReportType.FULL_PAPER_READINESS_BOARD_REVIEW,
        board_reviews=[board_review],
        gates=board_review.gates,
        write_block_events=[],
        write_block_proofs=[write_block_proof] if write_block_proof else [],
        activation_firewall_rules=[],
        activation_firewall_events=activation_events or [],
        audit_entries=[audit_entry_from_board_review(board_review)],
        output_paths={},
        warnings=[], errors=[]
    )

def paper_readiness_board_full_review_summary(review: PaperReadinessBoardFullReview) -> dict:
    return {"status": review.board_reviews[0].status.value if review.board_reviews else "UNKNOWN"}

def paper_readiness_board_limitations_text() -> str:
    return (
        "LIMITATIONS: no broker/live/demo order, no active paper enable, "
        "no real paper mutation, no Telegram real send, no production config patch, "
        "board PASS is not activation, write-blocked adapter is read-only, "
        "activation firewall denies activation, not investment advice."
    )

def paper_readiness_board_full_review_to_text(review: PaperReadinessBoardFullReview, limit: int = 100) -> str:
    return f"Full Review: {paper_readiness_board_full_review_summary(review)}\n{paper_readiness_board_limitations_text()}"
