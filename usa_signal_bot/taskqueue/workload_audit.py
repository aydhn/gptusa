from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import uuid
from datetime import datetime, timezone
from collections import deque

@dataclass
class WorkloadAuditEvent:
    event_id: str
    timestamp_utc: str
    event_type: str
    task_id: Optional[str]
    status: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)

def create_workload_audit_event(event_type: str, status: str, message: str, task_id: Optional[str] = None) -> WorkloadAuditEvent:
    return WorkloadAuditEvent(f"wevt_{uuid.uuid4().hex[:12]}", datetime.now(timezone.utc).isoformat(), event_type, task_id, status, message)

def write_workload_audit_jsonl(path: Path, events: List[WorkloadAuditEvent]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for ev in events: f.write(json.dumps({"event_id": ev.event_id, "timestamp_utc": ev.timestamp_utc, "event_type": ev.event_type, "task_id": ev.task_id, "status": ev.status, "message": ev.message, "metadata": ev.metadata}) + "\n")
    return path

def read_workload_audit_jsonl(path: Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    if not path.exists(): return []
    with open(path, "r", encoding="utf-8") as f:
        if limit is None:
            lines = [json.loads(line) for line in f]
            lines.reverse()
            return lines
        last_lines = deque(f, maxlen=limit)
    res = [json.loads(line) for line in last_lines]
    res.reverse()
    return res

def workload_audit_summary(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    types, statuses = {}, {}
    for ev in events:
        types[ev.get("event_type", "UNKNOWN")] = types.get(ev.get("event_type", "UNKNOWN"), 0) + 1
        statuses[ev.get("status", "UNKNOWN")] = statuses.get(ev.get("status", "UNKNOWN"), 0) + 1
    return {"total_events": len(events), "event_types": types, "event_statuses": statuses}

def workload_audit_summary_to_text(summary: Dict[str, Any]) -> str:
    lines = ["Workload Audit Summary", "=" * 40, f"Total Events: {summary['total_events']}", "\nEvent Types:"]
    for k, v in summary['event_types'].items(): lines.append(f"  - {k}: {v}")
    lines.append("\nEvent Statuses:")
    for k, v in summary['event_statuses'].items(): lines.append(f"  - {k}: {v}")
    return "\n".join(lines)
