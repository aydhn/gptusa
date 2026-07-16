import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from usa_signal_bot.core.enums import ResourceProfileScope
from usa_signal_bot.profiling.resource_timer import current_utc_iso

@dataclass
class ProfilingAuditEvent:
    event_id: str
    timestamp_utc: str
    event_type: str
    status: str
    scope: ResourceProfileScope | None
    profile_id: str | None
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProfilingAuditParams:
    event_type: str
    status: str
    message: str
    scope: ResourceProfileScope | None = None
    profile_id: str | None = None
    metadata: dict[str, Any] | None = None

def create_profiling_audit_event(
    params: ProfilingAuditParams
) -> ProfilingAuditEvent:

    safe_metadata = dict(params.metadata) if params.metadata else {}
    for key in ["token", "secret", "api_key", "password"]:
        for k in list(safe_metadata.keys()):
            if key in k.lower():
                safe_metadata[k] = "***REDACTED***"

    return ProfilingAuditEvent(
        event_id=f"prof_audit_{uuid.uuid4().hex[:12]}",
        timestamp_utc=current_utc_iso(),
        event_type=params.event_type,
        status=params.status,
        scope=params.scope,
        profile_id=params.profile_id,
        message=params.message,
        metadata=safe_metadata
    )

def profiling_audit_event_to_dict(event: ProfilingAuditEvent) -> dict:
    return {
        "event_id": event.event_id,
        "timestamp_utc": event.timestamp_utc,
        "event_type": event.event_type,
        "status": event.status,
        "scope": event.scope.value if event.scope else None,
        "profile_id": event.profile_id,
        "message": event.message,
        "metadata": event.metadata
    }

def write_profiling_audit_jsonl(path: Path, events: list[ProfilingAuditEvent]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'a', encoding='utf-8') as f:
        for event in events:
            f.write(json.dumps(profiling_audit_event_to_dict(event)) + '\n')

    return path

def read_profiling_audit_jsonl(path: Path, limit: int | None = None) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    if limit is not None:
        records = records[-limit:]

    return records

def profiling_audit_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_events": len(events),
        "latest_event_time": events[-1].get("timestamp_utc") if events else None
    }

def profiling_audit_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "Profiling Audit Summary:",
        f"  Total Events: {summary['total_events']}",
        f"  Latest Event: {summary['latest_event_time'] or 'None'}"
    ]
    return "\n".join(lines)
