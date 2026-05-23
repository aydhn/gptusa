
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_safe_gate.paper_safe_gate_models import (
    PaperSafeGateFullReview, PaperSafeGateReportType, FinalPaperSafeGate,
    BoundaryCertificateReplayResult, FrozenEvidenceIntegrityAudit,
    create_paper_safe_full_review_id, utcnow_iso
)

def build_paper_safe_review_from_parts(gate: FinalPaperSafeGate, replay_result: Optional[BoundaryCertificateReplayResult] = None, integrity_audit: Optional[FrozenEvidenceIntegrityAudit] = None) -> PaperSafeGateFullReview:
    return PaperSafeGateFullReview(
        review_id=create_paper_safe_full_review_id(),
        created_at_utc=utcnow_iso(),
        report_type=PaperSafeGateReportType.FULL_PAPER_SAFE_GATE_REVIEW,
        gates=[gate],
        replay_plans=[],
        replay_results=[replay_result] if replay_result else [],
        integrity_audits=[integrity_audit] if integrity_audit else [],
        rules=gate.rules,
        assertions=gate.assertions,
        audit_entries=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def build_paper_safe_gate_full_review(boundary_payload: Dict[str, Any]) -> PaperSafeGateFullReview:
    from usa_signal_bot.paper_safe_gate.final_paper_safe_gate import build_default_final_paper_safe_gate
    gate = build_default_final_paper_safe_gate()
    return build_paper_safe_review_from_parts(gate)

def paper_safe_gate_full_review_summary(review: PaperSafeGateFullReview) -> Dict[str, Any]:
    return {"review_id": review.review_id}

def paper_safe_gate_limitations_text() -> str:
    return "Paper-safe gate is metadata-only. Not investment advice. No active broker execution."

def paper_safe_gate_full_review_to_text(review: PaperSafeGateFullReview, limit: int = 100) -> str:
    return f"Paper Safe Review: {review.review_id}"
