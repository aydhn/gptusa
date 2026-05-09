from dataclasses import dataclass, field
from typing import Any
import uuid
import datetime
import json
from pathlib import Path

@dataclass
class IncidentAuditEvent:
    event_id: str
    timestamp_utc: str
    event_type: str
    status: str
    message: str
    incident_id: str | None = None
    path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

def create_incident_audit_event(event_type: str, status: str, message: str, incident_id: str | None = None, path: str | None = None) -> IncidentAuditEvent:

    # Redact path heuristically if it looks sensitive
    safe_path = path
    if path and any(x in path.lower() for x in ["secret", "token", "key"]):
         safe_path = "[REDACTED_SENSITIVE_PATH]"

    return IncidentAuditEvent(
        event_id=f"audit_{uuid.uuid4().hex[:8]}",
        timestamp_utc=datetime.datetime.utcnow().isoformat() + "Z",
        event_type=event_type,
        status=status,
        message=message,
        incident_id=incident_id,
        path=safe_path
    )

def incident_audit_event_to_dict(event: IncidentAuditEvent) -> dict:
    return {
        "event_id": event.event_id,
        "timestamp_utc": event.timestamp_utc,
        "event_type": event.event_type,
        "status": event.status,
        "message": event.message,
        "incident_id": event.incident_id,
        "path": event.path,
        "metadata": event.metadata
    }

def write_incident_audit_jsonl(path: Path, events: list[IncidentAuditEvent]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(incident_audit_event_to_dict(event)) + "\n")
    return path

def read_incident_audit_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    events = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    if limit is not None:
        return events[-limit:]
    return events

def incident_audit_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    summary = {
        "total_events": len(events),
        "by_type": {},
        "by_status": {}
    }
    for e in events:
        t = e.get("event_type", "unknown")
        s = e.get("status", "unknown")
        summary["by_type"][t] = summary["by_type"].get(t, 0) + 1
        summary["by_status"][s] = summary["by_status"].get(s, 0) + 1

    return summary

def incident_audit_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [f"Total Events: {summary['total_events']}"]
    lines.append("By Type:")
    for k, v in summary["by_type"].items():
         lines.append(f"  {k}: {v}")
    lines.append("By Status:")
    for k, v in summary["by_status"].items():
         lines.append(f"  {k}: {v}")
    return "\n".join(lines)
