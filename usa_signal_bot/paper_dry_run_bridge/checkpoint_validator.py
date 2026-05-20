from typing import Any, List
from datetime import datetime, timezone
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import (
    HumanReviewCheckpoint,
    HumanReviewCheckpointStatus
)

def validate_checkpoint_safety(checkpoint: HumanReviewCheckpoint) -> List[str]:
    errors = []
    if checkpoint.allows_active_paper:
        errors.append("Checkpoint allows active paper. This is strictly forbidden.")
    if checkpoint.allows_broker_execution:
        errors.append("Checkpoint allows broker execution. This is strictly forbidden.")
    if checkpoint.allows_config_patch:
        errors.append("Checkpoint allows config patch. This is strictly forbidden.")
    return errors

def checkpoint_requires_followup(checkpoint: HumanReviewCheckpoint) -> bool:
    if checkpoint.status in [
        HumanReviewCheckpointStatus.REQUIRED,
        HumanReviewCheckpointStatus.WAITING_REVIEW,
        HumanReviewCheckpointStatus.REQUEST_CHANGES
    ]:
        return True

    if checkpoint.status in [
        HumanReviewCheckpointStatus.REVIEWED_WITH_NOTES,
        HumanReviewCheckpointStatus.ACCEPTED_FOR_OBSERVATION_ONLY
    ] and not checkpoint.reviewer_notes:
        return True

    return False

def checkpoint_expired(checkpoint: HumanReviewCheckpoint, max_age_days: int = 7) -> bool:
    if not checkpoint.created_at_utc:
        return False
    try:
        created = datetime.fromisoformat(checkpoint.created_at_utc)
        age = datetime.now(timezone.utc) - created
        return age.days > max_age_days
    except ValueError:
        return False

def checkpoint_validator_summary(checkpoint: HumanReviewCheckpoint) -> dict[str, Any]:
    return {
        "safe": len(validate_checkpoint_safety(checkpoint)) == 0,
        "requires_followup": checkpoint_requires_followup(checkpoint),
        "expired": checkpoint_expired(checkpoint)
    }

def checkpoint_validator_to_text(payload: dict[str, Any]) -> str:
    safe_str = "Safe" if payload.get("safe", False) else "Unsafe"
    return f"Checkpoint Validation: {safe_str}, Followup: {payload.get('requires_followup', False)}"
