from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_final_handoff.final_handoff_models import (
    FinalHandoffReview,
    SealedReadinessArchiveManifest,
    ArchiveIntegrityReport,
    PrePaperGovernanceCheckpoint,
    FinalHandoffFullReview,
    create_final_handoff_review_id,
    create_final_handoff_full_review_id,
    _ts
)
from usa_signal_bot.core.enums import (
    FinalHandoffReviewStatus,
    FinalHandoffDecision,
    FinalHandoffReportType
)
from usa_signal_bot.paper_final_handoff.eligibility_checker import evaluate_final_handoff_eligibility, final_handoff_safety_flags_from_readiness, final_handoff_status_from_decision
from usa_signal_bot.paper_final_handoff.archive_manifest import build_final_handoff_evidence_refs

def build_final_handoff_review(readiness_payload: Dict[str, Any]) -> FinalHandoffReview:
    decision = evaluate_final_handoff_eligibility(readiness_payload)
    status = final_handoff_status_from_decision(decision)
    flags = final_handoff_safety_flags_from_readiness(readiness_payload)
    evidence = build_final_handoff_evidence_refs(readiness_payload)

    return FinalHandoffReview(
        handoff_review_id=create_final_handoff_review_id(),
        created_at_utc=_ts(),
        status=status,
        candidate_id=readiness_payload.get("candidate_id"),
        source_handoff_id=readiness_payload.get("handoff_id"),
        source_rehearsal_run_id=readiness_payload.get("rehearsal_run_id"),
        source_final_lock_id=readiness_payload.get("final_lock_id"),
        evidence_refs=evidence,
        decision=decision,
        safety_flags=flags,
        manual_review_required=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        warnings=[],
        errors=[]
    )

def build_final_handoff_full_review(handoff_review: FinalHandoffReview, manifest: Optional[SealedReadinessArchiveManifest] = None, integrity_report: Optional[ArchiveIntegrityReport] = None, checkpoint: Optional[PrePaperGovernanceCheckpoint] = None) -> FinalHandoffFullReview:
    return FinalHandoffFullReview(
        review_id=create_final_handoff_full_review_id(),
        created_at_utc=_ts(),
        report_type=FinalHandoffReportType.FULL_FINAL_HANDOFF_REVIEW,
        handoff_reviews=[handoff_review],
        archive_manifests=[manifest] if manifest else [],
        integrity_reports=[integrity_report] if integrity_report else [],
        checkpoints=[checkpoint] if checkpoint else [],
        audit_entries=[],
        output_paths={},
        warnings=[],
        errors=[]
    )

def final_handoff_full_review_summary(review: FinalHandoffFullReview) -> Dict[str, Any]:
    return {"id": review.review_id, "reviews": len(review.handoff_reviews)}

def final_handoff_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- No broker/live/demo order.\n"
        "- No active paper enable.\n"
        "- No real paper mutation.\n"
        "- No Telegram real send.\n"
        "- No production config patch.\n"
        "- Sealed archive is not deployment package.\n"
        "- Pre-paper checkpoint is not activation.\n"
        "- Not investment advice."
    )

def final_handoff_full_review_to_text(review: FinalHandoffFullReview, limit: int = 100) -> str:
    return f"FinalHandoffFullReview {review.review_id}:\n{final_handoff_limitations_text()}"
