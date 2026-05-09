import json
import uuid
import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class CleanupAuditEvent:
    event_id: str
    timestamp_utc: str
    event_type: str
    path: str | None
    action: str
    status: str
    bytes_affected: int
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)

def create_cleanup_audit_event(event_type: str, action: str, status: str, path: str | None = None, bytes_affected: int = 0, message: str = "") -> CleanupAuditEvent:
    from usa_signal_bot.retention.protected_paths import is_secret_like_path

    clean_path = path
    if path and is_secret_like_path(Path(path)):
         clean_path = "<REDACTED_SECRET_PATH>"

    return CleanupAuditEvent(
        event_id=str(uuid.uuid4()),
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        event_type=event_type,
        path=clean_path,
        action=action,
        status=status,
        bytes_affected=bytes_affected,
        message=message
    )

def cleanup_audit_event_to_dict(event: CleanupAuditEvent) -> dict:
    import dataclasses
    return dataclasses.asdict(event)

def write_cleanup_audit_jsonl(path: Path, events: list[CleanupAuditEvent]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(cleanup_audit_event_to_dict(event)) + "\n")
    return path

def read_cleanup_audit_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    events = []
    if not path.exists():
        return events
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if limit is not None:
         return events[-limit:]
    return events

def cleanup_audit_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    summary = {
        "total_events": len(events),
        "deleted_count": sum(1 for e in events if e.get("status") == "DELETED"),
        "skipped_count": sum(1 for e in events if e.get("status") == "SKIPPED"),
        "failed_count": sum(1 for e in events if e.get("status") == "FAILED"),
        "total_bytes_freed": sum(e.get("bytes_affected", 0) for e in events if e.get("status") == "DELETED")
    }
    return summary

def cleanup_audit_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "Cleanup Audit Summary:",
        f"Total Events: {summary['total_events']}",
        f"Deleted: {summary['deleted_count']}",
        f"Skipped: {summary['skipped_count']}",
        f"Failed: {summary['failed_count']}",
        f"Total Bytes Freed: {summary['total_bytes_freed'] / (1024*1024):.2f} MB"
    ]
    return "\n".join(lines)
