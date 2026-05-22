from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    PrePaperDryRehearsalReview,
    PrePaperDryRehearsalRun,
    ActivationDeniedCheckpoint,
    create_pre_paper_review_id,
    validate_pre_paper_dry_rehearsal_review
)
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_audit import (
    audit_entry_from_pre_paper_run,
    audit_entry_from_activation_checkpoint
)
from usa_signal_bot.core.enums import PrePaperReportType

def pre_paper_rehearsal_limitations_text() -> str:
    return (
        "LIMITATIONS: "
        "No broker/live/demo order. "
        "No active paper enable. "
        "No real paper mutation. "
        "No Telegram real send. "
        "No production config patch. "
        "Mutation firewall is metadata-only. "
        "Activation-denied checkpoint is not activation. "
        "Not investment advice."
    )

def build_pre_paper_dry_rehearsal_review(run: PrePaperDryRehearsalRun, checkpoint: Optional[ActivationDeniedCheckpoint] = None) -> PrePaperDryRehearsalReview:
    audit_entries = [audit_entry_from_pre_paper_run(run)]
    checkpoints = []

    if checkpoint:
        checkpoints.append(checkpoint)
        audit_entries.append(audit_entry_from_activation_checkpoint(checkpoint))

    review = PrePaperDryRehearsalReview(
        review_id=create_pre_paper_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        report_type=PrePaperReportType.FULL_PRE_PAPER_REHEARSAL_REVIEW,
        plans=[run.plan] if run.plan else [],
        runs=[run],
        firewall_events=run.firewall_events,
        activation_checkpoints=checkpoints,
        audit_entries=audit_entries,
        output_paths={},
        warnings=[],
        errors=[]
    )
    validate_pre_paper_dry_rehearsal_review(review)
    return review

def pre_paper_dry_rehearsal_review_summary(review: PrePaperDryRehearsalReview) -> Dict[str, Any]:
    return {
        "review_id": review.review_id,
        "runs": len(review.runs),
        "firewall_events": len(review.firewall_events),
        "checkpoints": len(review.activation_checkpoints)
    }

def pre_paper_dry_rehearsal_review_to_text(review: PrePaperDryRehearsalReview, limit: int = 100) -> str:
    s = pre_paper_dry_rehearsal_review_summary(review)
    return f"Pre-Paper Review {s['review_id']}: {s['runs']} runs, {s['firewall_events']} firewall events, {s['checkpoints']} checkpoints. {pre_paper_rehearsal_limitations_text()}"
