from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import CheckpointHistoryEntry
import datetime

def sort_checkpoint_history(entries: List[CheckpointHistoryEntry]) -> List[CheckpointHistoryEntry]:
    return sorted(entries, key=lambda x: x.created_at_utc)

def latest_checkpoint(entries: List[CheckpointHistoryEntry]) -> CheckpointHistoryEntry | None:
    if not entries:
        return None
    sorted_entries = sort_checkpoint_history(entries)
    return sorted_entries[-1]

def checkpoint_timeline_has_stale_review(entries: List[CheckpointHistoryEntry], max_age_days: int = 7) -> bool:
    latest = latest_checkpoint(entries)
    if not latest:
        return False
    try:
        dt = datetime.datetime.fromisoformat(latest.created_at_utc.replace("Z", "+00:00"))
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - dt).days > max_age_days
    except Exception:
        return True

def checkpoint_timeline_required_followups(entries: List[CheckpointHistoryEntry]) -> List[str]:
    followups = []
    if checkpoint_timeline_has_stale_review(entries):
        followups.append("Requires fresh manual review due to stale checkpoint.")
    for e in entries:
        if e.checkpoint_status == "WAITING_REVIEW":
            followups.append(f"Complete review for checkpoint {e.checkpoint_id}.")
    return followups

def checkpoint_timeline_summary(entries: List[CheckpointHistoryEntry]) -> dict[str, Any]:
    latest = latest_checkpoint(entries)
    return {
        "latest_checkpoint_id": latest.checkpoint_id if latest else None,
        "is_stale": checkpoint_timeline_has_stale_review(entries),
        "required_followups": len(checkpoint_timeline_required_followups(entries))
    }

def checkpoint_timeline_to_text(entries: List[CheckpointHistoryEntry], limit: int = 100) -> str:
    stale = "Yes" if checkpoint_timeline_has_stale_review(entries) else "No"
    return f"Checkpoint Timeline\nLatest: {latest_checkpoint(entries)}\nIs Stale: {stale}"
