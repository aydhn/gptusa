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
    return f"Checkpoint History ({status})\nTotal Entries: {len(entries)}\nWarnings: {len(checkpoint_history_warnings(entries))}"
