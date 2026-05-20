from typing import Any, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    DryRunBridgeContext,
    HumanReviewCheckpoint,
    HumanReviewCheckpointStatus,
    create_human_review_checkpoint_id
)

def build_human_review_checkpoint(context: DryRunBridgeContext, session_id: Optional[str] = None) -> HumanReviewCheckpoint:
    return HumanReviewCheckpoint(
        checkpoint_id=create_human_review_checkpoint_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        session_id=session_id,
        candidate_id=context.candidate_id,
        ticket_id=context.ticket_id,
        status=HumanReviewCheckpointStatus.REQUIRED,
        required=True,
        reviewer_notes=None,
        reviewer_id=None,
        reviewed_at_utc=None,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_config_patch=False,
        warnings=["Manual review required. Acceptance does not enable active paper."],
        errors=[],
        metadata={}
    )

def update_human_review_checkpoint_notes(checkpoint: HumanReviewCheckpoint, reviewer_notes: str, reviewer_id: Optional[str] = None) -> HumanReviewCheckpoint:
    checkpoint.reviewer_notes = reviewer_notes
    checkpoint.reviewer_id = reviewer_id
    checkpoint.reviewed_at_utc = datetime.now(timezone.utc).isoformat()
    if checkpoint.status == HumanReviewCheckpointStatus.REQUIRED:
        checkpoint.status = HumanReviewCheckpointStatus.REVIEWED_WITH_NOTES
    return checkpoint

def mark_checkpoint_observation_only(checkpoint: HumanReviewCheckpoint) -> HumanReviewCheckpoint:
    checkpoint.status = HumanReviewCheckpointStatus.ACCEPTED_FOR_OBSERVATION_ONLY
    checkpoint.reviewed_at_utc = datetime.now(timezone.utc).isoformat()
    return checkpoint

def reject_human_review_checkpoint(checkpoint: HumanReviewCheckpoint, reason: str) -> HumanReviewCheckpoint:
    checkpoint.status = HumanReviewCheckpointStatus.REJECTED
    checkpoint.reviewer_notes = f"Rejected: {reason}"
    checkpoint.reviewed_at_utc = datetime.now(timezone.utc).isoformat()
    return checkpoint

def human_review_checkpoint_summary(checkpoint: HumanReviewCheckpoint) -> dict[str, Any]:
    return {
        "checkpoint_id": checkpoint.checkpoint_id,
        "status": checkpoint.status.value,
        "required": checkpoint.required,
        "has_notes": bool(checkpoint.reviewer_notes)
    }

def human_review_checkpoint_to_text(checkpoint: HumanReviewCheckpoint) -> str:
    return f"Human Checkpoint {checkpoint.checkpoint_id} (Status: {checkpoint.status.value})"
