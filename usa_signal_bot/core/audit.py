"""Audit trail system."""

from pathlib import Path
from typing import List, Optional, Dict
import json

from usa_signal_bot.core.events import SystemEvent, event_to_dict, create_event
from usa_signal_bot.core.exceptions import AuditError
from usa_signal_bot.utils.json_utils import to_json_line, from_json_line
from usa_signal_bot.utils.text_utils import redact_sensitive_text

def get_audit_log_path(log_dir: Path) -> Path:
    """Returns the path to the audit log file."""
    return log_dir / "audit.jsonl"

def _sanitize_dict(data: dict) -> dict:
    """Sanitizes dictionary values by redacting sensitive text."""
    sanitized = {}
    for k, v in data.items():
        if isinstance(v, dict):
            sanitized[k] = _sanitize_dict(v)
        elif isinstance(v, str):
            sanitized[k] = redact_sensitive_text(v)
        else:
            sanitized[k] = v
    return sanitized

def write_audit_event(event: SystemEvent, log_dir: Path) -> Path:
    """Writes an event to the audit log."""
    try:
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        audit_path = get_audit_log_path(log_dir)

        # Redact sensitive info before writing
        event_dict = event_to_dict(event)
        event_dict["message"] = redact_sensitive_text(event_dict["message"])
        event_dict["details"] = _sanitize_dict(event_dict["details"])

        json_line = to_json_line(event_dict)

        with open(audit_path, "a", encoding="utf-8") as f:
            f.write(json_line)

        return audit_path
    except Exception as e:
        raise AuditError(f"Failed to write audit event: {e}")

def read_audit_events(log_dir: Path, limit: Optional[int] = None) -> List[Dict]:
    """Reads events from the audit log."""
    audit_path = get_audit_log_path(log_dir)
    if not audit_path.exists():
        return []

    events = []
    try:
        with open(audit_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

            # If limit is provided, read from the end
            if limit is not None and limit > 0:
                lines = lines[-limit:]

            for line in lines:
                if line.strip():
                    events.append(from_json_line(line))
        return events
    except Exception as e:
        raise AuditError(f"Failed to read audit events: {e}")

def tail_audit_events(log_dir: Path, n: int = 20) -> List[Dict]:
    """Returns the last n events from the audit log."""
    return read_audit_events(log_dir, limit=n)

def audit_safe_mode_confirmation(context) -> SystemEvent:
    """Creates a SystemEvent for safe mode confirmation."""
    return create_event(
        event_type="SAFE_MODE_CONFIRMED",
        severity="INFO",
        message="Safe mode confirmed.",
        component="runtime",
        details=context.as_summary_dict().get("safe_mode", {})
    )

def audit_forbidden_operation(operation_name: str, reason: str, log_dir: Path) -> SystemEvent:
    """Creates and logs a SystemEvent for a forbidden operation."""
    event = create_event(
        event_type="FORBIDDEN_OPERATION_BLOCKED",
        severity="CRITICAL",
        message=f"Blocked forbidden operation: {operation_name}. Reason: {reason}",
        component="security"
    )
    write_audit_event(event, log_dir)
    return event
