import os
from pathlib import Path

FILES = {}

FILES["usa_signal_bot/paper_observation/checkpoint_history.py"] = """\
from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import CheckpointHistoryEntry, CheckpointHistoryStatus, create_checkpoint_history_id
import datetime

def build_checkpoint_history_entry(checkpoint_payload: dict[str, Any]) -> CheckpointHistoryEntry:
    return CheckpointHistoryEntry(
        history_id=create_checkpoint_history_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        checkpoint_id=checkpoint_payload.get("checkpoint_id"),
        session_id=checkpoint_payload.get("session_id"),
        candidate_id=checkpoint_payload.get("candidate_id"),
        ticket_id=checkpoint_payload.get("ticket_id"),
        checkpoint_status=checkpoint_payload.get("status", "UNKNOWN"),
        reviewer_notes=checkpoint_payload.get("reviewer_notes"),
        reviewer_id=checkpoint_payload.get("reviewer_id"),
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_config_patch=False,
        warnings=[],
        errors=[],
        metadata=checkpoint_payload.get("metadata", {})
    )

def build_checkpoint_history(checkpoints: List[dict[str, Any]]) -> List[CheckpointHistoryEntry]:
    return [build_checkpoint_history_entry(cp) for cp in checkpoints]

def checkpoint_history_status(entries: List[CheckpointHistoryEntry]) -> CheckpointHistoryStatus:
    if not entries:
        return CheckpointHistoryStatus.EMPTY
    all_reviewed = all(e.checkpoint_status in ["REVIEWED", "APPROVED", "REJECTED"] for e in entries)
    if all_reviewed:
        return CheckpointHistoryStatus.COMPLETE
    return CheckpointHistoryStatus.PARTIAL

def checkpoint_history_warnings(entries: List[CheckpointHistoryEntry]) -> List[str]:
    warnings = []
    if not entries:
        warnings.append("No checkpoints in history.")
    for e in entries:
        if e.checkpoint_status == "WAITING_REVIEW":
            warnings.append(f"Checkpoint {e.checkpoint_id} is waiting for review.")
    return warnings

def checkpoint_history_summary(entries: List[CheckpointHistoryEntry]) -> dict[str, Any]:
    return {
        "total_checkpoints": len(entries),
        "status": checkpoint_history_status(entries),
        "waiting_review_count": sum(1 for e in entries if e.checkpoint_status == "WAITING_REVIEW")
    }

def checkpoint_history_to_text(entries: List[CheckpointHistoryEntry], limit: int = 100) -> str:
    status = checkpoint_history_status(entries)
    return f"Checkpoint History ({status})\\nTotal Entries: {len(entries)}\\nWarnings: {len(checkpoint_history_warnings(entries))}"
"""

FILES["usa_signal_bot/paper_observation/checkpoint_timeline.py"] = """\
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
    return f"Checkpoint Timeline\\nLatest: {latest_checkpoint(entries)}\\nIs Stale: {stale}"
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
