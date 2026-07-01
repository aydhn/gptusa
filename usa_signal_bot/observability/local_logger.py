import json
import logging

from pathlib import Path
from typing import Any, Dict, Optional
import datetime
import traceback

from usa_signal_bot.core.enums import ObservabilityEventType, ObservabilitySeverity
from usa_signal_bot.observability.observability_models import ObservabilityEvent, create_observability_event_id, observability_event_to_dict

logger = logging.getLogger(__name__)

def sanitize_log_payload(payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not payload:
        return {}
    sanitized = {}
    for k, v in payload.items():
        kl = str(k).lower()
        if any(bad in kl for bad in ["token", "secret", "password", "credential", "api_key"]):
            sanitized[k] = "[REDACTED]"
        else:
            sanitized[k] = v
    return sanitized

def sanitize_log_text(text: str) -> str:
    # A simple pass-through. If needed we could use regex to redact tokens.
    return text

def append_jsonl(path: Path, record: Dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception as e:
        logger.error(f"Failed to append to jsonl at {path}: {e}", exc_info=True)
    return path

def append_text_log(path: Path, line: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        logger.error(f"Failed to append to text log at {path}: {e}", exc_info=True)
    return path

def read_observability_events_jsonl(path: Path, limit: Optional[int] = None) -> list[Dict[str, Any]]:
    if not path.exists():
        return []
    res = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            try:
                res.append(json.loads(line))
            except Exception as e:
                logger.warning(f"Failed to parse jsonl line in {path}: {e}")
            if limit and len(res) >= limit:
                break
    return res

class LocalObservabilityLogger:
    def __init__(self, log_dir: Path, jsonl_filename: str = "events.jsonl", text_filename: str = "events.log"):
        self.log_dir = log_dir
        self.jsonl_filename = jsonl_filename
        self.text_filename = text_filename
        self._jsonl_path = self.log_dir / self.jsonl_filename
        self._text_path = self.log_dir / self.text_filename
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_event(self, event: ObservabilityEvent) -> Path:
        event.payload = sanitize_log_payload(event.payload)
        d = observability_event_to_dict(event)
        append_jsonl(self._jsonl_path, d)

        # also text log
        msg = f"[{event.timestamp_utc}] [{event.severity.value}] [{event.event_type.value}] [{event.source}] {event.message}"
        append_text_log(self._text_path, sanitize_log_text(msg))
        return self._jsonl_path

    def _create_and_log(self, source: str, message: str, severity: ObservabilitySeverity,
                        event_type: ObservabilityEventType, payload: Optional[Dict[str, Any]] = None) -> ObservabilityEvent:
        event = ObservabilityEvent(
            event_id=create_observability_event_id(),
            event_type=event_type,
            severity=severity,
            timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            source=source,
            message=message,
            payload=payload or {}
        )
        self.log_event(event)
        return event

    def info(self, source: str, message: str, payload: Optional[Dict[str, Any]] = None) -> ObservabilityEvent:
        return self._create_and_log(source, message, ObservabilitySeverity.INFO, ObservabilityEventType.CUSTOM, payload)

    def warning(self, source: str, message: str, payload: Optional[Dict[str, Any]] = None) -> ObservabilityEvent:
        return self._create_and_log(source, message, ObservabilitySeverity.WARNING, ObservabilityEventType.WARNING, payload)

    def error(self, source: str, message: str, payload: Optional[Dict[str, Any]] = None) -> ObservabilityEvent:
        return self._create_and_log(source, message, ObservabilitySeverity.ERROR, ObservabilityEventType.ERROR, payload)

    def command_started(self, command: str, payload: Optional[Dict[str, Any]] = None) -> ObservabilityEvent:
        return self._create_and_log("cli", f"Command started: {command}", ObservabilitySeverity.INFO, ObservabilityEventType.COMMAND_STARTED, payload)

    def command_completed(self, command: str, duration_seconds: Optional[float] = None, payload: Optional[Dict[str, Any]] = None) -> ObservabilityEvent:
        p = payload or {}
        if duration_seconds is not None:
            p["duration_seconds"] = duration_seconds
        return self._create_and_log("cli", f"Command completed: {command}", ObservabilitySeverity.INFO, ObservabilityEventType.COMMAND_COMPLETED, p)

    def command_failed(self, command: str, error: str, payload: Optional[Dict[str, Any]] = None) -> ObservabilityEvent:
        p = payload or {}
        p["error"] = error
        return self._create_and_log("cli", f"Command failed: {command}", ObservabilitySeverity.ERROR, ObservabilityEventType.COMMAND_FAILED, p)

    def jsonl_log_path(self) -> Path:
        return self._jsonl_path

    def text_log_path(self) -> Path:
        return self._text_path
