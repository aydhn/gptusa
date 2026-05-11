import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from usa_signal_bot.core.enums import RunLockScope

@dataclass
class LockAuditEvent:
    event_id: str
    timestamp_utc: str
    event_type: str
    scope: RunLockScope
    status: str
    lock_id: Optional[str]
    owner_run_id: Optional[str]
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)

def create_lock_audit_event(
    event_type: str,
    scope: RunLockScope,
    status: str,
    lock_id: Optional[str] = None,
    owner_run_id: Optional[str] = None,
    message: str = ""
) -> LockAuditEvent:
    return LockAuditEvent(
        event_id=f"audit_{uuid.uuid4().hex[:8]}",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        event_type=event_type,
        scope=scope,
        status=status,
        lock_id=lock_id,
        owner_run_id=owner_run_id,
        message=message
    )

def lock_audit_event_to_dict(event: LockAuditEvent) -> dict:
    return {
        "event_id": event.event_id,
        "timestamp_utc": event.timestamp_utc,
        "event_type": event.event_type,
        "scope": event.scope.value,
        "status": event.status,
        "lock_id": event.lock_id,
        "owner_run_id": event.owner_run_id,
        "message": event.message,
        "metadata": event.metadata
    }

def write_lock_audit_jsonl(path: Path, events: List[LockAuditEvent]) -> Path:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(lock_audit_event_to_dict(event)) + "\n")
    return path

def read_lock_audit_jsonl(path: Path, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    if limit:
        return records[-limit:]
    return records

def lock_audit_summary(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    summary = {
        "total_events": len(events),
        "types": {},
        "scopes": {},
        "status": {}
    }
    for e in events:
        t = e.get("event_type", "unknown")
        s = e.get("scope", "unknown")
        st = e.get("status", "unknown")

        summary["types"][t] = summary["types"].get(t, 0) + 1
        summary["scopes"][s] = summary["scopes"].get(s, 0) + 1
        summary["status"][st] = summary["status"].get(st, 0) + 1

    return summary

def lock_audit_summary_to_text(summary: Dict[str, Any]) -> str:
    lines = [f"Lock Audit Summary (Total Events: {summary['total_events']})"]
    lines.append("By Type:")
    for k, v in summary["types"].items():
        lines.append(f"  - {k}: {v}")
    lines.append("By Scope:")
    for k, v in summary["scopes"].items():
        lines.append(f"  - {k}: {v}")
    return "\n".join(lines)
