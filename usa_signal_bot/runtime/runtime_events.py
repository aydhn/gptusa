import datetime
import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import RuntimeEventType, PipelineStepName

@dataclass
class RuntimeEvent:
    event_id: str
    run_id: str
    event_type: RuntimeEventType
    timestamp_utc: str
    step_name: Optional[PipelineStepName]
    message: str
    severity: str
    payload: Dict[str, Any] = field(default_factory=dict)

def create_runtime_event(
    run_id: str,
    event_type: RuntimeEventType,
    message: str,
    step_name: Optional[PipelineStepName] = None,
    severity: str = "info",
    payload: Optional[Dict[str, Any]] = None
) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=str(uuid.uuid4()),
        run_id=run_id,
        event_type=event_type,
        timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        step_name=step_name,
        message=message,
        severity=severity,
        payload=payload or {}
    )

def runtime_event_to_dict(event: RuntimeEvent) -> dict:
    return {
        "event_id": event.event_id,
        "run_id": event.run_id,
        "event_type": event.event_type.value if isinstance(event.event_type, RuntimeEventType) else event.event_type,
        "timestamp_utc": event.timestamp_utc,
        "step_name": event.step_name.value if isinstance(event.step_name, PipelineStepName) else event.step_name,
        "message": event.message,
        "severity": event.severity,
        "payload": event.payload,
    }

def runtime_events_to_text(events: List[RuntimeEvent], limit: int = 50) -> str:
    lines = []
    for event in events[-limit:]:
        step = f"[{event.step_name.value if isinstance(event.step_name, PipelineStepName) else event.step_name}]" if event.step_name else ""
        lines.append(f"{event.timestamp_utc} | {event.severity.upper()} | {event.event_type.value if isinstance(event.event_type, RuntimeEventType) else event.event_type} {step}: {event.message}")
    return "\n".join(lines)

def filter_runtime_events(events: List[RuntimeEvent], event_type: Optional[RuntimeEventType] = None, step_name: Optional[PipelineStepName] = None) -> List[RuntimeEvent]:
    filtered = events
    if event_type:
        filtered = [e for e in filtered if e.event_type == event_type]
    if step_name:
        filtered = [e for e in filtered if e.step_name == step_name]
    return filtered

def write_runtime_events_jsonl(path: Path, events: List[RuntimeEvent]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for event in events:
            f.write(json.dumps(runtime_event_to_dict(event)) + "\n")
    return path

def read_runtime_events_jsonl(path: Path) -> List[Dict[str, Any]]:
    events = []
    if not path.exists():
        return events
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events
